import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import time
import xml.etree.ElementTree as ET
import concurrent.futures
import re
import os
import openpyxl
from datetime import datetime

start_time = time.time()

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
    result = {"NCT": n, "url": None, "TrialID": None, 'Indications' : None, 'Phase' : None, 'Recruitment status' : None, 'Country' : None, 'Number Of Sites' : None, "Companies Sponsor" : None, "Class" : None,
              'Technologies' : None,"Companies Collaborator": None, 'TermsPatientSelection' : None, 'TrialCategories' : None, 'TermsDesign' : None, 'TermsEndpoint' : None,
              'PatientCountEnrollment' : None, 'DateStart' : None, 'DateEnd' : None, 'TrialDuration' : None, 'DateChangeLast' : None, 'DateAdded' : None, 'Inclusion_Criteria_text' : None ,'Inclusion_Criteria_index' : 0, 
              'Exclusion_Criteria_text' : None ,'Exclusion_Criteria_index' : 0, 'Primary_Endpoint' : 0, 'Secondary_Endpoint' : 0 ,'Biomarkers' : 0 ,'Disease marker' : 0 ,
              "Therapeutic effect" : 0, "Toxic effect" : 0}
    
              
    
    idUrl = f"*******************query=trialIdentifiers:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID   
            
        #Once we get the TrialID we can go to the html to get the fields from cortellis.
            
        idURL = f"***********************trials?idList={TrialID}"

        response, message = getURL(idURL, API_KEY, API_PWD)
        if message == "success":
            context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

            #Indication
            ind = context.find("Trial/Indications/Indication")
            result["Indications"] = ind.text if ind is not None else "Not found"

            #Phase
            ph = context.find("Trial/Phase")
            result["Phase"] = ph.text if ph is not None else "Not found"

            #Recruitment status
            rec = context.find("Trial/RecruitmentStatus")
            result["Recruitment status"] = rec.text if rec is not None else "Not found"

            #Country
            country = context.find("Trial/SitesByCountries/SitesByCountry")
            result["Country"] = country.get("country") if country is not None else "Not found"

            #Number of sites
            sit = context.find("Trial/NumberOfSites")
            result["Number Of Sites"] = sit.text if sit is not None else "Not found"

            #Companies Sponsor
            sponsor = context.find('Trial/CompaniesSponsor')
            result["Companies Sponsor"] = "; ".join(el.text for el in sponsor) if sponsor is not None else "Not found"

            #Companies Collaborator
            collab = context.find('Trial/CompaniesCollaborator')
            result["Companies Collaborator"] = "; ".join(el.text for el in collab) if collab is not None else "Not found"

            #Class
            clas = context.find('Trial/Class')
            result["Class"] = "; ".join(el.text for el in clas) if clas is not None else "Not found"

            #Technologies
            tech = context.find('Trial/Technologies')
            result["Technologies"] = "; ".join(el.text for el in tech) if tech is not None else "Not found"

            #Terms Patient Selection
            tps= context.find('Trial/TermsPatientSelection')
            result["TermsPatientSelection"] = "; ".join(el.text for el in tps) if tps is not None else "Not found"

            #Trial categories
            tc = context.find('Trial/TrialCategories')
            result["TrialCategories"] = "; ".join(el.text for el in tc) if tc is not None else "Not found"

            #TermsDesign
            td = context.find('Trial/TermsDesign')
            result["TermsDesign"] = "; ".join(el.text for el in td) if td is not None else "Not found"

            #TermsEndpoint
            te= context.find('Trial/TermsEndpoint')
            result["TermsEndpoint"] = "; ".join(el.text for el in te) if te is not None else "Not found"

            #PatientCountEnrollment
            enr= context.find("Trial/PatientCountEnrollment")
            result["PatientCountEnrollment"] = enr.text if enr is not None else "Not found"

            #DateStart
            start = context.find("Trial/DateStart")
            result["DateStart"] = start.text.split("T")[0] if start is not None else "Not found"

            #DateEnd
            end = context.find("Trial/DateEnd")
            result["DateEnd"] = end.text.split("T")[0] if end is not None else "Not found"

            #DateChangeLast
            ch= context.find("Trial/DateChangeLast")
            result["DateChangeLast"] = ch.text.split("T")[0] if ch is not None else "Not found"

            #DateAdded
            ad = context.find("Trial/DateAdded")
            result["DateAdded"] = ad.text.split("T")[0] if ad is not None else "Not found"

            #Gettin inclusion/exclusion criteria text:   

            # Inclusion criteria
            inc = context.find('Trial/CriteriaInclusion')
            result["Inclusion_Criteria_text"] = inc.text if inc is not None else "Not found"

            # Exclusion criteria
            exc = context.find('Trial/CriteriaExclusion')
            result["Exclusion_Criteria_text"] = exc.text if exc is not None else "Not found"

            # Getting inclusion/exclusion criteria index:
            i = 0
            for elem in context.iterfind('Trial/EligibilityCriteriaTerms/InclusionCriteria/Inclusion/Criterion'):
                i += 1
            result["Inclusion_Criteria_index"] = i

            e = 0
            for elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                e += 1
            result["Exclusion_Criteria_index"] = e

            # Getting the number of primary and secondary endpoints:
            p = 0
            for elem in context.iterfind('Trial/OutcomeMeasureTerms/PrimaryEndpoints/PrimaryEndpoint'):
                p += 1
            result["Primary_Endpoint"] = p

            s = 0
            for elem in context.iterfind('Trial/OutcomeMeasureTerms/SecondaryEndpoints/SecondaryEndpoint'):
                s += 1
            result["Secondary_Endpoint"] = s

            # Getting the number of biomarkers:
            bm = 0
            for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                bm += 1
            result["Biomarkers"] = bm
            
            #Getting the number of disease marker:
            d1 = 0
            d2 = 0
            d3 = 0                 
            for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                Tipo = elem.attrib.get('role', '')
                if "disease marker" in Tipo.lower():
                    d1 += 1
                elif "Therapeutic effect marker" in Tipo.lower():
                    d2 += 1 
                elif "Toxic effect marker" in Tipo.lower():
                    d3 += 1 

            result["Disease marker"] = d1
            result["Therapeutic effect"] = d2
            result["Toxic effect"] = d3

        return result

