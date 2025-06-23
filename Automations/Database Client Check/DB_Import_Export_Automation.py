#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:





# # Global Configs

# In[ ]:


output_folder = r"Your Path Here"

date_range = "5.1.25-5.31.25"


# In[ ]:





# # Mappings

# In[ ]:


## Keep in dictionary format (i.e. {Male: 1, Female:2, ...}

service_id_map = {
    "Your Map Here"
}

funding_id_map = {
    "Your Map Here"
}

program_definition_id_map = {
    "Your Map Here"
}

family_type_map = {
    "Your Map Here"
}

ethnicity_map = {
    "Your Map Here"
}

race_id_map = {
    "Your Map Here"
}

gender_id_map = {
    "Your Map Here"
}


language_code_id_map = {
   "Your Map Here"
}


# In[ ]:





# # Functions

# In[ ]:


def map_column(df, source_col, target_col, mapping_dict, default_value):
    """Map a column based on a dictionary, with a default fallback."""
    df[target_col] = df[source_col].apply(lambda x: mapping_dict.get(str(x).strip(), default_value))
    return df

def compute_service_id(program_text, service_id_map):
    txt = str(program_text).upper()

    if "Fund 1" in txt:
        return service_id_map.get("Fund 1", "")
    elif "Fund 2" in txt and "Fund 3" not in txt:
        return service_id_map.get("Fund 2", "")
    elif "Fund 3" in txt and "Fund 2" not in txt:
        return service_id_map.get("Fund 3", "")
    else:
        return ""

def get_invalid_ssn(df, ssn_column):
    ssn_clean = df[ssn_column].astype(str).str.strip()
    invalid_mask = ~ssn_clean.str.match(r"^\d{9}$")
    return df[invalid_mask]

def check_row_count(df1, df2, import_df):
    total = df1.shape[0] + df2.shape[0]
    expected = import_df.shape[0]
    if total == expected:
        print(f"Row count matches: {total}")
    else:
        print(f"Mismatch! Import rows: {expected}, Combined: {total}")

def export_to_excel(df, path):
    df.to_excel(path, index=False)


# In[ ]:





# # Input Files

# ## Original File

# In[ ]:


try:
    Import = pd.read_excel("Your File Here", dtype={'SSN': str})
except FileNotFoundError:
    print("This file is not valid")

Import["AreaCode"] = Import["AreaCode"].astype("Int64")
Import["Phone"] = Import["Phone"].astype("Int64")

Import["IntakeDate"] = pd.to_datetime(Import["IntakeDate"], errors="coerce")
Import["IntakeDate"] = Import["IntakeDate"].dt.strftime("%m/%d/%Y")

Import["ApplicationTransferDate"] = pd.to_datetime(Import["ApplicationTransferDate"], errors="coerce")
Import["ApplicationTransferDate"] = Import["ApplicationTransferDate"].dt.strftime("%m/%d/%Y")

Import["TotalPaymentTotal"] = Import["TotalPaymentTotal"].apply(
    lambda x: "${:,.2f}".format(x) if pd.notnull(x) else ""
)

Import["TotalMonthlyIncome"] = Import["TotalMonthlyIncome"].apply(
    lambda x: "${:,.2f}".format(x) if pd.notnull(x) else ""
)

Import.head()


# In[ ]:





# ## Full List from Database

# In[ ]:


try:
    All_Persons_Case = pd.read_excel("Your File Here")
except FileNotFoundError:
    print("This file is not valid")

All_Persons_Case.drop(All_Persons_Case.columns[3], axis=1, inplace=True)

All_Persons_Case["idDesiredCenter"] = All_Persons_Case["idDesiredCenter"].astype("Int64")
All_Persons_Case["gender"] = All_Persons_Case["gender"].astype("Int64")
All_Persons_Case["#Case"] = All_Persons_Case["#Case"].astype("Int64")
All_Persons_Case["idDesiredCenter"] = All_Persons_Case["idDesiredCenter"].astype("string").fillna("")
All_Persons_Case["gender"] = All_Persons_Case["gender"].astype("string").fillna("")
All_Persons_Case["#Case"] = All_Persons_Case["#Case"].astype("string").fillna("")
All_Persons_Case.fillna("", inplace=True)

All_Persons_Case["birthdate"] = pd.to_datetime(All_Persons_Case["birthdate"], errors="coerce")
All_Persons_Case["birthdate"] = All_Persons_Case["birthdate"].dt.strftime("%m/%d/%Y")

columns_to_insert = [
    (7, ["BD", "Gender", "Combined NBDG"]),
    (11, ["SSN No dash", "personID"])
]

