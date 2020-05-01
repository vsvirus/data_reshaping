# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:38:20 2020

@author: Jesús S. Alegre
"""
import json
import pandas as pd
from random import randint, seed, random
from datetime import datetime
from dateutil.relativedelta import relativedelta
seed(1)

ethnicity = ['european', 'african', 'asian', 'other']
discharge = [None,(datetime.now()-relativedelta(days=randint(10,20)))]
boolean = [True,False]
prev_contitions = ['diabetes','smoker','cancer', 'colesterol']
parametros = ['hemoglobine','leucocytes','haematocrit']
symptoms1 = ['cough','dyspnea','anosmia','ageusia']
symptoms2 = ['rinorrea','dizziness','nausea']
symptoms3 = ['diarrhoea','headache','anorexia','articular_pain']
symptoms4 = ['astenia','chest_pain','palpitations']

complications1 = ['thrombosis','renal_impairment','liver_impairment']
complications2 = ['arritmia','heart_failure','infection']

lugares = ['Llegada', 'Planta', 'UCI']

blod_preassure = [None,randint(120,160)]
heart_rate = [None,randint(50,120)]
respiratory_rate = [None,randint(15,30)]
o2_saturation_percent = [None,randint(60,100)]
o2_device_specifier = [None,randint(1,10)]
pneumonia = ['unilateral','bilateral','frontal']
tipo_rx = ['chest_rx_ray','escaner','Tac']
drogas = ['Morphin', 'Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Antibioticos']
cov_test = ['pcr', 'abb', 'ott']
result = ['positive', 'negative']


def dummy_data():
    data = []
    
    for i in range (10):
        previous_conditions = [] # done
        test_paciente = [] # done
        clinical_updates = [] # done
        chest_rxs= [] # done
        sars_cov2_tests = [] # done
        drugs = [] # done
        
        n_drugs = randint(0,2)
        for j in range(n_drugs):
            date = datetime.now()-relativedelta(days=22/(j+1))
            drg = {'_id':str(i), 'date_start':date,
                  'date_end':date + relativedelta(days=randint(1,2)), 
                  'name':drogas[randint(0,4)], 'dose':randint(1,10),
                  'interval':randint(1,4)*3600}
            drugs.append(drg)
            
        
        n_sars = randint(0,2)
        for j in range(n_sars):
            sars = {'_id':str(i),'timestamp':datetime.now()-relativedelta(days=22/(j+1)),
                  'result':result[randint(0,1)], 'test_type': cov_test[randint(0,2)]}
            sars_cov2_tests.append(sars)
        
        n_rx = randint(0,2)
        for j in range(n_rx):
            rx = {'_id':str(i),'timestamp':datetime.now()-relativedelta(days=22/(j+1)),
                  'has_pneumonia':boolean[randint(0,1)], 'pneumonia_subtype':pneumonia[randint(0,2)], 'test_type':tipo_rx[randint(0,2)]}
            chest_rxs.append(rx)
        
        
        n_cu = randint(1,4)
        for j in range(n_cu):
            cu = {'_id': str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)) ,'is_icu_candidate':boolean[randint(0,1)], 
                  'temperature_celsius':randint(35,42), 'blood_pressure_systolic':randint(120,160),
                  'blood_pressure_diastolic':randint(120,160), 'heart_rate': randint(50,120),
                  'respiratory_rate':randint(15,30), "glasgow_coma_scale_score":randint(10,20),
                  'o2_saturation_percent':randint(60,100), 'o2_device_type':randint(0,2),
                  'o2_device_model':randint(1,10), 'o2_device_oxygen_concentration_percent':randint(0,100),
                  'o2_device_flow_liters_per_min':randint(0,4),
                  'has_good_o2_device_adherence':boolean[randint(0,1)], 'needs_prone_position':boolean[randint(0,1)],
                  'symptoms':[symptoms1[randint(0,len(symptoms1)-1)],symptoms2[randint(0,len(symptoms2)-1)],symptoms3[randint(0,len(symptoms3)-1)],symptoms4[randint(0,len(symptoms4)-1)]],
                  'other_symptoms':['locura'], 
                  'complications':[complications1[randint(0,len(complications1)-1)],complications2[randint(0,len(complications2)-1)]],
                  'other_complications':['dierna'],
                  'location':lugares[randint(0,2)]}
            clinical_updates.append(cu)
        
        n_tests = randint(1,5)
        for j in range(n_tests): # numero de tests por paciente
            timestamp = j
            raw_text = 'nadaandanaa'
            concrete_result = []
            for k in range(0,3): # numero de parametros por test
                parameter_key = parametros[k]
                value = j*70 - 2**j + 100**random()
                out_of_bounds = [False,True]
                _id = i*j*k
                param = {'parameter_key': parameter_key, 'value': value, 'is_out_of_bounds': out_of_bounds[randint(0,1)]}
                concrete_result.append(param)
            test = {'items': concrete_result, '_id': _id,'timestamp': timestamp, 'text_raw': raw_text}
            test_paciente.append(test)
        
        n_pc = randint(0, 2)
        for j in range(n_pc):
            pc = {'name': prev_contitions[randint(0,3)],'extra_info': {'insulin_units': 2},'comments': 'bla bla'}
            previous_conditions.append(pc)
    
        patient = {'_id': str(i),
                   'patient_id':str(i),
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
                     'episode_number': randint(1,3),
                     'previous_conditions': previous_conditions,
                     'clinical_updates': clinical_updates,
                     'radiological_tests': chest_rxs,
                     'coronavirus_tests': sars_cov2_tests,
                     'lab_tests': test_paciente,
                     'prescriptions': drugs}
        
        data.append(patient)
    
    return data

# Function to find min, max, categories, and classify them according to types
def seeker(k,v,choices,route,tipo, variables):
    if tipo == 'tc':
        cat = 'tc_cat'
        bol = 'tc_bool'
        num = 'tc_num'
        
    elif tipo == 'tv':
        cat = 'tv_cat'
        bol = 'tv_bool'
        num = 'tv_num'
    
    if k not in choices and k not in second_level:        
        choices[k] = {'Route':route}
        if type(v)==list: # categories
              choices[k]['type'] = cat
              choices[k]['value'] = v
        
        elif type(v) == str: # categories auch
              choices[k]['type'] = cat
              choices[k]['value'] = [v]
             
        elif type(v) == bool: # booleans
              choices[k]['type'] = bol
              choices[k]['value'] = [True,False]
        
        elif type(v) == int or type(v)==float: # numerics
              choices[k]['type'] = num
              choices[k]['value'] = [v,v]
        else: # to avoid conflict with timestamp
          choices[k]['type'] = 'None'
        
        variables[choices[k]['type']] = variables[choices[k]['type']] + [k]
    
    elif k in choices and k not in second_level:
        if type(v)==list and choices[k]['type'] == cat: # necessary because some categorial variables can be equal to several categories
            for elem in v:
                if elem not in choices[k]['value']:
                      choices[k]['value'] = choices[k]['value'] + [elem]
        
        elif type(v)==str and choices[k]['type'] == cat: # necessary because some categorial variables can be equal to several categories
            if v not in choices[k]['value']:
                     choices[k]['value'].append(v)
        
        elif choices[k]['type'] == num:
            if v > choices[k]['value'][1]:
                choices[k]['value'][1]=v
            elif v < choices[k]['value'][0]:
                choices[k]['value'][0]=v
                
    return choices, variables
    

DD = dummy_data()
DATA = pd.DataFrame(DD)

# to know the name of the first level variables and which ones have other levels underneath:
first_level = []
second_level = []
for k,v in DD[0].items():
    first_level.append(k)
    if type(v) == list:
        second_level.append(k)
 
    
# Gather all variables, classify by type and get their max and min or categories  
# Gather all types, and classify variables accordingly
####################################################################################
variables = {'tc_bool':[] , 'tc_cat':[], 'tc_num':[], 'tv_bool':[], 'tv_cat':[], 'tv_num':[], 'events':[], 'None':[]}      
choices = dict()
for index, patient in DATA.iterrows():
    # To get all the basic info but not the variables with objects inside
    for (k,v) in patient.items():
        route = 'Basic'
        choices, variables = seeker(k,v,choices,route,'tc',variables)
        
    # To get all different the parameters of the blood tests and their max and min within the DB
    lab_tests = patient['lab_tests']
    for test in lab_tests:
        for (item, val) in test.items():
            if item == 'items':
                for param in val:
                    k = param['parameter_key']
                    v = param['value']
                    route = 'Analitica'
                    choices, variables = seeker(k,v,choices,route,'tv', variables)           
        
    #To get all fields from clinical updates and their max and mins
    clinical_update = patient['clinical_updates']
    for update in clinical_update:
        for (k,v) in update.items():
            route = 'Clinico'
            choices, variables = seeker(k,v,choices,route,'tv', variables)
                          
    #To get all the differnt drugs (categories) and their max and min dose
    drug = patient['prescriptions']
    for update in drug: 
        k = update['name']
        v = update['dose']
        route = 'Tratamiento'
        choices, variables = seeker(k,v,choices,route,'tv', variables)
                                             
    # To get all the tests of covid and their possible results (categories)
    sars_cov2_test = patient['coronavirus_tests']
    for update in sars_cov2_test:
        k = update['test_type']
        v = update['result']
        route = 'TestCovid'
        choices, variables = seeker(k,v,choices,route,'tv', variables)
                            
    # To get all the previous conditions names (categories)
    previous_conditions = patient['previous_conditions']
    k = 'Condiciones_Previas' #if I put 'previous_conditions', as it is in 'second_level', it wont take it
    for update in previous_conditions:
         v = update['name']
         route = 'Condiciones_Previas'
         choices, variables = seeker(k,v,choices,route,'tv', variables)     
                    
    # To get all radiological tests variables
    rx = patient['radiological_tests']
    for update in rx:
        for (k,v) in update.items():
            route = 'Radiologia'
            choices, variables = seeker(k,v,choices,route,'tv', variables)
            


# Saving choices and variables as JSON in a txt file
with open('choices.txt', 'w') as outfile:
    json.dump(choices, outfile)
    
with open('variables.txt', 'w') as outfile:
    json.dump(variables, outfile)




        