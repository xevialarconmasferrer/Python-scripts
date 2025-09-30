# Importing packages

import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import xml.etree.ElementTree as ET
import concurrent.futures
import re
import json


# Function to access API and request HTML.
def getURL(url):
    """
    Execute a REST call and return XML
    @param url:
    @return: XML and text message or JSON :)
    """
    headers = {'Accept': 'application/xml'}
    response = None
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r.text, "success"
    except Exception as e:
        return None, str(e)

def process_nct(n,cont=0):

    records = {"NCT": n, "Start_date": None, "Sponsor": None, "Collaborators": None, "Enrollment" : None,  "Phase" : None, "Indication" : None, "Study_type" : None, "Location" : None, "Status" : None}
    
    idURL = f"https://clinicaltrials.gov/api/v2/studies/{n}?format=json"
    response, message = getURL(idURL)
   

    if message == "success":
        try:
            data = json.loads(response)     
        except json.JSONDecodeError as e:
            print("Error al parsear JSON:", e)
            return None

        #Start Date (Actual)

        start_date = data.get("protocolSection", {}) \
                            .get("statusModule", {}) \
                            .get("startDateStruct", {})
        
        start = start_date.get("date")
        records["Start_date"] = start

        #Sponsor 

        sponsor = data.get("protocolSection", {}) \
                            .get("sponsorCollaboratorsModule", {}) \
                            .get("leadSponsor", {})
        
        sp = sponsor.get("name")
        records["Sponsor"] = sp

        #Collaborators

        collab= data.get("protocolSection", {}) \
                            .get("sponsorCollaboratorsModule", {}) \
                            .get("collaborators", {})
        cl = []

        for c in collab:
            if "name" in c:
                cl.append(c["name"])

        records["Collaborators"] = cl

        #Enrollment (Actual)

        Enrollment = data.get("protocolSection", {}) \
                            .get("designModule", {}) \
                            .get("enrollmentInfo", {})
        
        Enr = Enrollment.get("count")
        records["Enrollment"] = Enr

        #Study Type

        study = data.get("protocolSection", {}) \
                            .get("designModule", {}) \
        
        st = study.get("studyType")
        records["Study_type"] = st

        #Phase

        phase = data.get("protocolSection", {}) \
                            .get("designModule", {}) 
    
        ph = phase.get("phases")
        records["Phase"] = ph[0]
               
        #Indication

        Indication = data.get("protocolSection", {}) \
                            .get("conditionsModule", {}) 
        
        ind = Indication.get("conditions")
        records["Indication"] =  ind[0]

        #Location

        location = data.get("protocolSection", {}) \
                            .get("contactsLocationsModule", {}) \
                            .get("locations") 
    
        if location and isinstance(location[0], dict):
            country = location[0].get('country')
            records["Location"] = country
        else:
            print("No se pudo acceder a 'country'.")

        #Status

        status = data.get("protocolSection", {}) \
                            .get("statusModule", {}) 
        
        if status and isinstance(status, dict):
            stat = status.get('overallStatus')
            records["Status"] = stat
        else:
            print("No se pudo acceder a 'country'.")
    
    return records


# Importing Excel file with list of project codes.

data = pd.read_excel(r'end.xlsx')
AllRecords = data["NCT"].tolist()

# Using ThreadPoolExecutor for parallel processing

results = []

with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
    future_to_origins = {executor.submit(process_nct, n): n for n in AllRecords}
    for count, future in enumerate(concurrent.futures.as_completed(future_to_origins), 1):
        try:
            result = future.result()
            results.append(result)
            print(count, "of", len(AllRecords))
        except Exception as e:
            print(f"Error processing {future_to_origins[future]}: {e}")


# Creating DataFrame from results
df2 = pd.DataFrame(results)

# Exporting dataframe to Excel file
df2.to_excel("final.xlsx")

print("Done!!")