for insert_index, new_cols in columns_to_insert:
    for i, col_name in enumerate(new_cols):
        All_Persons_Case.insert(loc=insert_index + i, column=col_name, value="")

All_Persons_Case["BD"] = All_Persons_Case["birthdate"].astype("string")

gender_map = {
    '2': "female",
    '1': "male",
    '3': "Data not Collected"
}

All_Persons_Case["Gender"] = All_Persons_Case["gender"].map(gender_map).fillna("blank")

All_Persons_Case["Combined NBDG"] = (
    All_Persons_Case["firstName"].fillna("").astype(str) + " " +
    All_Persons_Case["lastName"].fillna("").astype(str) + " " +
    All_Persons_Case["BD"].fillna("").astype(str) + " " +
    All_Persons_Case["Gender"].fillna("").astype(str)
)

All_Persons_Case["SSN No dash"] = All_Persons_Case["SSN"].astype(str).str.replace("-", "", regex=False)

All_Persons_Case["personID"] = All_Persons_Case["PersonID"]

All_Persons_Case.head()


# In[ ]:





# ## List from database for relevant program

# In[ ]:


try:
    Person_Case_Program_2025 = pd.read_excel("Your File Here")
except FileNotFoundError:
    print("This file is not valid")

Person_Case_Program_2025["idDesiredCenter"] = Person_Case_Program_2025["idDesiredCenter"].astype("Int64")
Person_Case_Program_2025["CaseNo"] = Person_Case_Program_2025["CaseNo"].astype("Int64")

Person_Case_Program_2025["SSN"] = Person_Case_Program_2025["SSN"].astype("string").fillna("")

Person_Case_Program_2025["birthdate"] = pd.to_datetime(Person_Case_Program_2025["birthdate"], errors="coerce")
Person_Case_Program_2025["birthdate"] = Person_Case_Program_2025["birthdate"].dt.strftime("%m/%d/%Y")

new_columns = [
    ("caseID", 0),
    ("caseNo", 1)
]

for col_name, insert_index in new_columns:
    Person_Case_Program_2025.insert(loc=insert_index, column=col_name, value="")

Person_Case_Program_2025["caseID"] = Person_Case_Program_2025["CaseID"]
Person_Case_Program_2025["caseNo"] = Person_Case_Program_2025["CaseNo"]

Person_Case_Program_2025.head()


# In[ ]:





# # Database Lookup

# In[ ]:


Name_ImportDB = Import

Name_ImportDB["SSN"] = Name_ImportDB["SSN"].astype("string").fillna("")

Name_ImportDB["DateOfBirth"] = pd.to_datetime(Name_ImportDB["DateOfBirth"], errors="coerce")
Name_ImportDB["DateOfBirth"] = Name_ImportDB["DateOfBirth"].dt.strftime("%m/%d/%Y")

Name_ImportDB["FamilyTypeDisplay"] = Name_ImportDB["FamilyTypeDisplay"].astype(str).str.strip()

new_columns = [
    ("Combined NBDG", 0),
    ("gender", 1),
    ("Person ID(agency in database)", 2),
    ("Program Case ID", 3)
]

for col_name, insert_index in new_columns:
    Name_ImportDB.insert(loc=insert_index, column=col_name, value="")

lookup_dict = Person_Case_Program_2025.set_index("caseID")["caseNo"].to_dict()
Name_ImportDB["Program Case ID"] = Name_ImportDB["ApplicationID"].map(lookup_dict)

lookup_dict2 = All_Persons_Case.set_index("SSN No dash")["personID"].to_dict()
Name_ImportDB["Person ID(agency in database)"] = Name_ImportDB["SSN"].map(lookup_dict2)
Name_ImportDB["Person ID(agency in database)"] = Name_ImportDB["Person ID(agency in database)"].astype("Int64")

gender_map = {
    'SELF-IDENTIFIED FEMALE': "female",
    'SELF-IDENTIFIED MALE': "male",
    'other': "Data not Collected"
}

Name_ImportDB["gender"] = Name_ImportDB["Gender"].map(gender_map).fillna("blank")

Name_ImportDB["Combined NBDG"] = (
    Name_ImportDB["FirstName"].fillna("").astype(str) + " " +
    Name_ImportDB["LastName"].fillna("").astype(str) + " " +
    Name_ImportDB["DateOfBirth"].fillna("").astype(str) + " " +
    Name_ImportDB["gender"].fillna("").astype(str)
)


# In[ ]:


# Matched: rows where "Person ID(agency in database)" is not NA
SSN_ImportDB = Name_ImportDB[Name_ImportDB["Person ID(agency in database)"].notna()].copy()

