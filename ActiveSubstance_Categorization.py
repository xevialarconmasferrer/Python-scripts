import pandas as pd
import re

def load_data(file_path):
    return pd.read_excel(file_path)

def categorize_technologies(rows):
    technologies = str(rows["Technologies"]) if pd.notnull(rows["Technologies"]) else ""
    other_actions = str(rows["Other Actions"]) if pd.notnull(rows["Other Actions"]) else ""
    concat = technologies + "; " + other_actions
    concat_lower = concat.lower()
    
    if "small molecule therapeutic" in technologies.lower():
        if "adjuvant" in other_actions.lower():
            return "Small molecule", "Adjuvant", "Non"
        return "Small molecule", "Non", "Non"
    
    elif "vaccine" in technologies.lower() or "vaccine" in other_actions.lower():
        if "therapeutic vaccine" in concat_lower and "prophylactic vaccine" in concat_lower:
            return "Biologic", "Vaccine", "Both"
        if "therapeutic vaccine" in concat_lower:
            return "Biologic", "Vaccine", "Therapeutic vaccine"
        if "prophylactic vaccine" in concat_lower:
            return "Biologic", "Vaccine", "Prophylactic vaccine"
        return "Biologic", "Vaccine", "Other"
    
    elif "biological therapeutic" in technologies.lower() or "biologic" in concat_lower: 
        if any(term in concat_lower for term in ["gene therapy", "gene editing", "gene technology"]):
            return "Biologic", "Gene therapy", "Non"
        elif "cell therapy" in concat_lower:
            return "Biologic", "Cell therapy", "Non"
        elif any(term in concat_lower for term in ["oligonucleotide","antisense"]) or any (term in  concat for term in ["RNA", "siRNA"]):
            return "Biologic", "Oligonucleotide", "Non"
        elif "antibody drug conjugate" in concat_lower:
            return "Biologic", "Antibody-drug Conjugated", "Non"
        elif re.search("antibody", technologies.lower()):
            return "Biologic", "Antibody", "Non"
        elif any(re.search(term, concat_lower) for term in ["protein", "enzym","glycoprotein", "lipoprotein"]):
            return "Biologic", "Therapeutic protein", "Non"
        elif "peptide" in technologies.lower() or "peptide" in other_actions.lower():
            return "Biologic", "Peptide", "Non"
        elif any(term in concat_lower for term in ["vector expression", "virus recombinant", "virus therapy", "bacteria recombinant"]):
            return "Biologic", "Vector", "Non"
        elif "adjuvant" in other_actions.lower():
            return "Biologic", "Adjuvant", "Non"
        return "Biologic", "Other", "Non"
    
    else:  

        if any(term in concat_lower for term in ["gene therapy", "gene editing", "gene technology"]):
            return "Biologic", "Gene therapy", "Non"
        elif "cell therapy" in concat_lower:
            return "Biologic", "Cell therapy", "Non"
        elif any(term in concat_lower for term in ["oligonucleotide","antisense"]) or any (term in  concat for term in ["RNA", "siRNA"]):
            return "Biologic", "Oligonucleotide", "Non"
        elif "antibody drug conjugate" in concat_lower:
            return "Biologic", "Antibody-drug Conjugated", "Non"
        elif re.search("antibody", technologies.lower()):
            return "Biologic", "Antibody", "Non"
        elif any(re.search(term, concat_lower) for term in ["protein", "enzym","glycoprotein", "lipoprotein"]):
            return "Biologic", "Therapeutic protein", "Non"
        elif "peptide" in technologies.lower() or "peptide" in other_actions.lower():
            return "Biologic", "Peptide", "Non"
        elif any(term in concat_lower for term in ["vector expression", "virus recombinant", "virus therapy", "bacteria recombinant"]):
            return "Biologic", "Vector", "Non"
        elif "adjuvant" in other_actions.lower():
            return "Biologic", "Adjuvant", "Non"
        return "Other", "Other", "Non"


def categorize_data(df):
    
    intervention_type = []
    biologic_type = []
    vaccine_type = []

    for _, rows in df.iterrows():
        it, bt, vt = categorize_technologies(rows)
        intervention_type.append(it)
        biologic_type.append(bt)
        vaccine_type.append(vt)
    
    df["Intervention type"] = intervention_type
    df["Biologic_type"] = biologic_type
    df["Vaccine_type"] = vaccine_type

    return df

def save_data(df, output_path):
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    input_path = r"****.xlsx"
    output_path = r"***.xlsx"
    
    data = load_data(input_path)
    data = categorize_data(data)
    save_data(data, output_path)
