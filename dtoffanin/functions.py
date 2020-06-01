# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:04:16 2020

@author: Damiano
"""
import requests
import json

def mongoGetData(url, auth, mongoFilterDict={'$and': [{'gender': 'female'}]}, mongoSelectList=['height_cm']):
    
    filter_MongoDB = json.dumps(mongoFilterDict, separators=(',',':'))
    select_MongoDB = json.dumps(mongoSelectList, separators=(',',':'))
    
    payload = {"filter": filter_MongoDB, 
           "select": select_MongoDB}

    data_connection = requests.get(url, auth=auth, params=payload)
    if data_connection.status_code == 200:
        patients = data_connection.json()
    else:
        raise Exception(data_connection.status_code)
    return patients

def mongoTest(url, auth):
    x = mongoGetData(url, auth)
    if len(x) == 4:
        print("Perfect! Mongo works")
    else:
        raise Exception("You fool")
        
def getDictMongoStructure(path):
    import json
    with open(path) as f:
      data = json.load(f)
    return(data)

# Subset dictMongoStructure
def subsetDictMongoStructure(dictQueryFromDashboard, dictMongoStructure):
    requestedKeys = list(dictQueryFromDashboard.keys())
    availableKeys = list(dictMongoStructure.keys())
    if not all(x in availableKeys for x in requestedKeys):
        raise Exception("Some keys in dictQueryFromDashboard are not present in dictMongoStructure")
    
    dictMongoStructureSubset = {key: dictMongoStructure[key] for key in dictQueryFromDashboard.keys()}
    for key in dictMongoStructureSubset.keys():
        dictMongoStructureSubset[key]["value"] = dictQueryFromDashboard[key]
        
    return(dictMongoStructureSubset)
