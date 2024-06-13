import pandas as pd
import numpy as np
import openpyxl as open
import regex as re
import os
import sys
import codecs
import math
import requests
from requests.auth import HTTPDigestAuth
import urllib
import xml
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

'''
    README FIRST
	
	API_KEY and API_PWD must be populated with your API information.  In this case, API_Key is your API account user name and API_PWD is 
        the API Key provided to you by ******.

'''
#Function to access API and request html.

def getURL(url):
    """
    execute a REST call and return XML
    @param url:
    @return: XML and text message or JSON :)
    """
    response = None
    headers = {'Accept': 'application/xml'}
    #headers = {'Accept': 'application/json'}
    API_KEY = '********'
    API_PWD= '*********'
    try:
        r = requests.get(url, auth=HTTPDigestAuth(API_KEY,API_PWD), headers=headers)
    except Exception:
        return response, Exception.message
    try:
        response = r.text
        message = "success"
    except:
        if r.status_code != 200:
            message = str(r.status_code) + " Error " + r.text
        else:
            message = r.text
    return response, message


# Importing Excel file with list of project codes.

data = pd.read_excel(r'******')
NCT = data['NCT'].tolist()

#Create dataframe with all the fields to export to excel file.

NCT_web = []
    
dataf =  pd.DataFrame(NCT_web, columns=['NCT','TrialID', 'url', 'Inclusion_Criteria_text','Inclusion_Criteria_index', 'Exclusion_Criteria_text','Exclusion_Criteria_index', 'Primary_Endpoint', 'Secondary_Endpoint','Biomarkers','Disease marker',"Therapeutic effect", "Toxic effect")	

NCTd = dict()
TrialIDd = dict()
urld = dict()
incld = dict()
inclid = dict()
excld = dict()
exclid = dict()
primd = dict()
secd = dict()
biomd  = dict()
dismark1d = dict()
dismark2d = dict()
dismark3d = dict()
cont = 0

#Apply function for each of the NCT codes in the field

for n in NCT[0:2763]:
    cont = cont +1
    print("Record number:", cont)

#Function to obtain TrialID from NCT code.

    NCTL = list()
    TrialIDL = list()
    urlL = list()
    incll = list()
    incill = list()
    excll = list()
    excill = list()
    priml = list()
    secl = list()
    bioml = list()
    dismark1l = list()
    dismark2l = list()
    dismark3l = list()


    idUrl = "*******************************************" + str(n)
    
    unicodeRecordResponse = getURL(idUrl)
    if unicodeRecordResponse[1] == 'success':
        context = ET.ElementTree(ET.fromstring(unicodeRecordResponse[0].encode('utf-8')))
        for elem in context.iterfind('SearchResults/Trial'):
            TrialID = elem.attrib['Id']

            NCTL.append(n)
            NCTd[n] = NCTL

            urlL.append(idUrl)
            urld[n] = urlL

            TrialIDL.append(TrialID)
            TrialIDd[n] = TrialIDL
        
        
            #Once we get the TrialID we can go to the html to get the fields from cortellis.
            
            idUrl = ************************************************
            unicodeRecordResponse = getURL(idUrl)
            if unicodeRecordResponse[1] == 'success':
                context = ET.ElementTree(ET.fromstring(unicodeRecordResponse[0].encode('utf-8')))

                #Gettin inclusion/exclusion criteria text:
                inc = ""
                for elem in context.iterfind('Trial/CriteriaInclusion'):
                    if elem in context.iterfind('Trial/CriteriaInclusion'):
                        inc = elem.text
                    else:
                        inc = "Not found"

                incll.append(str(inc))
                incld[n] = incll

                exc = ""
                for elem in context.iterfind('Trial/CriteriaExclusion'):
                    if elem in context.iterfind('Trial/CriteriaExclusion'):
                        exc = elem.text
                    else:
                        exc = "Not found"

                excll.append(str(exc))
                excld[n] = excll

                #Getting inclusion/exclusion criteria index:
    
                i = 0
                for elem in context.iterfind('Trial/EligibilityCriteriaTerms/InclusionCriteria/Inclusion/Criterion'):
                    if elem in context.iterfind('Trial/EligibilityCriteriaTerms/InclusionCriteria/Inclusion/Criterion'):
                        i = i+1
                    else:
                        i = i
                ini = i
                incill.append(ini)
                inclid[n] = incill

                e = 0
                for elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                    if elem in context.iterfind('Trial/EligibilityCriteriaTerms/ExclusionCriteria/Exclusion/Criterion'):
                        e = e+1
                    else:
                        e = e
                ene = e
                excill.append(ene)
                exclid[n] = excill

                #Gettin the number of primary and secondary endpoints:

                p = 0
                for elem in context.iterfind('Trial/MeasuresOutcome/MeasuresPrimary/Measure/Description'):
                    if elem in context.iterfind('Trial/MeasuresOutcome/MeasuresPrimary/Measure/Description'):
                        p = p+1
                        #print('Number of primary endpoints:', p)
                    else:
                        p = p
                prim = p
                priml.append(prim)
                primd[n] = priml

                s = 0
                for elem in context.iterfind('Trial/MeasuresOutcome/MeasureSecondary/Measure/Description'):
                    if elem in context.iterfind('Trial/MeasuresOutcome/MeasureSecondary/Measure/Description'):
                        s = s+1
                        #print('Number of secondary endpoints:', s)
                    else:
                        s = s
                sec = s
                secl.append(sec)
                secd[n] = secl
                
                #Getting the number of biomarkers:
                bm = 0
                for elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                    if elem in context.iterfind('Trial/BiomarkerNames/BiomarkerName'):
                        bm = bm+1
                        #print("Number of biomarkers:", bm)
                    else:
                        bm = bm
                biom = bm
                bioml.append(bm)
                biomd[n] = bioml
            
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
                dismark1l.append(d1)
                dismark1d[n] = dismark1l
                dismark2l.append(d2)
                dismark2d[n] = dismark2l
                dismark3l.append(d3)
                dismark3d[n] = dismark3l                

    else:
        NCTL.append(n)
        NCTd[n] = NCTL
        TrialIDL.append("Not found")
        TrialIDd[n] = TrialIDL
        urlL.append("Not found")
        urld[n] = urlL
        incll.append("Not found")
        incld[n] = incll
        excll.append("Not found")
        excld[n] = excll
        priml.append("Not found")
        primd[n] = priml
        secl.append("Not found")
        secd[n] = secl
        bioml.append("Not found")
        biomd[n] = bioml
        dismark1l.append("Not found")
        dismark1d[n] = dismark1l
        dismark2l.append("Not found")
        dismark2d[n] = dismark2l
        dismark3l.append("Not found")
        dismark3d[n] = dismark3l

        print('error'+unicodeResponse[1])

# Append results to the initial DataFrame

#df2 = pd.DataFrame(columns=['NCT','url'])
#df3 = pd.DataFrame(columns=['TrialID', 'Inclusion_Criteria', 'Exclusion_Criteria', 'Primary_Endpoint', 'Secondary_Endpoint','Biomarkers'])
#A = data['NCT']
df2 = dataf
A = list(NCTd.values())
B = list(TrialIDd.values())
C = list(urld.values())
D = list(incld.values())
E = list(inclid.values())
F = list(excld.values())
G = list(exclid.values())
H = list(primd.values())
I = list(secd.values())
J = list(biomd.values())
K = list(dismark1d.values())
L = list(dismark2d.values())
M = list(dismark3d.values())

df2['NCT'] = A
df2['TrialID'] = B
df2['url'] = C
df2['Inclusion_Criteria_text'] = D
df2['Inclusion_Criteria_index'] = E
df2['Exclusion_Criteria_text'] = F
df2['Exclusion_Criteria_index'] = G
df2['Primary_Endpoint'] = H
df2['Secondary_Endpoint'] = I
df2['Biomarkers'] = J
df2['Disease marker'] = K
df2['Therapeutic effect'] = L
df2['Toxic effect'] = M

# Exporting dataframe to Excel file

df2.to_excel("C:/Users/Usuari/Desktop/NCT_Final.xlsx")




