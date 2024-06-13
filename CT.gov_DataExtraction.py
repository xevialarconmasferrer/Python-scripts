# Importing packages

import pandas as pd
import numpy as np
import openpyxl as open
import regex as re
import requests
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Importing Excel file with list of project codes.

data = pd.read_excel(r'C:\Users\Desktop\NCT.xlsx')
NCT = data['TrialRegistryID'].tolist()

# Creating URL adress for each Project

NCT_web = []

for i in NCT:
    NCT_web.append([i,f"https://xxxxxxxx.xxx/ct2/show/{i}?id={i}&draw=2&rank=1"])
df = pd.DataFrame(NCT_web, columns=['TrialRegistryID', "url"])


# Open URL for each Projects

Indication = dict()
Indication_names = dict()
Pr_Endpoints=dict()
All_Endpoints=dict()
Secondary_Endpoints=dict()
Exp_cohort=dict()

for i in df["url"]:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(i)
    
    # Number of Indications
    indication = list()
    content = driver.page_source
    soup = BeautifulSoup(content)
    for f in soup.findAll("div",attrs={'id':"tab-body"}):
        for x in f.findAll("div",attrs={'class':'tr-indent2'}):
            for y in x.findAll("div",attrs={'class':'tr-indent1'}):
                for z in y.findAll("div",attrs={'class':'tr-indent2'}):
                    for a in z.findAll("table",attrs={'class':'ct-data_table tr-data_table'}):
                        for b in a.findAll("td",attrs={'class':'ct-body3'}):
                            for c in b.findAll("span"):
                                for d in c:  
                                    indication.append(str(d))
                            break
   
    Indication_names[i] = indication
    Indication[i] = len(indication)
    
    # Number of Primary endpoints
    
    Pr = list()
    for m in soup.findAll("div",attrs={'id':"tab-body"}):
        for x in m.findAll("div",attrs={'class':'tr-indent2'}):
            for y in x.findAll("div",attrs={'class':'tr-indent3'}):
                for d in y.findAll("div",attrs={'class':'ct-body3'}):
                    for c in d.findAll("ol"):
                        for f in d.findAll("li"): 
                            Pr.append(str(f))                
                    break
    
    Pr_Endpoints[i] = len(Pr)
    

    # Secondary and total endpoints

    all_end =list()
    for m in soup.findAll("div",attrs={'id':"tab-body"}):
        for x in m.findAll("div",attrs={'class':'tr-indent2'}):
            for y in x.findAll("div",attrs={'class':'tr-indent3'}):
                for d in y.findAll("div",attrs={'class':'ct-body3'}):
                    for f in d.findAll("li"): 
                        all_end.append(str(f)) 

    All_Endpoints[i] = len(all_end)
    Secondary_Endpoints[i] = len(all_end) -   Pr_Endpoints[i]
    
    # Ocurrences of "Expansion cohort"

    Exp_cohort[i] = len(re.findall(r'(?i)expansion cohort|cohort expansion', requests.get(i).text))
    
    
    
# Append results to the initial DataFrame

df2 = df
Indication_Names = list(Indication_names.values())
Ind = list(Indication.values())
Pr_End = list(Pr_Endpoints.values())
Sr_End = list(Secondary_Endpoints.values())
All_End = list(All_Endpoints.values())   

df2['Number of indications'] = Ind
df2['Indications'] = Indication_Names
df2['Primary endpoints'] = Pr_End
df2['Secondary endpoints'] = Sr_End
df2['All endpoints'] = All_End

# Exporting dataframe to Excel file

df2.to_excel("C:/Users/Desktop/NCT2.xlsx")
