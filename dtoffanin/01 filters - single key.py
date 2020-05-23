# -*- coding: utf-8 -*-
"""
Created on Sat May 23 10:59:59 2020

@author: Damiano
"""
# Import
import os
import yaml

# PARAMETERS
url = 'https://backend-demo.cobig19.com/patient'

# Read yaml authentication
if ("dtoffanin" in os.getcwd()):
    pathAuth = '../user_pass.yml'
    from functions import mongoGetData
else:
    pathAuth = 'user_pass.yml'
    from dtoffanin.functions import mongoGetData
    
with open(pathAuth, 'r') as f:
     access = yaml.load(f, Loader=yaml.FullLoader)

#%%

# BODY
print(os.getcwd())
auth = (access["user"], access["password"])

# Test API
x = mongoGetData(url, auth)
if len(x) == 4:
    print("Perfect! Mongo works")
else:
    raise Exception("You fool")
    
mongoSelectList = ['height_cm']
mongoFilterDict = {'$and': [{'gender': 'female'}]}
x = mongoGetData(url, auth, mongoFilterDict, mongoSelectList)