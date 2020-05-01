# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 23:50:16 2020

@author: Jesús S. Alegre
"""
import json
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
    
    for i in range (50):
        previous_conditions = [] # done
        test_paciente = [] # done
        clinical_updates = [] # done
        chest_rxs= [] # done
        sars_cov2_tests = [] # done
        drugs = [] # done
        
        n_drugs = randint(0,2)
        for j in range(n_drugs):
            date = datetime.now()-relativedelta(days=22/(j+1))
            drg = {'_id':str(i), 'date_start':str(date),
                  'date_end':str(date + relativedelta(days=randint(1,2))), 
                  'name':drogas[randint(0,4)], 'dose':randint(1,10),
                  'interval':randint(1,4)*3600}
            drugs.append(drg)
            
        
        n_sars = randint(0,2)
        for j in range(n_sars):
            sars = {'_id':str(i),'timestamp':str(datetime.now()-relativedelta(days=22/(j+1))),
                  'result':result[randint(0,1)], 'test_type': cov_test[randint(0,2)]}
            sars_cov2_tests.append(sars)
        
        n_rx = randint(0,2)
        for j in range(n_rx):
            rx = {'_id':str(i),'timestamp':str(datetime.now()-relativedelta(days=22/(j+1))),
                  'has_pneumonia':boolean[randint(0,1)], 'pneumonia_subtype':pneumonia[randint(0,2)], 'test_type':tipo_rx[randint(0,2)]}
            chest_rxs.append(rx)
        
        
        n_cu = randint(1,4)
        for j in range(n_cu):
            cu = {'_id': str(i), 'timestamp':str(datetime.now()-relativedelta(days=22/(j+1))) ,'is_icu_candidate':boolean[randint(0,1)], 
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
                     'date_of_birth': str(datetime.now()-relativedelta(years=randint(5,85))),
                     'date_of_first_symptoms': str(datetime.now()-relativedelta(days=randint(25,40))),
                     'date_of_admission': str(datetime.now()-relativedelta(days=randint(0,10))),
                     'date_of_discharge': str(discharge[randint(0,1)]),
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

DD = dummy_data()

archivo = open("dummy_data.txt","w")
archivo.write(str((DD)))
archivo.close()

with open('dummy_data.txt', 'w') as outfile:
    json.dump(DD, outfile)