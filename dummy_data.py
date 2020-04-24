# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 23:50:16 2020

@author: Jesús S. Alegre
"""
from random import randint, seed, random
from datetime import datetime
from dateutil.relativedelta import relativedelta
seed(1)

ethnicity = ['european', 'african', 'asian', 'other']
discharge = [None,(datetime.now()-relativedelta(days=randint(10,20)))]
boolean = [True,False]
prev_contitions = ['diabetes','smoker','cancer', 'colesterol']
parametros = ['uno','dos','tres']
multipliers = [2,5,10]
symptoms1 = ['dyspena','anosmia','ageusia']
symptoms2 = ['rinorrea','dizziness','nausea']
symptoms3 = ['diarrhoea','headache','anorexia','articular_pain']
symptoms4 = ['astenia','chest_pain','palpitations']
blod_preassure = [None,randint(120,160)]
heart_rate = [None,randint(50,120)]
respiratory_rate = [None,randint(15,30)]
o2_saturation_percent = [None,randint(60,100)]
o2_device_specifier = [None,randint(1,10)]
pneumonia = [None,randint(0,2)]
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
            rx = {'_id':str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)),
                  'has_pneumonia':boolean[randint(0,1)], 'pneumonia_subtype':pneumonia[randint(0,1)]}
            chest_rxs.append(rx)
        
        
        n_cu = randint(1,20)
        for j in range(n_cu):
            cu = {'_id': str(i), 'timestamp':datetime.now()-relativedelta(days=22/(j+1)) ,'is_icu_candidate':boolean[randint(0,1)], 
                  'temperature_celsius':randint(35,42), 'blood_pressure_systolic':blod_preassure[randint(0,1)],
                  'blood_pressure_diastolic':blod_preassure[randint(0,1)], 'heart_rate': heart_rate[randint(0,1)],
                  'respiratory_rate':respiratory_rate[randint(0,1)],
                  'o2_saturation_percent':o2_saturation_percent[randint(0,1)], 'o2_device':randint(0,2),
                  'o2_device_specifier':o2_device_specifier[randint(0,1)],
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
            pc = {'_id': '5e8f42eb854f7f49880906b6','name': prev_contitions[randint(0,3)],'extra_info': {'insulin_units': 2},'comments': 'bla bla'}
            previous_conditions.append(pc)
    
    
    
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
                     'previous_contitions': previous_conditions,
                     'clinical_update': clinical_updates,
                     'chest_rx': chest_rxs,
                     'sars_cov2_test': sars_cov2_tests,
                     'lab_tests': test_paciente,
                     'drug': drugs,
                     '__v': 0}
        
        data.append(patient)
        
    return data

DD = dummy_data()