# Unmatched: rows where "Person ID(agency in database)" is NA
df_unmatched = Name_ImportDB[Name_ImportDB["Person ID(agency in database)"].isna()].copy()


# In[ ]:


num_rows = SSN_ImportDB.shape[0]
print(f"Number of rows: {num_rows}")


# In[ ]:


df_unmatched["Person ID(agency in database)"] = ""

lookup_dict3 = (
    All_Persons_Case
    .assign(Combined_NBDG_lower = All_Persons_Case["Combined NBDG"].astype(str).str.lower())
    .set_index("Combined_NBDG_lower")["personID"]
    .to_dict()
)

df_unmatched["Person ID(agency in database)"] = (
    df_unmatched["Combined NBDG"]
    .astype(str)
    .str.lower()
    .map(lookup_dict3)
)

df_unmatched["Person ID(agency in database)"] = df_unmatched["Person ID(agency in database)"].astype("Int64")


# In[ ]:


# Matched: rows where "Person ID(agency in database)" is not NA
Name_ImportDB_InDB = df_unmatched[df_unmatched["Person ID(agency in database)"].notna()].copy()

# Unmatched: rows where "Person ID(agency in database)" is NA
Name_ImportDB_NotInDB = df_unmatched[df_unmatched["Person ID(agency in database)"].isna()].copy()


# In[ ]:


num_rows = Name_ImportDB_InDB.shape[0]
print(f"Number of rows: {num_rows}")


# In[ ]:


num_rows = Name_ImportDB_NotInDB.shape[0]
print(f"Number of rows: {num_rows}")


# In[ ]:





# ## Seperate In Database Clients with not In Database Clients

# In[ ]:


# Append DataFrames
Clients_In_DB = pd.concat([SSN_ImportDB, Name_ImportDB_InDB], ignore_index=True)


# In[ ]:


Name_ImportDB_NotInDB = Name_ImportDB_NotInDB.reset_index(drop=True)


# In[ ]:





# # Finalize 'Not In Database' Export

# In[ ]:


cols_to_drop_idx = [0, 1, 2, 3, 18, 19, 20, 21, 26, 27, 28, 29, 30, 31, 32, 33, 35, 39, 41, 42, 43, 44]
cols_to_drop = Name_ImportDB_NotInDB.columns[cols_to_drop_idx]

Name_ImportDB_NotInDB = Name_ImportDB_NotInDB.drop(columns=cols_to_drop)

# Get current list of columns
cols = list(Name_ImportDB_NotInDB.columns)
# Remove "AreaCode" from current position
cols.remove("AreaCode")
# Insert "AreaCode" at position 14
cols.insert(14, "AreaCode")
# Reorder DataFrame columns
Name_ImportDB_NotInDB = Name_ImportDB_NotInDB[cols]

new_columns = [
    ("Service", 20),
    ("Service id", 21),
    ("Funding id", 24),
    ("Program Definition id", 26)
]

for col_name, insert_index in new_columns:
    Name_ImportDB_NotInDB.insert(loc=insert_index, column=col_name, value="")


# In[ ]:





# In[ ]:


###FILL IN FORMULAS###

# SERVICE COLUMN

# Make a copy of Program column uppercased
txt = Name_ImportDB_NotInDB["Program"].astype(str).str.upper()

# Define condition masks
has_serv1 = txt.str.contains("Service 1", na=False)
has_serv2 = txt.str.contains("Service 2", na=False)
has_serv3 = txt.str.contains("Service 3", na=False)
has_serv4 = txt.str.contains(r"\bService4\b", na=False)

# Apply logic
Name_ImportDB_NotInDB["Service"] = (
    np.where(has_serv3, "Service 1",
    np.where(has_serv2 & has_serv1, "Service 2",
    np.where(has_serv4 & has_serv1, "Service 3",
    np.where(has_serv4, "Service 4", ""))))
)

#SERVICE ID COLUMN

def compute_service_id(program_text, service_id_map):
    txt = str(program_text).upper()

    if "Service 1" in txt:
        return service_id_map.get("Service 1", "")
    elif "Service 4" in txt and "Service 2" not in txt:
        return service_id_map.get("Service 4_ONLY", "")
    elif "Service 2" in txt and "Service 4" not in txt:
        return service_id_map.get("Service 2", "")
    else:
        return ""

Name_ImportDB_NotInDB["Service id"] = Name_ImportDB_NotInDB["Program"].apply(
    lambda x: compute_service_id(x, service_id_map)
)

#Funding ID COLUMN

