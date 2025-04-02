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
    result = {"NCT": n, "url": None, "TrialID": None, "Trial Arms": 0, "Trial Arm text" : None, "Title" : None, "Title Official" : None, "Protocol and Outcomes" : None, "Criteria of inclusion" : None,"Master protocol" : 0, "Sub-study" : 0, "Biomarker study" : 0, "Umbrella" : 0, 
              "Platform" : 0, "Combination drug" : 0, "Escalation" : 0 , "Expansion" : 0 , "Adaptive trial" : 0, "Bioavailability" : 0, "Bioequivalence trial" : 0, "Screening trial" : 0,
              "Chinese population" : 0, "Japanese population" : 0}
    
    idUrl = f"https://********:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID

        arms = 0
        for elem in context.iterfind('SearchResults/Trial/ArmLabels'):
            if elem in context.iterfind('SearchResults/Trial/ArmLabels'):
                arms = len(elem)
            else:
                arms = 0
            result["Trial Arms"] = arms
                
            for elem in context.iterfind('SearchResults/Trial/ArmLabels'):
                if elem in context.iterfind('SearchResults/Trial/ArmLabels'):
                    text = ";".join(el.text for el in elem)
            result["Trial Arm text"] = text
            
            
            idUrl = f"https://*********={TrialID}"
            response, message = getURL(idUrl, API_KEY, API_PWD)
            
            if message == "success":
                context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

                for elep in context.iterfind('Trial/TitleDisplay'):
                    if elep in context.iterfind('Trial/TitleDisplay'):
                        result["Title"] = elep.text    

                for eles in context.iterfind('Trial/TitleOfficial'):
                    if eles in context.iterfind('Trial/TitleOfficial'):
                        result["Title Official"] = eles.text  


                for elem in context.iterfind('Trial/ProtocolAndOutcomes'):
                    if elem in context.iterfind('Trial/ProtocolAndOutcomes'):
                        prot = " ".join(el.text for el in elem)
                        result["Protocol and Outcomes"] = prot  

                    for helem in context.iterfind('Trial/CriteriaInclusion'):
                        if helem in context.iterfind('Trial/CriteriaInclusion'):
                            result["Criteria of inclusion"] = helem.text

                            substudies = " ".join(el.text for el in elem)
                            substudies1 = " ".join(hel.text for hel in helem)

                            Sub = substudies + substudies1

                            result["Master protocol"] = len(re.findall("master protocol", Sub,re.IGNORECASE))
                            result["Sub-study"] = len(re.findall("sub-study", Sub,re.IGNORECASE))
                            result["Biomarker study"] = len(re.findall("biomarker study", Sub,re.IGNORECASE))
                            result["Umbrella"] = len(re.findall("umbrella", Sub,re.IGNORECASE))
                            result["Combination drug"] = len(re.findall("combination", Sub,re.IGNORECASE)) + len(re.findall("combinated", Sub,re.IGNORECASE))
                            result["Escalation"] = len(re.findall("escalation", Sub, re.IGNORECASE))
                            result["Expansion"] = len(re.findall("expansion", Sub, re.IGNORECASE))
                            result["Platform"] = len(re.findall("platform", Sub, re.IGNORECASE))
                            result["Bioavailability"] = len(re.findall("bioavailability", Sub, re.IGNORECASE))
                            result["Bioequivalence trial"] = len(re.findall("bioequivalence", Sub, re.IGNORECASE))
                            result["Screening trial"] = len(re.findall("screening", Sub, re.IGNORECASE))
                            result["Adaptive trial"] = len(re.findall("adaptive", Sub, re.IGNORECASE))
                            result["Chinese population"] = len(re.findall("chinese", Sub, re.IGNORECASE))
                            result["Japanese population"] = len(re.findall("japanese", Sub, re.IGNORECASE))
                            result["Proof of concept"] = len(re.findall(("proof-of-concept"), Sub, re.IGNORECASE)) + len(re.findall(("proof of concept"), Sub, re.IGNORECASE))     
    
        return result

# Importing Excel file with list of project codes.
data = pd.read_excel(r'************.xlsx')
NCT = data["NCT"].tolist()

API_KEY = '********'
API_PWD = '********'

# Using ThreadPoolExecutor for parallel processing

results = []


with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
    future_to_origins = {executor.submit(process_nct, n, API_KEY, API_PWD): n for n in NCT}
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
df2.to_excel("*****.xlsx")

print("Done!!")
