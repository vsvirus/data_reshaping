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