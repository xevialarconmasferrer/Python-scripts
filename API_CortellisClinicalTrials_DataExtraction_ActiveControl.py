import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import xml.etree.ElementTree as ET
import concurrent.futures
import re
import openpyxl

# Function to access API and request HTML.
def getURL(url, API_KEY, API_PWD):
    """
    Execute a REST call and return XML
    @param url:
    @return: XML and text message or JSON :)
    """
    headers = {'Accept': 'application/xml'}
    response = None
    try:
        r = requests.get(url, auth=HTTPDigestAuth(API_KEY, API_PWD), headers=headers)
        r.raise_for_status()
        return r.text, "success"
    except Exception as e:
        return None, str(e)

# Function to process each NCT code
def process_nct(n, API_KEY, API_PWD, cont = 0):
    result = {"NCT": n, "url": None, "TrialID": None, "Active Control Number" : None, "Active Control" : None}
    
    idUrl = f"https://****=trialIdentifiers:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID   
        
        for elen in context.iterfind('Filters/Filter'):

            if elen.attrib.get('name') == 'trialActiveControls':

                result["Active Control Number"] = elen.attrib["total"]

                substudies = ";".join(el.attrib["label"] for el in elen)
                result["Active Control"] = substudies           
                  
    return result

# Importing Excel file with list of project codes.
data = pd.read_excel(r'****.xlsx')
NCT = data["NCT"].tolist()

API_KEY = '****'
API_PWD = '****'

# Using ThreadPoolExecutor for parallel processing

results = []


with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
    future_to_origins = {executor.submit(process_nct, n, API_KEY, API_PWD): n for n in NCT[0:1095]}
    for count, future in enumerate(concurrent.futures.as_completed(future_to_origins), 1):
        try:
            result = future.result()
            results.append(result)
            print(count, "of", len(NCT))
        except Exception as e:
            print(f"Error processing {future_to_origins[future]}: {e}")

# Creating DataFrame from results
df2 = pd.DataFrame(results)

# Exporting dataframe to Excel file
df2.to_excel("****.xlsx")

print("Done!!")
