# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:20:37 2020

@author: Jesús S. Alegre
"""
import json
import requests
import pandas as pd
import numpy as np
from random import randint, seed, random
seed(1)


pay = json.dumps({"ethnicity":{"$gt":0}}, separators=(',', ':'))
resp_filter = requests.get('http://localhost:3000/patient', params={"filter":pay})   

if resp_filter.status_code == 200:
    full_data= resp_filter.json()
    data = pd.DataFrame(full_data)

# Generate data for height and weight    
height = [randint(0, 200) for age in range(81)]
weight = [randint(0, 200) for age in range(81)]
data['heigth']=height
data['weigth']=weight

#Generate blood test data
lab_test = []
parametros = ['uno','dos','tres']
multipliers = [2,5,10]
for i in range(0,81): # numero de pacientes
    test_paciente = []
    for j in range(0,10): # numero de tests por paciente
        timestamp = j
        raw_text = 'nadaandanaa'
        concrete_result = []
        for k in range(0,3): # numero de parametros por test
            parameter_key = parametros[k]
            value = j*70 - 2**j + 100**random()
            multiplier = multipliers[k]*random()
            out_of_bounds = False
            _id = i*j*k
            param = {'_id': _id, 'parameter_key': parameter_key, 'value': value, 'multiplier': multiplier, 'out_of_bounds': out_of_bounds}
            concrete_result.append(param)
        test = {'concrete_result': concrete_result, '_id': _id, 'timestamp': timestamp, 'raw_text': raw_text}
        test_paciente.append(test)
    lab_test.append(test_paciente)

data['lab_tests']=lab_test


# Initialization of lists
# Type of variables set by hand according to Marco's classification

#Patient info
info = []
max_info = []
min_info = []
type_info = []

#Lab info
Lab = []
Max_lab = []
Min_lab = []
Type_lab = []

#Clinical parameteres
clinical_params= []
max_clinic = []
min_clinic = []
Type_clinic = []

#Treatments
drug_names = []
dose_max = []
dose_min = []
Type_drug = []

#Covid Test
covid_test = []
result_covid = []
Type_covid = []

#Previous Conditions
prev_cond = [] #categories
Type_cond = []

#Chest rx
rx_info = []
cat_rx = []
Type_rx = []

Type_rx.append('tv_bool')
Type_rx.append('tv_cat')
cat_rx = [[True,False],[]]
rx_info.append('has_pneumonia')
rx_info.append('pneumonia_subtype')
i=1

#Sublist of symptoms and complications
symptoms = [] # I will store names, but the real variable is "has_symptom_whatever"
complications = [] # same

for index, patient in data.iterrows():
    # To get all the basic info
    for (k,v) in patient.items():
        if k not in info:
            info.append(k)
            if k == 'gender' or k == 'ethnicity' or k=='health_provider_id' or k == '_id':
                max_info.append([v])
                min_info.append([v])
                type_info.append('tc_cat')
            elif type(v) == float:
                max_info.append('event')
                min_info.append('event')
                type_info.append('event')
            elif type(v) == list:
                max_info.append('dic')
                min_info.append('dic')
                type_info.append('tc_cat')
            else:
                max_info.append(v)
                min_info.append(v)
                if  type(v) == bool:
                    type_info.append('tc_bool')
                elif type(v) == int or type(v) == float:
                    type_info.append('tc_num')
                
        elif k in info:
            index = info.index(k)
            if k == 'gender' or k == 'ethnicity' or k=='health_provider_id' or k=='_id':
                if v not in max_info[index]:
                    max_info[index].append(v)
                    #min_info[index].append(v)
                    
            elif type(v) == list or type(v) == str or type(v) == float:
                pass  
                
            else:
                if v > max_info[index]:
                    max_info[index] = v
                elif v < min_info[index]:
                    min_info[index] = v
            
    # To get all different the parameters of the blood tests and their max and min within the DB
    lab_tests = patient['lab_tests']
    for test in lab_tests:
        for (item, val) in test.items():
            if item == 'concrete_result':
                for param in val:
                    if param['parameter_key'] not in Lab:
                        Lab.append(param['parameter_key'])
                        Type_lab.append('tv_num')
                        Max_lab.append(param['value'])
                        Min_lab.append(param['value'])
                    
                    elif param['parameter_key'] in Lab:
                        index = Lab.index(param['parameter_key'])
                        if param['value'] > Max_lab[index]:
                            Max_lab[index] = param['value']
                        elif param['value'] < Min_lab[index]:
                            Min_lab[index] = param['value']
                    
    # To get all fields from clinical updates and their max and mins
    clinical_update = patient['clinical_update']
    for update in clinical_update:
        for (field,value) in update.items():
            if field not in clinical_params:
                clinical_params.append(field)
                if field == 'other_complications':
                    Type_clinic.append('tc_cat')
                    max_clinic.append([value])
                    min_clinic.append([value])
                elif field == 'other_symptoms':
                    Type_clinic.append('tc_cat')
                    max_clinic.append([value])
                    min_clinic.append([value])
                else:
                    if type(value) == bool:
                        Type_clinic.append('tv_bool')
                    elif type(value) == int:
                        Type_clinic.append('tv_num')
                    else:
                        Type_clinic.append('tbd')
                    max_clinic.append(value)
                    min_clinic.append(value)
            
            elif field in clinical_params:
                index = clinical_params.index(field)
                if field == 'other_complications':
                    if value not in max_clinic[index]:
                        max_clinic[index].append([value])
                    # elif value < min_clinic[index]:
                    #     min_clinic[index].append([value])
                elif field == 'other_symptoms':
                    if value not in max_clinic[index]:
                        max_clinic[index].append([value])
                    # elif value < min_clinic[index]:
                    #     min_clinic[index].append([value])
                else:
                    if value > max_clinic[index]:
                        max_clinic[index] = value
                    elif value < min_clinic[index]:
                        min_clinic[index] = value
    
    # To get all the differnt drugs (categories) and their max and min dose
    drug = patient['drug']
    for update in drug:
        if update['name'] not in drug_names:
            Type_drug.append('tv_cat')
            drug_names.append(update['name'])
            dose_max.append(update['dose'])
            dose_min.append(update['dose'])
                
        elif update['name'] in drug_names:
            index = drug_names.index(update['name'])
            if update['dose'] > dose_max[index]:
                dose_max[index] = update['dose']
            elif update['dose'] < dose_min[index]:
                dose_min[index] = update['dose']
                
    # To get all the tests of covid and their possible results (categories)
    sars_cov2_test = patient['sars_cov2_test']
    for update in sars_cov2_test:
        if update['test_type'] not in covid_test:
            Type_covid.append('tv_cat')
            covid_test.append(update['test_type'])
            result_covid.append([update['result']])
                
        elif update['test_type'] in covid_test:
            index = covid_test.index(update['test_type'])
            if update['result'] not in result_covid[index]:
                result_covid[index].append(update['result'])
                
    # To get all the previous conditions names (categories)
    previous_contitions = patient['previous_contitions']
    Type_cond.append('tv_cat')
    for update in previous_contitions:
        if update['name'] not in prev_cond:
            prev_cond.append(update['name'])
    
     # To get all the pneumonia subtypes (categories)
    rx = patient['chest_rx']
    for update in rx:
        if update['pneumonia_subtype'] not in cat_rx[1]:
            cat_rx[1].append(update['pneumonia_subtype'])
    
            
    # Grouping info dictionary variables as categorical:
    for i in range(len(info)):
        if type_info[i]=='tc_cat':
            nam = info[i]
            if nam == 'previous_conditions':
                max_info[i]= prev_cond
                min_info[i]= prev_cond
                
            elif nam == 'clinical_update':
                max_info[i]= clinical_params
                min_info[i]= clinical_params
                
            elif nam == 'chest_rx':
                pass
                # max_info[i]= cat_rx[1]
                # min_info[i]= cat_rx[1]
            
            elif nam == 'sars_cov2_test':
                max_info[i]= covid_test
                min_info[i]= covid_test
            
            elif nam == 'lab_tests':
                max_info[i]= Lab
                min_info[i]= Lab
            
            elif nam == 'drug':
                max_info[i]= drug_names
                min_info[i]= drug_names
    
#Subroup of symptoms and complications: still have to append "other_symptoms" and "other_complications"
clinical_params_copy = clinical_params.copy()             
for param in clinical_params:
    if 'symptom' in param:
        name = param[12:]
        symptoms.append(name)
        clinical_params.remove(param)
    elif 'complication' in param:
        name = param[17:]
        complications.append(name)
        clinical_params.remove(param)

# Creating a dictionary with the informatio in the desired way for the dashboard
variables = dict()
for j in range(len(info)):
    var_name = 'Basic.' + info[j]
    if type_info[j] == 'tc_num' or type_info[j] == 'tv_num' or type_info[j] == 'tc_bool' or type_info[j] == 'tv_bool':
        variables[var_name] = {'type':type_info[j], 'value':[max_info[j],min_info[j]]}
        
    else: #Categories ---- 'events still not considered'
        variables[var_name] = {'type':type_info[j], 'value':max_info[j]}
        
var_name = 'Basic.Condiciones_Previas'        
variables[var_name] = {'type':'tc_cat', 'value':prev_cond}
        
for j in range(len(Lab)):
    var_name = 'Analitica.' + Lab[j]
    if Type_lab[j] == 'tc_num' or Type_lab[j] == 'tv_num' or Type_lab[j] == 'tc_bool' or Type_lab[j] == 'tv_bool':
        variables[var_name] = {'type':Type_lab[j], 'value':[Max_lab[j],Min_lab[j]]}
        
    else: #Categories ---- 'events still not considered'
        variables[var_name] = {'type':Type_lab[j], 'value':Max_lab[j]}
        
for j in range(len(clinical_params)):
    var_name = 'Clinico.' + clinical_params[j]
    if Type_clinic[j] == 'tc_num' or Type_clinic[j] == 'tv_num' or Type_clinic[j] == 'tc_bool' or Type_clinic[j] == 'tv_bool':
        variables[var_name] = {'type':Type_clinic[j], 'value':[max_clinic[j],min_clinic[j]]}
        
    else: #Categories ---- 'events still not considered'
        variables[var_name] = {'type':Type_clinic[j], 'value':max_clinic[j]}

var_name = 'Clinico.Sintomas'        
variables[var_name] = {'type':'tc_cat', 'value':symptoms}

var_name = 'Clinico.Complicaciones'        
variables[var_name] = {'type':'tc_cat', 'value':complications}        


for j in range(len(drug_names)):
    var_name = 'Tratamiento.' + drug_names[j]
    if Type_drug[j] == 'tc_num' or Type_drug[j] == 'tv_num' or Type_drug[j] == 'tc_bool' or Type_drug[j] == 'tv_bool':
        variables[var_name] = {'type':Type_drug[j], 'value':[dose_max[j],dose_min[j]]}
        
    else: #Categories ---- 'events still not considered'
        variables[var_name] = {'type':Type_drug[j], 'value':dose_max[j]}
        
for j in range(len(covid_test)):
    var_name = 'TestCovid.' + str(covid_test[j])
    variables[var_name] = {'type':Type_covid[j], 'value':result_covid[j]}
        
for j in range(len(rx_info)):
    var_name = 'RX.' + rx_info[j]
    variables[var_name] = {'type':Type_rx[j], 'value':cat_rx[j]}




            
        
                
    
    
        
        
        
        
        
        
        
        
        







