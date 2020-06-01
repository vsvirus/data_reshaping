# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:59:59 2020

@author: Damiano
"""
# Import
import os
import yaml
import json
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
                          "clinical_updates.blood_pressure_diastolic": [10.0, 180.0], 
                          "gender": ["female"]}

# Get DB structure
dictMongoStructure = getDictMongoStructure(FILE_CHOICES)

# Subset DB structure and get only fields that are relevant for filters
dictParamsMongoQuery = subsetDictMongoStructure(dictQueryFromDashboard, dictMongoStructure)

def mongoBuildFilter(dictParamsMongoQuery):

    # Atomic filter for range  
    def getDictFilterRange(path_to_value, minmax):
        dictFilter = {path_to_value: {"$gte": min(minmax), "$lte": max(minmax)}}                  
        return(dictFilter)
    
    # Atomic filter for categorical  
    def getDictFilterCategorical(path_to_value, options):
        dictFilter = {path_to_value: {"$in": options}}                  
        return(dictFilter)
    
    # Atomic filter for bool  
    def getDictFilterBool(path_to_value, truefalse):
        dictFilter = {path_to_value: truefalse}                    
        return(dictFilter)
    
    # dictItem = dictParamsMongoQuery["gender"]
    def getDictFilter(dictItem):
        variableType = dictItem["type"]
        
        if "bool" in variableType:
            dictFilter = getDictFilterBool(path_to_value=dictItem["path_to_value"], 
                                           truefalse=dictItem["value"])
            
        elif "cat" in variableType:
            dictFilter = getDictFilterCategorical(path_to_value=dictItem["path_to_value"],
                                                  options=dictItem["value"])
            
        elif "num" in variableType:
            dictFilter = getDictFilterRange(path_to_value=dictItem["path_to_value"],
                                            minmax=dictItem["value"])            
        else: 
            raise Exception("Unknown variable type: {}".format(variableType))
            
        return(dictFilter)
            
    listFilters = [getDictFilter(dictItem) for (key, dictItem) in dictParamsMongoQuery.items()]
    
    #fullFilter = {"$elemMatch" : {"$and": listFilters}}
    # TODO: integrate $elementMatch
    fullFilter = {"$and": listFilters}
    
    return(fullFilter)

myFilter = mongoBuildFilter(dictParamsMongoQuery)
x = mongoGetData(url, auth, mongoFilterDict = myFilter, mongoSelectList = [])

