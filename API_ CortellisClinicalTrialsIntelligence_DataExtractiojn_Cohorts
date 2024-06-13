import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import xml.etree.ElementTree as ET
import concurrent.futures
import re

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
    result = {"NCT": n, "url": None, "TrialID": None, "basket": 0, "umbrella": 0, "part": 0, "expansion": 0, "escalation": 0, "cohort": 0, "Number of cohorts": 0, "Trial Arm text": None}
    idUrl = f"************************************:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID
            
            idUrl = f"*************************************={TrialID}"
            response, message = getURL(idUrl, API_KEY, API_PWD)
            
            if message == "success":
                context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
                for elem in context.iterfind('Trial/ProtocolAndOutcomes'):
                    substudies = " ".join(el.text for el in elem)
                    result["basket"] = len(re.findall("basket", substudies,re.IGNORECASE))
                    result["umbrella"] = len(re.findall("umbrella", substudies,re.IGNORECASE))
                    result["part"] = len(re.findall("part", substudies, re.IGNORECASE))
                    result["expansion"] = len(re.findall("expansion", substudies, re.IGNORECASE))
                    result["escalation"] = len(re.findall("escalation", substudies, re.IGNORECASE))
                    result["cohort"] = len(re.findall("cohort", substudies, re.IGNORECASE))
                
                arms = 0
                for elem in context.iterfind('Trial/TrialArms/Arm'):
                    if elem in context.iterfind('Trial/TrialArms/Arm'):
                        arms = arms + 1
                    else:
                        arms = 0
                result["Number of cohorts"] = arms
                
                for elem in context.iterfind('Trial/TrialArms'):
                    if elem in context.iterfind('Trial/TrialArms'):
                        text = "******".join(el.attrib["label"] for el in elem)
                result["Trial Arm text"] = text
    return result

# Importing Excel file with list of project codes.
data = pd.read_excel(r'****************')
NCT = data['NCT'].tolist()

API_KEY = '***************'
API_PWD = '***************'

# Using ThreadPoolExecutor for parallel processing

results = []

count = 0

for n in NCT[0:1841]:
    count = count +1
    print(count, "of", len(NCT))
    result =  process_nct(n, API_KEY, API_PWD)
    results.append(result)



# Creating DataFrame from results
df2 = pd.DataFrame(results)

# Exporting dataframe to Excel file
df2.to_excel("***************************", index=False)

print("Done!!")
