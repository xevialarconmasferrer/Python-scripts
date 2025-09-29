
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
def process_generic_name(n, API_KEY, API_PWD, cont = 0):

    records = []

    idUrl = f"https://***:{n}"

    response, message = getURL(idUrl, API_KEY, API_PWD)

    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        trials = context.find("SearchResults").findall("Trial")
        pattern = re.compile(r"NCT\d{8}")
        
        # Sacar los Ids
        for trial in trials:
            trial_id = trial.get("Id")
            nct = None
            # Buscamos el NCT dentro de los elementos del trial
            for elem in trial.iter():
                if elem.text:
                    match = pattern.search(elem.text)
                    if match:
                        nct = match.group()
                        break  # asumimos solo un NCT por trial
            if nct:
                records.append({
                    "GenericName": n,
                    "Trial_id": trial_id,
                    "NCT": nct,
                    "url": idUrl
                                    })

    return records


# Importing Excel file with list of project codes.
data = pd.read_excel(r'****.xlsx')
generic_names = data["Genericname"].tolist()

API_KEY = '*******'
API_PWD = '*****'

# Using ThreadPoolExecutor for parallel processing

all_records = []

all_records = []
for name in generic_names:
    all_records += process_generic_name(name, API_KEY, API_PWD)


# Creating DataFrame from results
df2 = pd.DataFrame(all_records)

# Exporting dataframe to Excel file
df2.to_excel("***.xlsx")

print("Done!!")
