# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:59:59 2020

@author: Damiano
"""
# Import
import os
import yaml
import json
import pandas as pd
from dfply import *
import functools

print(os.getcwd())

# PARAMETERS
url = 'https://backend-demo.cobig19.com/patient'
DB_SELECT_ALL = []
DB_FILTER_ALL = {}

# Read yaml authentication
if ("dtoffanin" in os.getcwd()):
    pathAuth = '../user_pass.yml'
    from functions import *
    FILE_CHOICES = "choices.json"

else:
    pathAuth = 'user_pass.yml'
    from dtoffanin.functions import *
    FILE_CHOICES = "dtoffanin/choices.json"
    
with open(pathAuth, 'r') as f:
     access = yaml.load(f, Loader=yaml.FullLoader)

#%%

# BODY
print(os.getcwd())
auth = (access["user"], access["password"])

# Test API
mongoTest(url, auth)

dictQueryFromDashboard = {#"radiological_tests.has_pneumonia": [True], 
                          "clinical_updates.blood_pressure_diastolic": [10.0, 180.0], # Single key
                          # Element match is necessary here: you want to keep the lab test that had simultaneously hemoglobine and hematocrit within filters.
                          # "lab_tests.hemoglobine_value": [20.0, 150.0], # Double key 
                          # "lab_tests.hematocric_value": [10.0, 100.0], #Double key
                          "gender": ["female"]}


# path_to_value = "lab_tests.items.value"
# condition = "lab_tests.items.name==hemoglobine"
# path_to_timestamp = "lab_tests.timestamp"
# minmax = [20.0, 150.0]

# Get DB structure
dictMongoStructure = getDictMongoStructure(FILE_CHOICES)

# Get queries from dashboard
dictQueryFromDashboard = {#"radiological_tests.has_pneumonia": [True], 
                          "clinical_updates.blood_pressure_diastolic": [10.0, 180.0], # Single key
                          # Element match is necessary here: you want to keep the lab test that had simultaneously hemoglobine and hematocrit within filters.
                          # "lab_tests.hemoglobine_value": [20.0, 150.0], # Double key 
                          # "lab_tests.hematocric_value": [10.0, 100.0], #Double key
                         
                          "gender": ["female"]}


# Subset DB structure and get only fields that are relevant for filters
dictParamsMongoQuery = subsetDictMongoStructure(dictQueryFromDashboard, dictMongoStructure, discardTimeVariantFields = True)

myFilter = mongoBuildFilter(dictParamsMongoQuery)


# Naïve version: keep all patients that fulfill all criteria at least once, not necessarily at the same time. 
# No time sinchronicity enforced. Little meaning. "Show me the emoglobine (when?) of a patient that had (when?) a blood pressure within [P1, P2]
# Decision: for version 1.0 only filter by time constant.

x = mongoGetData(url, auth, mongoFilterDict = myFilter, mongoSelectList = [])
x = mongoGetData(url, auth, mongoFilterDict = myFilter, 
                 mongoSelectList = ["clinical_updates", "lab_tests", "patient_id"])

list_lab_test = x[1]["lab_tests"]


def reshapeField_lab_test(list_lab_test):
    
    lab_test = x[1]["lab_tests"][1]
    def reshape_lab_test_single(lab_test):
        df = pd.DataFrame(lab_test["items"])
        df["timestamp"] = lab_test["timestamp"]
        return(df)

    list_df_lab_tests = [reshape_lab_test_single(lab_test = x) for x in list_lab_test]
    df_lab_tests = pd.concat(list_df_lab_tests)
    
    dfReturn = (df_lab_tests >> 
     rename(variable=X.parameter_key) >> 
     select(["variable", "timestamp", "value", "is_out_of_bounds"]))
    
    return(dfReturn)

list_items = x[1]["clinical_updates"]
def reshape_itemsWithTimestamp(list_items):
    
    item = list_items[1]
    def reshape_item(item):
        timestamp = item["timestamp"]
        dictReturn = { key:{timestamp:value} for key, value in item.items() if type(value) != list and key!="timestamp"}
        return(dictReturn)
    
    listOfDict = [reshape_item(item) for item in list_items]
    
    json.dump(listOfDict)
    
    allVariables = functools.reduce(set.union, [set(D.keys()) for D in listOfDict])
    
    v = {k: [dic[k] for dic in listOfDict if k in dic] for k in allKeys}
    
    {list(listOfDict[0]["_id"].values())[0]:element["heart_rate"] for element in listOfDict} for key in allKeys 
    
    
    {variable:
     {list(element["_id"].values())[0]:
      {element[key] for element in listOfDict}} for variable in allVariables}
    
   {variable: {
		list(element['_id'].values())[0]: element[variable]
		for element in listOfDict
	}
	for variable in allVariables}
        
   {variable: {
		list(element['_id'].values())[0]: {**element[variable], }
		for element in listOfDict
	}
	for variable in allVariables}
   
   
    list(listOfDict[0]["_id"].values())[0]
    
   {"12:01":[3,2], "12:01":[6,2]}
   a = {3}
   
   [1,2,3]
   
   a = {"A":1, "B":2}
   b = {"C":3, "D":4}
   
   {**a, **b}
   
   xx = v["_id"]
   dic = xx[1]
   for key,value in dic.items():
       print({key:value})
   
   [[{key:value} for key,value in dic] for dic in xx]
    
    return(dfReturn)

for index, patient in dat.iterrows():


# Transpose

print(listOfDict)
def reshape_lab_tests(dict_lab_tests):
    









dictParamsMongoQuery.keys()