Name_ImportDB_NotInDB["Funding id"] = Name_ImportDB_NotInDB["Program"].map(funding_id_map).fillna("")

#Program Definition id COLUMN

Name_ImportDB_NotInDB["Program Definition id"] = Name_ImportDB_NotInDB["Program"].map(program_definition_id_map).fillna("")


# In[ ]:


Name_ImportDB_NotInDB = Name_ImportDB_NotInDB.rename(columns={'IntakeDate': 'CaseDateApplied', 
 'ApplicationTransferDate': 'ServiceDate',
 'TotalPaymentTotal': 'Quantity (Payment Total)', 
 'Program': 'Fund'})


# In[ ]:


Pers_Case_Serv = Name_ImportDB_NotInDB

new_columns = [
    ("Gender(ID)", 5),
    ("FamilyTypeDisplay (ID)", 7),
    ("LanguageCode (ID)", 18),
    ("Ethicity (ID)", 20),
    ("Race (ID)", 22)
]

for col_name, insert_index in new_columns:
    Pers_Case_Serv.insert(loc=insert_index, column=col_name, value="")

#GENDER ID COLUMN

map_column(Pers_Case_Serv, "Gender", "Gender(ID)", gender_id_map, 9999)

#Family Type ID COLUMN

map_column(Pers_Case_Serv, "FamilyTypeDisplay", "FamilyTypeDisplay (ID)", family_type_map, 9999)

#Language Code ID COLUMN

map_column(Pers_Case_Serv, "LanguageCode", "LanguageCode (ID)", family_type_map, "")

#Ethnicity ID COLUMN

map_column(Pers_Case_Serv, "Ethicity", "Ethicity (ID)", ethnicity_map, 2)

#Race ID COLUMN

map_column(Pers_Case_Serv, "Race", "Race (ID)", race_id_map, "")



Pers_Case_Serv = Pers_Case_Serv.drop(columns=['OverIncome'])

Pers_Case_Serv['TotalHouseholdSize'] = 1


# In[ ]:





# # Finalize 'In Database' Export

# In[ ]:


Case_Serv = Clients_In_DB[['Person ID(agency in database)', 'ApplicationID','IntakeDate',
                             'ApplicationTransferDate', 'TotalPaymentTotal', 'Program']]

new_columns = [
    ("Service", 3),
    ("Service id", 4),
    ("Funding id", 8),
    ("Program Definition id", 9)
]

for col_name, insert_index in new_columns:
    Case_Serv.insert(loc=insert_index, column=col_name, value="")


# In[ ]:


# SERVICE COLUMN

# Make a copy of Program column uppercased
txt = Case_Serv["Program"].astype(str).str.upper()

# Define condition masks
has_serv1 = txt.str.contains("Service 1", na=False)
has_serv2 = txt.str.contains("Service 2", na=False)
has_serv3 = txt.str.contains("Service 3", na=False)
has_serv4 = txt.str.contains(r"\bService4\b", na=False)

# Apply logic
Case_Serv["Service"] = (
    np.where(has_serv3, "Service 1",
    np.where(has_serv2 & has_serv1, "Service 2",
    np.where(has_serv4 & has_serv1, "Service 3",
    np.where(has_serv4, "Service 4", ""))))
)

#SERVICE ID COLUMN

Case_Serv["Service id"] = Case_Serv["Program"].apply(
    lambda x: compute_service_id(x, service_id_map)
)

#Funding ID COLUMN

Case_Serv["Funding id"] = Case_Serv["Program"].map(funding_id_map).fillna("")

#Program Definition id COLUMN

Case_Serv["Program Definition id"] = Case_Serv["Program"].map(program_definition_id_map).fillna("")


# In[ ]:


Case_Serv = Case_Serv.rename(columns={'IntakeDate': 'CaseDateApplied',
 'Person ID(agency in database)': 'databasePersonid',                                     
 'ApplicationTransferDate': 'ServcieDate',
 'TotalPaymentTotal': 'Quantity', 
 'Program': 'Fund'})


# In[ ]:





# # Final DQC

# In[ ]:


# Get invalid SSNs
invalid_ssn_df = get_invalid_ssn(Pers_Case_Serv, "SSN")

# Final row count check
check_row_count(Pers_Case_Serv, Case_Serv, Import)


# In[ ]:





# # Export

# In[ ]:


export_to_excel(Pers_Case_Serv, f"{output_folder}/Pers_Case_Serv_{date_range}.xlsx")
export_to_excel(Case_Serv, f"{output_folder}/Case_Serv_{date_range}.xlsx")


# In[ ]:





# In[ ]:




