# -*- coding: utf-8 -*-
"""
Created on Sat May 23 16:04:16 2020

@author: Damiano
"""
import requests
import json
import re

def getMethods(x):
    methods = [method_name for method_name in dir(x) if callable(getattr(x, method_name))]
    return(methods)

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
def subsetDictMongoStructure(dictQueryFromDashboard, dictMongoStructure, discardTimeVariantFields = True):
    requestedKeys = list(dictQueryFromDashboard.keys())
    availableKeys = list(dictMongoStructure.keys())
    if not all(x in availableKeys for x in requestedKeys):
        raise Exception("Some keys in dictQueryFromDashboard are not present in dictMongoStructure")
    
    dictMongoStructureSubset = {key: dictMongoStructure[key] for key in dictQueryFromDashboard.keys()}
    
    # Add range to "value"
    for key in dictMongoStructureSubset.keys():
        dictMongoStructureSubset[key]["value"] = dictQueryFromDashboard[key]
        
    # if discardTimeVariantFields, discard fields that contain $type like "tv_"
    if discardTimeVariantFields:
        dictMongoStructureSubset = {key: dictMongoStructureSubset[key] for key in dictMongoStructureSubset.keys() 
                                    if re.search("^tv_", dictMongoStructureSubset[key]["type"]) == None}
    return(dictMongoStructureSubset)

def mongoBuildFilter(dictParamsMongoQuery):

    # Single key. Atomic filter for range  
    def getDictFilterRangeSingleKey(path_to_value, minmax):
        dictFilter = {path_to_value: {"$gte": min(minmax), "$lte": max(minmax)}}                  
        return(dictFilter)
    
    # Atomic filter for categorical  
    def getDictFilterCategoricalSingleKey(path_to_value, options):
        dictFilter = {path_to_value: {"$in": options}}                  
        return(dictFilter)
    
    # Atomic filter for bool  
    def getDictFilterBoolSingleKey(path_to_value, truefalse):
        dictFilter = {path_to_value: truefalse}                    
        return(dictFilter)
    
    # dictItem = dictParamsMongoQuery["gender"]
    def getDictFilter(dictItem):
        variableType = dictItem["type"]
        
        # Build filter for booleans
        if "bool" in variableType:
            dictFilter = getDictFilterBoolSingleKey(path_to_value=dictItem["path_to_value"], 
                                           truefalse=dictItem["value"])
        
        # Build filter for categorical
        elif "cat" in variableType:
            dictFilter = getDictFilterCategoricalSingleKey(path_to_value=dictItem["path_to_value"],
                                                  options=dictItem["value"])
        # Build filter for numeric    
        elif "num" in variableType:
            dictFilter = getDictFilterRangeSingleKey(path_to_value=dictItem["path_to_value"],
                                            minmax=dictItem["value"])            
        else: 
            raise Exception("Unknown variable type: {}".format(variableType))
            
        return(dictFilter)
            
    listFilters = [getDictFilter(dictItem) for (key, dictItem) in dictParamsMongoQuery.items()]
    
    #fullFilter = {"$elemMatch" : {"$and": listFilters}}
    # TODO: integrate $elementMatch
    fullFilter = {"$and": listFilters}
    
    return(fullFilter)




# DATA RESHAPING
def reshapeField_lab_test(list_lab_test):
    
    #lab_test = x[1]["lab_tests"][1]
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

