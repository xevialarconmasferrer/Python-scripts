import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import xml.etree.ElementTree as ET
import concurrent.futures
import re

# Function to access API and request HTML.
def getURL(url, KEY, PWD):
    """
    Execute a REST call and return XML
    @param url:
    @return: XML and text message or JSON :)
    """
    headers = {'Accept': 'application/xml'}
    response = None
    try:
        r = requests.get(url, auth=HTTPDigestAuth(KEY, PWD), headers=headers)
        r.raise_for_status()
        return r.text, "success"
    except Exception as e:
        return None, str(e)

# Function to process each NCT code
def Origins(n, API_KEY, API_PWD, cont=0):
    result = {"DrugName": n, "url": None, "ID": None, "Licensed": 0, "Acquisition": 0, "Collaborative": 0, "Origin": 0, "Text": None}
    idUrl = f'https://**************************:"{n}"'
    response, message = getURL(url=idUrl, KEY=API_KEY, PWD=API_PWD)

    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

        for elem in context.iterfind('SearchResults/Drug'):
            DrugID = elem.attrib['id']
            result["ID"] = DrugID

            dUrl = f"https://***************************{DrugID}"
            response, message = getURL(url=dUrl, KEY=API_KEY, PWD=API_PWD)

            result["url"] = dUrl

            if message == "success":
                context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

                for elem in context.iterfind('DevelopmentProfile/Summary/value'):
                    result["Text"] = elem.text

                    if any(re.search(term, elem.text, re.IGNORECASE) for term in ["licensed", "licensing", "licensed-in"]):
                        result["Licensed"] = "Yes"
                    else:
                        result["Licensed"] = "No"

                    if any(re.search(term, elem.text, re.IGNORECASE) for term in ["acquired", "acquisition"]):
                        result["Acquisition"] = "Yes"
                    else:
                        result["Acquisition"] = "No"

                    if any(re.search(term, elem.text, re.IGNORECASE) for term in ["collaboration", "collaborate", "collaboratieve"]):
                        result["Collaborative"] = "Yes"
                    else:
                        result["Collaborative"] = "No"

                    if result["Licensed"] == "Yes" and result["Acquisition"] == "Yes" and result["Collaborative"] == "Yes":
                        result["Origin"] = "Licensed-in; Acquisition; Collaborative"
                    elif result["Licensed"] == "Yes" and result["Acquisition"] == "Yes" and result["Collaborative"] == "No":
                        result["Origin"] = "Licensed-in; Acquisition"
                    elif result["Licensed"] == "Yes" and result["Acquisition"] == "No" and result["Collaborative"] == "Yes":
                        result["Origin"] = "Licensed-in; Collaborative"
                    elif result["Licensed"] == "No" and result["Acquisition"] == "Yes" and result["Collaborative"] == "Yes":
                        result["Origin"] = "Acquisition; Collaborative"
                    elif result["Licensed"] == "Yes" and result["Acquisition"] == "No" and result["Collaborative"] == "No":
                        result["Origin"] = "Licensed-in"
                    elif result["Licensed"] == "No" and result["Acquisition"] == "Yes" and result["Collaborative"] == "No":
                        result["Origin"] = "Acquisition"
                    elif result["Licensed"] == "No" and result["Acquisition"] == "No" and result["Collaborative"] == "Yes":
                        result["Origin"] = "Collaborative"

    return result

# Importing Excel file with list of project codes.
data = pd.read_excel(r':*************.xlsx')
ID = data['Drug Name'].tolist()

API_KEY = '**********'
API_PWD = '*******'

# Using ThreadPoolExecutor for parallel processing
results = []

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    future_to_origins = {executor.submit(Origins, n, API_KEY, API_PWD): n for n in ID[0:7357]}
    for count, future in enumerate(concurrent.futures.as_completed(future_to_origins), 1):
        try:
            result = future.result()
            results.append(result)
            print(count, "of", len(ID[0:7357]))
        except Exception as e:
            print(f"Error processing {future_to_origins[future]}: {e}")

# Creating DataFrame from results
df2 = pd.DataFrame(results)

# Exporting dataframe to Excel file
df2.to_excel(r"************.xlsx", index=False)

print("Done!!")
