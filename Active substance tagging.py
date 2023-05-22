import openpyxl
import numpy as np
import datetime
import pandas as pd
import os
import glob


##                                                                                  Import  files from a folder:


# Ask the user for the location path of the files.

file_path = input('Enter a file path: ')
print(file_path)

# Use os to get all the  files in the folder

if os.path.exists(file_path):

    files_xlsx = glob.glob(os.path.join(file_path, "*.xlsx"))

    if len(files_xlsx) == 1:

        print("There is", len(files_xlsx),"file in the folder")

    else:

        print("There are", len(files_xlsx),"files in the folder")

else:
    print('The specified file path does NOT exist')

print(files_xlsx)

# Creating a new dataframe to append all imported files.

df2023 = []

# Loop over list of files to append to empty dataframe:

df2023 = pd.concat((pd.read_excel(f,sheet_name= "Results") for f in files_xlsx), ignore_index=True)

df2023.fillna('EMPTY STRING IN HERE', inplace=True)

#Erase duplicates in the dataframe.

Datos = df2023.drop_duplicates(keep="first")

Dup = len(df2023) - len(Datos)

print(Dup,"duplicates removed")


##                                                                                 Conditional Tagging:


# Iteration through each row on the dataframe and appending to each list the right tag for "Type of active substance" and "Category" for each drug.

Datos["concat"] = Datos["Technologies"] + "; " + Datos["Other Actions"]

Type = []
Category =[]

# For loop to iterate through the columns of interest in the data frame

for colums,rows in Datos.iterrows():

    if "small molecule therapeutic" in str(rows["concat"]).lower() or  "small molecule therapeutic" in str(rows["Extract"]).lower():

        Type.append("Small molecule therapeutic") 
        Category.append("Other")
  
    elif "vaccine" in str(rows["concat"]).lower() or "vaccine" in str(rows["Extract"]).lower():
            
        Type.append("Biological therapeutic") 
        Category.append("Vaccine")

    elif "gene therapy" in str(rows["concat"]).lower() or "gene therapy" in str(rows["Extract"]).lower() or "gene editing" in str(rows["concat"]).lower() or "gene editing" in str(rows["Extract"]).lower() or "gene technology" in str(rows["concat"]).lower(): 
                
        Type.append("Biological therapeutic") 
        Category.append("Gene Therapy")   
                
    elif "cell therapy" in str(rows["concat"]).lower() or "cell therapy" in str(rows["Extract"]).lower():

        Type.append("Biological therapeutic") 
        Category.append("Cell Therapy")

    elif "oligo" in str(rows["concat"]).lower() or "RNA" in str(rows["concat"]) or "antisense" in str(rows["concat"]).lower():
                        
        Type.append("Biological therapeutic") 
        Category.append("Oligonucleotide")

    elif "antibody conjugated" in str(rows["concat"]).lower() or "antibody drug conjugate" in str(rows["concat"]).lower() or "conjugated antibody" in str(rows["concat"]).lower() or "antibody conjugated" in str(rows["Extract"]).lower():

        Type.append("Biological therapeutic") 
        Category.append("Antibody-drug conjugated")

    elif "antibody" in str(rows["concat"]).lower():
                                
        Type.append("Biological therapeutic") 
        Category.append("Antibody")

    elif "protein fusion" in str(rows["concat"]).lower() or "protein recombinant" in str(rows["concat"]).lower()  or "glycoprotein" in str(rows["concat"]).lower() or "protein conjugated" in str(rows["concat"]).lower() or "recombinant enzyme" in str(rows["concat"]).lower()  or "enzyme" in str(rows["concat"]).lower() or "lipoprotein" in str(rows["concat"]).lower():
                                    
        Type.append("Biological therapeutic") 
        Category.append("Therapeutic protein")
                                                  
    elif "peptide" in str(rows["concat"]).lower():
                                        
        Type.append("Biological therapeutic") 
        Category.append("Peptide")
    
    elif "biological therapeutic" in str(rows["Technologies"]).lower() or "virus recombinant" in str(rows["Technologies"]).lower() or "virus therapy" in str(rows["Technologies"]).lower() or "probiotic" in str(rows["Extract"]).lower() or "yeast recombinant" in str(rows["Technologies"]).lower()  or "bacteria recombinant" in str(rows["Technologies"]).lower() :

        Type.append("Biological therapeutic")
        Category.append("Other")
    
    elif "small molecule" in str(rows["Extract"]).lower() :

        Type.append("Small molecule therapeutic") 
        Category.append("Other") 

    else:
        
        Type.append("Other") 
        Category.append("Other")


#Datos["Type of active substance"] = Type

Datos.drop(["concat"], axis = 1, inplace = True)

Datos["Type of active substance"] = Type
Datos["Category"] = Category

Datos.replace('EMPTY STRING IN HERE',"", inplace=True)

##                                                                                 Exporting dataframe in an excel file:


# Export the dataframe in an excel file at the same location path where we got the files.

Datos.to_excel(file_path + "\2023_Cortellis_tagging_Final.xlsx", index= False) 

