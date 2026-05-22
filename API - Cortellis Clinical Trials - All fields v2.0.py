import requests
from requests.auth import HTTPDigestAuth
import pandas as pd
import xml.etree.ElementTree as ET
import concurrent.futures
import re
import openpyxl
from datetime import datetime

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
    
              
    
    idUrl = f"************************?query=trialIdentifiers:{n}"
    response, message = getURL(idUrl, API_KEY, API_PWD)
    
    if message == "success":
        context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']
            result["url"] = idUrl
            result["TrialID"] = TrialID   
            
        #Once we get the TrialID we can go to the html to get the fields from cortellis.
            
        idURL = f"***********************?idList={TrialID}"

        response, message = getURL(idURL, API_KEY, API_PWD)
        if message == "success":
            context = ET.ElementTree(ET.fromstring(response.encode('utf-8')))
            
            #Indication

            ind =""

            for elem in context.iterfind("Trial/Indications/Indication"):
                if elem in context.iterfind("Trial/Indications/Indication"):
                    ind = elem.text
                else:
                    ind = "Not found"

                result["Indications"] = ind
            
            #Phase

            ph = ""

            for elem in context.iterfind("Trial/Phase"):
                if elem in context.iterfind("Trial/Phase"):
                    ph = elem.text
                else:
                    ph = "Not found"
                
                result["Phase"] = ph
            
            #Recruitment status

            rec = ""

            for elem in context.iterfind("Trial/RecruitmentStatus"):
                if elem in context.iterfind("Trial/RecruitmentStatus"):
                    rec = elem.text
                else:
                    rec = "Not found"
                
                result["Recruitment status"] = rec
            
            #Country

            country = ""

            for elem in context.iterfind("Trial/SitesByCountries/SitesByCountry"):
                if elem in context.iterfind("Trial/SitesByCountries/SitesByCountry"):
                    country = elem.get("country")
                else:
                    country = "Not found"
                
                result["Country"] = country
            
            #Number of sites

            sit = ""

            for elem in context.iterfind("Trial/NumberOfSites"):
                if elem in context.iterfind("Trial/NumberOfSites"):
                    sit = elem.text
                else:
                    sit = "Not found"
                
                result["Number Of Sites"] = sit

            #Companies Sponsor

            for elem in context.iterfind('Trial/CompaniesSponsor'):
                if elem in context.iterfind('Trial/CompaniesSponsor'):
                    text = "; ".join(el.text for el in elem)
            result["Companies Sponsor"] = text

            #Companies collaborator

            for elem in context.iterfind('Trial/CompaniesCollaborator'):
                if elem in context.iterfind('Trial/CompaniesCollaborator'):
                    text = "; ".join(el.text for el in elem)
            result["Companies Collaborator"] = text

            #Class

            for elem in context.iterfind('Trial/Class'):
                if elem in context.iterfind('Trial/Class'):
                    text = "; ".join(el.text for el in elem)
            result["Class"] = text

            #Technologies

            for elem in context.iterfind('Trial/Technologies'):
                if elem in context.iterfind('Trial/Technologies'):
                    text = "; ".join(el.text for el in elem)
            result["Technologies"] = text

            #Terms Patient Selection

            for elem in context.iterfind('Trial/TermsPatientSelection'):
                if elem in context.iterfind('Trial/TermsPatientSelection'):
                    text = "; ".join(el.text for el in elem)
            result["TermsPatientSelection"] = text

            #Trial categories

            for elem in context.iterfind('Trial/TrialCategories'):
                if elem in context.iterfind('Trial/TrialCategories'):
                    text = "; ".join(el.text for el in elem)
            result["TrialCategories"] = text

            #TermsDesign

            for elem in context.iterfind('Trial/TermsDesign'):
                if elem in context.iterfind('Trial/TermsDesign'):
                    text = "; ".join(el.text for el in elem)
            result["TermsDesign"] = text

            #TermsEndpoint

            for elem in context.iterfind('Trial/TermsEndpoint'):
                if elem in context.iterfind('Trial/TermsEndpoint'):
                    text = "; ".join(el.text for el in elem)
            result["TermsEndpoint"] = text

            #PatientCountEnrollment

            Enr = ""

            for elem in context.iterfind("Trial/PatientCountEnrollment"):
                if elem in context.iterfind("Trial/PatientCountEnrollment"):
                    Enr = elem.text
                else:
                    Enr = "Not found"
                
                result["PatientCountEnrollment"] = Enr

            #DateStart

            Start = ""

            for elem in context.iterfind("Trial/DateStart"):
                if elem in context.iterfind("Trial/DateStart"):
                    Start = elem.text.split("T")[0]
                else:
                    Start = "Not found"
                
                result["DateStart"] = Start

            #DateEnd

            End = ""

            for elem in context.iterfind("Trial/DateEnd"):
                if elem in context.iterfind("Trial/DateEnd"):
                    End = elem.text.split("T")[0]
                else:
                    End = "Not found"

                result["DateEnd"] = End

            #DateChangeLast

            Ch = ""

            for elem in context.iterfind("Trial/DateChangeLast"):
                if elem in context.iterfind("Trial/DateChangeLast"):
                    Ch = elem.text.split("T")[0]
                else:
                    Ch = "Not found"
                
                result["DateChangeLast"] = Ch

            #DateAdded

            Ad = ""

            for elem in context.iterfind("Trial/DateAdded"):
                if elem in context.iterfind("Trial/DateAdded"):
                    Ad = elem.text.split("T")[0]
                else:
                    Ad = "Not found"
                
                result["DateAdded"] = Ad


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
                
                result["Inclusion_Criteria_index"] = i

                e = 0
                for elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                    if elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                        e = e+1
                    else:
                        e = e
                result["Exclusion_Criteria_index"] = e

                #Gettin the number of primary and secondary endpoints:

                p = 0
                for elem in context.iterfind('Trial/OutcomeMeasureTerms/PrimaryEndpoints/PrimaryEndpoint'):
                    if elem in context.iterfind('Trial/OutcomeMeasureTerms/PrimaryEndpoints/PrimaryEndpoint'):
                        p = p+1

                        #print('Number of primary endpoints:', p)
                    else:
                        p = p

                result["Primary_Endpoint"] = p

                s = 0
                for elem in context.iterfind('Trial/OutcomeMeasureTerms/SecondaryEndpoints/SecondaryEndpoint'):
                    if elem in context.iterfind('Trial/OutcomeMeasureTerms/SecondaryEndpoints/SecondaryEndpoint'):
                        s = s+1
                        #print('Number of secondary endpoints:', s)
                    else:
                        s = s
                result["Secondary_Endpoint"] = s
                
                #Getting the number of biomarkers:
                bm = 0
                for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                    if elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                        bm = bm+1
                    else:
                        bm = bm

                result["Biomarkers"] = bm
            
                #Getting the number of disease marker:
                d1 = 0
                d2 = 0
                d3 = 0                 
                for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                    if elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                        Tipo = elem.attrib['role']
                        if "Disease marker" in Tipo:
                            d1 = d1 +1
                            d2 = d2
                            d3 = d3
                        elif "Therapeutic effect marker" in Tipo:
                            d1 = d1
                            d2 = d2 +1
                            d3 = d3
                        elif "Toxic effect marker" in Tipo:
                            d1 = d1
                            d2 = d2
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
data = pd.read_excel(r'*************\NCT_Andy.xlsx')
NCT = data["NCT"].tolist()

API_KEY = '**************'
API_PWD = '************'

# Using ThreadPoolExecutor for parallel processing

results = []


with concurrent.futures.ThreadPoolExecutor(max_workers = 100) as executor:
    future_to_origins = {executor.submit(process_nct, n, API_KEY, API_PWD): n for n in NCT[0:20000]}
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
Start = pd.to_datetime(df2['DateStart']) 
End = pd.to_datetime(df2['DateEnd'])

df2['TrialDuration'] = (((End - Start).dt.days)/30).round(2).astype(str) + " months"

# Exporting dataframe to Excel file
df2.to_excel("**********NCTFinal_Corrected.xlsx")

print("Done!!")
