# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 18:48:07 2020

@author: Jesús S. Alegre
"""

import json
import requests
import pandas as pd
import numpy as np
from random import randint, seed, random
from datetime import datetime
from dateutil.relativedelta import relativedelta
seed(1)


ethnicity = ['european', 'african', 'asian', 'other']
boolean = [True,False]
prev_conditions = ['diabetes','smoker','cancer', 'colesterol']
parametros = ['glucose','linfocitos','plaquetas']
multipliers = [2,5,10]
symptoms1 = ['dyspena','anosmia','ageusia']
symptoms2 = ['rinorrea','dizziness','nausea']
symptoms3 = ['diarrhoea','headache','anorexia','articular_pain']
symptoms4 = ['astenia','chest_pain','palpitations']
drogas = ['Morphin', 'Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Antibioticos']


def dummy_data():
    data = []
    
    for i in range (100):
        previous_conditions = [] # done
        test_paciente = [] # done
        clinical_updates = [] # done
        chest_rxs= [] # done
        sars_cov2_tests = [] # done
        drugs = [] # done
        
        n_drugs = randint(0,4)
        for j in range(n_drugs):
            date = datetime.now()-relativedelta(days=22/(j+1))
            drg = {'_id':str(i), 'date_start':date,
                  'date_end':date + relativedelta(days=randint(1,2)), 
                  'name':drogas[randint(0,4)], 'dose':randint(1,10),
                  'interval':randint(1,4)*3600}
            drugs.append(drg)
            
        
        n_sars = randint(0,2)
        for j in range(n_sars):
            sars = {'_id':str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)),
                  'result':randint(0,3), 'test_type': randint(0,2)}
            sars_cov2_tests.append(sars)
        
        n_rx = randint(0,2)
        for j in range(n_rx):
            pneumonia = [0,randint(0,2)]
            rx = {'_id':str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)),
                  'has_pneumonia':boolean[randint(0,1)], 'pneumonia_subtype':pneumonia[randint(0,1)]}
            chest_rxs.append(rx)
        
        
        n_cu = randint(1,20)
        for j in range(n_cu):
            #If i dont put it here, no new random numbers are generated
            
            cu = {'_id': str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)) ,'is_icu_candidate':boolean[randint(0,1)], 
                  'temperature_celsius':randint(35,42), 'blood_pressure_systolic':randint(120,160),
                  'blood_pressure_diastolic':randint(120,160), 'heart_rate': randint(50,120),
                  'respiratory_rate':randint(15,30),
                  'o2_saturation_percent':randint(60,100), 'o2_device':randint(0,2),
                  'o2_device_specifier':randint(1,10),
                  'has_good_o2_device_adherence':boolean[randint(0,1)], 'needs_prone_position':boolean[randint(0,1)],
                  'has_symptom_cough':boolean[randint(0,1)], 'has_symptom_dyspena':boolean[randint(0,1)],
                  'has_symptom_anosmia':boolean[randint(0,1)],'has_symptom_ageusia':boolean[randint(0,1)],
                  'has_symptom_rinorrea':boolean[randint(0,1)],'has_symptom_dizziness':boolean[randint(0,1)],
                  'has_symptom_nausea':boolean[randint(0,1)],'has_symptom_diarrhoea':boolean[randint(0,1)],
                  'has_symptom_headache':boolean[randint(0,1)],'has_symptom_anorexia':boolean[randint(0,1)],
                  'has_symptom_articular_pain':boolean[randint(0,1)],'has_symptom_astenia':boolean[randint(0,1)],
                  'has_symptom_chest_pain':boolean[randint(0,1)],'has_symptom_palpitations':boolean[randint(0,1)],
                  'other_symptoms':'locura', 'has_complication_thrombosis':boolean[randint(0,1)],
                  'has_complication_renal_impairment':boolean[randint(0,1)],
                  'has_complication_liver_impairment':boolean[randint(0,1)],'has_complication_arritmia':boolean[randint(0,1)],
                  'has_complication_heart_failure':boolean[randint(0,1)],'has_complication_infection':boolean[randint(0,1)],
                  'other_complications':'dierna'}
            clinical_updates.append(cu)
            clinical_updates.append(cu)
        
        n_tests = randint(1,10)
        for j in range(n_tests): # numero de tests por paciente
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
        
        n_pc = randint(0, 2)
        for j in range(n_pc):
            pc = {'_id': '5e8f42eb854f7f49880906b6','name': prev_conditions[randint(0,3)],'extra_info': {'insulin_units': 2},'comments': 'bla bla'}
            previous_conditions.append(pc)
    
    
        discharge = [None,(datetime.now()-relativedelta(days=randint(10,20)))]
        patient = {'_id': str(i),
                     'health_provider_id': randint(1,3),
                     'gender': randint(1,3),
                     'ethnicity': ethnicity[randint(0,3)],
                     'date_of_birth': datetime.now()-relativedelta(years=randint(5,85)),
                     'date_of_first_symptoms': datetime.now()-relativedelta(days=randint(25,40)),
                     'date_of_admission': datetime.now()-relativedelta(days=randint(0,10)),
                     'date_of_discharge': discharge[randint(0,1)],
                     'is_deceased': boolean[randint(0,1)],
                     'height_cm': randint(150, 200),
                     'weight_kg': randint(50, 100),
                     'last_edition_date': datetime.now(),
                     'episode_index': randint(1,3),
                     'previous_conditions': previous_conditions,
                     'clinical_update': clinical_updates,
                     'chest_rx': chest_rxs,
                     'sars_cov2_test': sars_cov2_tests,
                     'lab_tests': test_paciente,
                     'drug': drugs,
                     '__v': 0}
        
        data.append(patient)
        
    return data

DD = dummy_data()
DATA = pd.DataFrame(DD)


####################################################################################

# Initialization of lists
# Type of variables set by hand according to Marco's classification
# IGNORAR LOS 'NONE' !! aun no implementado

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

for index, patient in DATA.iterrows():
    # To get all the basic info
    for (k,v) in patient.items():
        if k not in info:
            info.append(k)
            if k == 'gender' or k == 'ethnicity' or k=='health_provider_id' or k == '_id':
                max_info.append([v])
                min_info.append([v])
                type_info.append('tc_cat')
            elif type(v) == float:
                max_info.append('events')
                min_info.append('events')
                type_info.append('events')
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
                else:
                    type_info.append('events')
                
        elif k in info:
            index = info.index(k)
            if k == 'gender' or k == 'ethnicity' or k=='health_provider_id' or k=='_id':
                if v not in max_info[index]:
                    max_info[index].append(v)
                    #min_info[index].append(v)
                    
            elif type(v) == list or type(v) == str or type(v) == float:
                pass  
                
            else:
                if type(v)!="<class 'NoneType'>":
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
                        if str(type(param['value']))!="<class 'NoneType'>":
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
                    elif str(type(value))== "<class 'NoneType'>":
                        Type_clinic.append('tv_num')
                    else:
                        Type_clinic.append('tc_cat')
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
                    if str(type(max_clinic[index]))== "<class 'NoneType'>" and str(type(value)) != "<class 'NoneType'>":
                        max_clinic[index] = value
                        
                    elif str(type(min_clinic[index]))=="<class 'NoneType'>" and str(type(value)) != "<class 'NoneType'>":
                        min_clinic[index] = value
                        
                    elif str(type(value)) != "<class 'NoneType'>":
                        if value > max_clinic[index]:
                            max_clinic[index] = value
                        elif value < min_clinic[index]:
                            min_clinic[index] = value
    
    # To get all the differnt drugs (categories) and their max and min dose
    drug = patient['drug']
    for update in drug:
        if update['name'] not in drug_names:
            Type_drug.append('tv_num')
            drug_names.append(update['name'])
            dose_max.append(update['dose'])
            dose_min.append(update['dose'])
                
        elif update['name'] in drug_names:
            index = drug_names.index(update['name'])
            # if type(update['dose'])!='NoneType':
            #     if update['dose'] > dose_max[index]:
            #         dose_max[index] = update['dose']
            #     elif update['dose'] < dose_min[index]:
            #         dose_min[index] = update['dose']
            
            if str(type(dose_max[index]))== "<class 'NoneType'>" and str(type(update['dose'])) != "<class 'NoneType'>":
                        dose_max[index] = update['dose']
                        
            elif str(type(min_clinic[index]))=="<class 'NoneType'>" and str(type(update['dose'])) != "<class 'NoneType'>":
                dose_min[index] = update['dose']
                
            elif str(type(update['dose'])) != "<class 'NoneType'>":
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
    previous_conditions = patient['previous_conditions']
    Type_cond.append('tv_cat')
    for update in previous_conditions:
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
    
#Subroup of symptoms and complications
clinical_params_copy = clinical_params.copy()             
for param in clinical_params_copy:
    if 'symptom' in param:
        if param != 'other_symptoms':
            #name = param[12:]
            symptoms.append(param)
            idx = clinical_params.index(param)
            clinical_params.pop(idx)
            Type_clinic.pop(idx)
            min_clinic.pop(idx)
            max_clinic.pop(idx)
        
    elif 'complication' in param:
        if param != 'other_complications':
            #name = param[17:]
            complications.append(param)
            idx = clinical_params.index(param)
            clinical_params.pop(idx)
            Type_clinic.pop(idx)
            min_clinic.pop(idx)
            max_clinic.pop(idx)
        
 


# Creating a dictionary with the informatio in the desired way for the dashboard
#droping parameters
info_to_be_removed = ['__v','chest_rx','lab_tests','previous_conditions','sars_cov2_test','clinical_update','drug']
cpy =  info.copy()
for i in range(len(cpy)):
    if cpy[i] in info_to_be_removed:
        index = info.index(cpy[i])
        del info[index]
        del type_info[index]
        del min_info[index]
        del max_info[index]


choices = dict()
for j in range(len(info)):
    var_name = 'Basic.' + info[j]
    if type_info[j] == 'tc_num' or type_info[j] == 'tv_num' or type_info[j] == 'tc_bool' or type_info[j] == 'tv_bool':
        choices[var_name] = {'type':type_info[j], 'value':[min_info[j],max_info[j]]}
        
    else: #Categories ---- 'events still not considered'
        choices[var_name] = {'type':type_info[j], 'value':max_info[j]}
        
var_name = 'Basic.Condiciones_Previas'        
choices[var_name] = {'type':'tc_cat', 'value':prev_cond}
        
for j in range(len(Lab)):
    var_name = 'Analitica.' + Lab[j]
    if Type_lab[j] == 'tc_num' or Type_lab[j] == 'tv_num' or Type_lab[j] == 'tc_bool' or Type_lab[j] == 'tv_bool':
        choices[var_name] = {'type':Type_lab[j], 'value':[Min_lab[j],Max_lab[j]]}
        
    else: #Categories ---- 'events still not considered'
        choices[var_name] = {'type':Type_lab[j], 'value':Max_lab[j]}
        
for j in range(len(clinical_params)):
    if clinical_params[j] != "_id" and clinical_params[j] != "timestamp":
        var_name = 'Clinico.' + clinical_params[j]
        if Type_clinic[j] == 'tc_num' or Type_clinic[j] == 'tv_num' or Type_clinic[j] == 'tc_bool' or Type_clinic[j] == 'tv_bool':
            choices[var_name] = {'type':Type_clinic[j], 'value':[min_clinic[j],max_clinic[j]]}
            
        else: #Categories ---- 'events still not considered'
            choices[var_name] = {'type':Type_clinic[j], 'value':max_clinic[j]}

var_name = 'Clinico.Sintomas'        
choices[var_name] = {'type':'tc_cat', 'value':symptoms}

var_name = 'Clinico.Complicaciones'        
choices[var_name] = {'type':'tc_cat', 'value':complications}        


for j in range(len(drug_names)):
    var_name = 'Tratamiento.' + drug_names[j]
    if Type_drug[j] == 'tc_num' or Type_drug[j] == 'tv_num' or Type_drug[j] == 'tc_bool' or Type_drug[j] == 'tv_bool':
        choices[var_name] = {'type':Type_drug[j], 'value':[dose_min[j],dose_max[j]]}
        
    else: #Categories ---- 'events still not considered'
        choices[var_name] = {'type':Type_drug[j], 'value':dose_max[j]}
        
for j in range(len(covid_test)):
    var_name = 'TestCovid.' + str(covid_test[j])
    choices[var_name] = {'type':Type_covid[j], 'value':result_covid[j]}
        
for j in range(len(rx_info)):
    var_name = 'RX.' + rx_info[j]
    choices[var_name] = {'type':Type_rx[j], 'value':cat_rx[j]}
    



variables = dict()
tc_bool = []
tc_cat= []
tc_num = []
tv_bool = []
tv_cat = []
tv_num = []
events = []

for k,v in choices.items():
    dot_index = k.find('.')
    name = k[dot_index+1:]
    if name == 'Complicaciones':
        for s in v['value']:
            tv_bool.append(s)
    
    elif name == 'Sintomas':
        for s in v['value']:
            tv_bool.append(s)
    
    else:
        if v['type'] == 'tc_bool':
            tc_bool.append(name)
        
        elif v['type'] == 'tc_cat':
            tc_cat.append(name)
            
        elif v['type'] == 'tc_num':
           tc_num.append(name)
           
        elif v['type'] == 'tv_bool':
           tv_bool.append(name)
           
        elif v['type'] == 'tv_cat':
           tv_cat.append(name)
           
        elif v['type'] == 'tv_num':
           tv_num.append(name)
           
        elif v['type'] == 'events':
           events.append(name)
           

    
variables = {'tc_bool':tc_bool , 'tc_cat':tc_cat, 'tc_num':tc_num, 'tv_bool':tv_bool, 'tv_cat':tv_cat, 'tv_num':tv_num, 'events':events}    
        
    
    
    
    
    
    
    
    
    
    
    
    
    