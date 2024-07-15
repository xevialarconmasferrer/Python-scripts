import openpyxl
import numpy as np
import datetime
import pandas as pd
import os
import glob
import re

## Import  files from a folder:


# Ask the user for the location path of the files.

def Read_multipleFiles ():


    file_path = input('Enter a file path: ')
    file_type = input('Define a file type (Excel, csv): ')


    # Use os to get all the  files in the folder

    if file_type.lower() == "excel":

        if os.path.exists(file_path):


            files_xlsx = glob.glob(os.path.join(file_path, "*.xlsx"))

            df = []

            # Loop over list of files to append to empty dataframe:

            df = pd.concat((pd.read_excel(f) for f in files_xlsx), ignore_index=True)

            df.fillna('EMPTY', inplace=True)


            #Erase duplicates in the dataframe.

            Datos = df.drop_duplicates(keep="first")

            Dup = len(df) - len(Datos)

            print(Dup,"duplicates removed")

            Datos.to_excel(file_path + "\DD.xlsx", index= False) 

            if len(files_xlsx) == 1:

                print("There is", len(files_xlsx),"file in the folder")

            else:

                print("There are", len(files_xlsx),"files in the folder")

        else:
            print('The specified file path does NOT exist')

        print(files_xlsx)

    elif file_type.lower == "csv":
        
        
        if os.path.exists(file_path):

            files_csv = glob.glob(os.path.join(file_path, "*.csv"))


            df = []


            # Loop over list of files to append to empty dataframe:

            df = pd.concat((pd.read_csv(f,sheet_name= "Results") for f in files_csv), ignore_index=True)

            df.fillna('EMPTY', inplace=True)


            #Erase duplicates in the dataframe.

            Datos = df.drop_duplicates(keep="first")

            Dup = len(df) - len(Datos)

            print(Dup,"duplicates removed")

            Datos.to_csv(file_path + "\DD.xlsx", index= False) 

            if len(files_csv) == 1:

                print("There is", len(files_csv),"file in the folder")

            else:

                print("There are", len(files_csv),"files in the folder")

        else:
            print('The specified file path does NOT exist')

        print(files_csv)
        
    
    ## Exporting dataframe in an excel file:


    # Export the dataframe in an excel file at the same location path where we got the files.

 

Read_multipleFiles ()


def Cortellis_ATCtagging():

    file_path = input("Enter a file path with your files: ")

    Datos = pd.read_excel(file_path + "\DD.xlsx")

    # Iteration through each row on the dataframe and appending to each list the right tag for "Type of active substance" and "Category" for each drug.

    Type = []
    Size =[]

    # For loop to iterate through the columns of interest in the data frame

    for colums,rows in Datos.iterrows():

        if "center" in str(rows["Company Name"]).lower() or "centre" in str(rows["Company Name"]).lower()  or "zentrum" in str(rows["Company Name"]).lower() or re.search("institut", str(rows["Company Name"]).lower())  or "istituto" in str(rows["Company Name"]).lower():
            
            Type.append("Other")
            
            if "Large" in str(rows["Organization Type"]):

                Size.append("Large")

            elif "Medium" in str(rows["Organization Type"]):

                Size.append("Medium")

            elif "Mega" in str(rows["Organization Type"]):

                Size.append("Mega")

            elif "Small" in str(rows["Organization Type"]):

                Size.append("Small")

            elif "Micro" in str(rows["Organization Type"]):

                Size.append("Micro")

            else:

                Size.append("Other")
            
        elif re.search("universit", str(rows["Company Name"]).lower()) or "hospital" in str(rows["Company Name"]).lower()  or "foundation" in str(rows["Company Name"]).lower() :

            Type.append("Working")
            
            if "Large" in str(rows["Organization Type"]):

                Size.append("Large")

            elif "Medium" in str(rows["Organization Type"]):

                Size.append("Medium")

            elif "Mega" in str(rows["Organization Type"]):

                Size.append("Mega")

            elif "Small" in str(rows["Organization Type"]):

                Size.append("Small")

            elif "Micro" in str(rows["Organization Type"]):

                Size.append("Micro")

            else:

                Size.append("Other")
            
        elif re.search("company", str(rows["Organization Type"]).lower()):

            if "Academic/Research" in str(rows["Field of Activity"]) or "Not for Profit" in str(rows["Field of Activity"]) or "Government Agency" in str(rows["Field of Activity"]):

                Type.append("Non-profit")

                if "Large" in str(rows["Organization Type"]):

                    Size.append("Large")

                elif "Medium" in str(rows["Organization Type"]):

                    Size.append("Medium")

                elif "Mega" in str(rows["Organization Type"]):

                    Size.append("Mega")

                elif "Small" in str(rows["Organization Type"]):

                    Size.append("Small")

                elif "Micro" in str(rows["Organization Type"]):

                    Size.append("Micro")

                else:

                    Size.append("Other")
            
            else:

                Type.append("Profit")

                if "Large" in str(rows["Organization Type"]):

                    Size.append("Large")

                elif "Medium" in str(rows["Organization Type"]):

                    Size.append("Medium")

                elif "Mega" in str(rows["Organization Type"]):

                    Size.append("Mega")

                elif "Small" in str(rows["Organization Type"]):

                    Size.append("Small")

                elif "Micro" in str(rows["Organization Type"]):

                    Size.append("Micro")

                else:

                    Size.append("Other")

        elif "Other" in str(rows["Organization Type"]):

            if "Academic/Research" in str(rows["Field of Activity"]) or "Not for Profit" in str(rows["Field of Activity"]) or "Government Agency" in str(rows["Field of Activity"]):

                Type.append("Non-profit")

                if "Large" in str(rows["Organization Type"]):

                    Size.append("Large")

                elif "Medium" in str(rows["Organization Type"]):

                    Size.append("Medium")

                elif "Mega" in str(rows["Organization Type"]):

                    Size.append("Mega")

                elif "Small" in str(rows["Organization Type"]):

                    Size.append("Small")

                elif "Micro" in str(rows["Organization Type"]):

                    Size.append("Micro")
                else:

                    Size.append("Other")
            
            else:

                Type.append("Other")

                if "Large" in str(rows["Organization Type"]):

                    Size.append("Large")

                elif "Medium" in str(rows["Organization Type"]):

                    Size.append("Medium")

                elif "Mega" in str(rows["Organization Type"]):

                    Size.append("Mega")

                elif "Small" in str(rows["Organization Type"]):

                    Size.append("Small")

                elif "Micro" in str(rows["Organization Type"]):

                    Size.append("Micro")
                
                else:

                    Size.append("Other")
        
        elif "Non-Profit" in str(rows["Organization Type"]) or "Academic" in str(rows["Organization Type"]): 
            
            Type.append("Non-profit")

            if "Large" in str(rows["Organization Type"]):

                Size.append("Large")

            elif "Medium" in str(rows["Organization Type"]):

                Size.append("Medium")

            elif "Mega" in str(rows["Organization Type"]):

                Size.append("Mega")

            elif "Small" in str(rows["Organization Type"]):

                Size.append("Small")

            elif "Micro" in str(rows["Organization Type"]):

                Size.append("Micro")
                
            else:

                Size.append("Other")
        
        else:

            Size.append("Other")
            Type.append("Other")
            
    Datos["Company Type"] = Type
    Datos["Company Size"] = Size
    Datos.replace('EMPTY',"", inplace=True)

    ## Exporting dataframe in an excel file:


    # Export the dataframe in an excel file at the same location path where we got the files.

    Datos.to_excel(file_path + "\CompanytagsTest.xlsx", index= False) 
    

Cortellis_ATCtagging()