# Importing Excel file with list of project codes.
input_path = input("Enter the Excel file path: ")
output_name = input("Enter the output file name (without extension): ")
data = pd.read_excel(input_path)
NCT = data["NCT"].tolist()

API_KEY = '****************'
API_PWD = '******************'

# Using ThreadPoolExecutor for parallel processing

results = []


with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
    future_to_origins = {executor.submit(process_nct, n, API_KEY, API_PWD): n for n in NCT} 
    for count, future in enumerate(concurrent.futures.as_completed(future_to_origins), 1):
        try:
            result = future.result()
            results.append(result)
            print(count, "of", len(NCT))
        except Exception as e:
            print(f"Error processing {future_to_origins[future]}: {e}")

# Creating DataFrame from results
results = [r for r in results if r is not None]
df2 = pd.DataFrame(results)

#TrialDuration              
Start = pd.to_datetime(df2['DateStart'], errors='coerce')
End = pd.to_datetime(df2['DateEnd'], errors='coerce')

df2['TrialDuration'] = (((End - Start).dt.days) / 30.44).round(2).astype(str) + " months"

# Exporting dataframe to Excel file
input_dir = os.path.dirname(input_path)
output_path = os.path.join(input_dir, f"{output_name}.xlsx")
df2.to_excel(output_path)

#Timelapse
end_time = time.time()
elapsed = end_time - start_time

minutes = int(elapsed // 60)
seconds = int(elapsed % 60)

print(f"Done!! Process completed in {minutes}m {seconds}s")
