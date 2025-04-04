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
    result = {"NCT": n, "url": None, "TrialID": None, 'Inclusion_Criteria_text' : None ,'Inclusion_Criteria_index' : 0, 'Exclusion_Criteria_text' : None ,'Exclusion_Criteria_index' : 0, 'Primary_Endpoint' : 0, 
                                        'Secondary_Endpoint' : 0 ,'Biomarkers' : 0 ,'Disease marker' : 0 ,"Therapeutic effect" : 0, "Toxic effect" : 0}
    
    idUrl = f"https://****:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID   
            
        #Once we get the TrialID we can go to the html to get the fields from cortellis.
            
        idURL = f"https://****={TrialID}"

        response, message = getURL(idURL, API_KEY, API_PWD)
        if message == "success":
            context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))

            #Gettin inclusion/exclusion criteria text:   

            inc = ""
            for elem in context.iterfind('Trial/CriteriaInclusion'):
                if elem in context.iterfind('Trial/CriteriaInclusion'):
                    inc = elem.text
                else:
                    inc = "Not found"

                result["Inclusion_Criteria_text"] = inc

                exc = ""
                for elem in context.iterfind('Trial/CriteriaExclusion'):
                    if elem in context.iterfind('Trial/CriteriaExclusion'):
                        exc = elem.text
                    else:
                        exc = "Not found"

                result["Exclusion_Criteria_text"] = exc

                #Getting inclusion/exclusion criteria index:

                i = 0
                for elem in context.iterfind('Trial/EligibilityCriteriaTerms/InclusionCriteria/Inclusion/Criterion'):
                    if elem in context.iterfind('Trial/EligibilityCriteriaTerms/InclusionCriteria/Inclusion/Criterion'):
                        i = i+1
                    else:
                        i = i
                ini = i
                
                result["Inclusion_Criteria_index"] = ini

                e = 0
                for elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                    if elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                        e = e+1
                    else:
                        e = e
                ene = e
                result["Exclusion_Criteria_index"] = ene

                #Gettin the number of primary and secondary endpoints:

                p = 0
                for elem in context.iterfind('Trial/MeasuresOutcome/MeasuresPrimary/Measure/Description'):
                    if elem in context.iterfind('Trial/MeasuresOutcome/MeasuresPrimary/Measure/Description'):
                        p = p+1

                        #print('Number of primary endpoints:', p)
                    else:
                        p = p
                prim = p

                result["Primary_Endpoint"] = prim

                s = 0
                for elem in context.iterfind('Trial/MeasuresOutcome/MeasureSecondary/Measure/Description'):
                    if elem in context.iterfind('Trial/MeasuresOutcome/MeasureSecondary/Measure/Description'):
                        s = s+1
                        #print('Number of secondary endpoints:', s)
                    else:
                        s = s
                sec = s

                result["Secondary_Endpoint"] = sec
                
                #Getting the number of biomarkers:
                bm = 0
                for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                    if elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                        bm = bm+1
                        #print("Number of biomarkers:", bm)
                    else:
                        bm = bm
                biom = bm

                result["Biomarker"] = biom
            
                #Getting the number of disease marker:
                d1 = 0
                d2 = 0
                d3 = 0                 
                for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                    if elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                        Tipo = elem.attrib['role']
                        if Tipo == "Disease marker":
                            d1 = d1 +1
                            d2 = d2
                            d3 = d3
                        elif Tipo == "Therapeutic effect marker":
                            d1 = d1
                            d2 = d2 +1
                            d3 = d3
                        elif Tipo == "Toxic effect marker":
                            d1 = d1
                            d2 = d2
                            d3 = d3 +1
                        elif Tipo == "Disease marker;Therapeutic effect marker" or Tipo == "Therapeutic effect marker;Disease marker":
                            d1 = d1 +1
                            d2 = d2 +1
                            d3 = d3
                        elif Tipo == "Disease marker;Toxic effect marker" or Tipo == "Toxic effect marker;Disease marker":
                            d1 = d1 +1
                            d2 = d2
                            d3 = d3 +1
                        elif Tipo == "Toxic effect marker;Therapeutic effect marker" or Tipo == "Therapeutic effect marker;Toxic effect marker":
                            d1 = d1
                            d2 = d2 +1
                            d3 = d3 +1
                        else:
                            d1 = d1
                            d2 = d2
                            d3 = d3

                result["Disease marker"] = d1
                result["Therapeutic effect"] = d2
                result["Toxic effect"] = d3

            return result

# Importing Excel file with list of project codes.
data = pd.read_excel(r'****.xlsx')
NCT = data["NCT"].tolist()

API_KEY = '****'
API_PWD = '****'

# Using ThreadPoolExecutor for parallel processing

results = []


with concurrent.futures.ThreadPoolExecutor(max_workers = 50) as executor:
    future_to_origins = {executor.submit(process_nct, n, API_KEY, API_PWD): n for n in NCT[0:6354]}
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
