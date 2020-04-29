# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:40:52 2020

@author: Jesús S. Alegre
"""
import json
import requests
import pandas as pd
import numpy as np

# Filter coming from Dashboard
filters = {'Basic.gender': ['3', '1'], 'Basic.height_cm': [164.6, 190.65], 'Basic.episode_index': [1.7, 3], 'Clinico.other_symptoms': ['locura']}
# Lo transformo en :
# {'$and': [{'height_cm': {'$lte': 164.6}}, {'height_cm': {'$gte': 190.65}}, {'episode_index': {'$lte': 1.7}}, {'episode_index': {'$gte': 3}}, {'clinical_update': {'$elemMatch': {'$and': [{'other_symptoms': 'locura'}]}}}]}

# Other examples of Mongo filters:
# {lab_tests: {$elemMatch: {concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}
# {$and: [{lab_tests: {$elemMatch: { concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}, {previous_contitions: {$elemMatch: {name: 'diabetes'}}}]}
# payload = { filter : {filtroMierdas}, select : ['gender', 'episode_number', 'lab_tests'] }
# filtroMierdas = TIENE QUE SER UN UNICO FILTRO       
# {lab_tests: {$elemMatch: {concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}
# {$and: [{lab_tests: {$elemMatch: { concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}, {previous_contitions: {$elemMatch: {name: 'diabetes'}}}]}


# Filter transformation to our MongoDB structure and Query
super_filtro = []
for k, v in filters.items():
    lista_bs = []
    lista_cd = []
    lista_an = []
    lista_cl = []
    lista_rx = []
    lista_te = []
    lista_dr = []
    
    dot = k.find('.')
    subclass = k[:dot]
    var_name = k[dot+1:]
    
    if subclass == 'Basic': # this categories should match the dot notation index of the variables
        if var_name == 'Condiciones_Previas':
            for var in v:
                fil = {"name":var}
                lista_cd.append(fil)
            #filtros_anidados_condiciones = {"previous_conditions": {"$elemMatch" : {"$and": lista_cd}}}
            super_filtro.append({"previous_conditions": {"$elemMatch" : {"$and": lista_cd}}})
        
        else:
            if type(v[0])==bool or type(v[0])==str: # categories and booleans
                for var in v:
                    fil = {var_name:var}
                    lista_bs.append(fil)
            
            elif type(v[0])==int or type(v[0])==float:  # numebers, go for max and mins
                for i in range(len(v)):
                    if i == 0:  #max
                        fil = {var_name:{"$lte":v[i]}}
                        #lista_bs.append(fil)
                        super_filtro.append(fil)
                        
                    elif i == 1: #min
                        fil = {var_name:{"$gte":v[i]}}
                        #lista_bs.append(fil)
                        super_filtro.append(fil)
            # filtros_anidados_basico =  lista_bs
            # super_filtro.append(filtros_anidados_basico)
        
    
    elif subclass == 'Analitica':
         for i in range(len(v)):
            if i == 0:  #max
                 fil = {"parameter_key":var_name}
                 fil1= {"value":{"$lte":v[i]}}
                 lista_an.append(fil)
                 lista_an.append(fil1)
                 
            elif i == 1: #min
                 fil = {"parameter_key":var_name}
                 fil1= {"value":{"$gte":v[i]}}
                 lista_an.append(fil)
                 lista_an.append(fil1)      
         #filtros_anidados_analiticas = {"lab_tests": {"$elemMatch": { "concrete_result": {"$elemMatch" : {"$and": lista_an}}}}}
         super_filtro.append({"lab_tests": {"$elemMatch": { "concrete_result": {"$elemMatch" : {"$and": lista_an}}}}})
             
    elif subclass == 'Clinico':
        if var_name == "other_symptoms" or var_name == "other_complications":
            for var in v:
                fil = 	{var_name:var}
                lista_cl.append(fil)
        
        elif type(var) == int or type(var) == float:
            for i in range(len(v)):
                if i == 0:  #max
                    fil = {var_name:{"$lte":v[i]}}
                    lista_cl.append(fil)
                
                elif i == 1: #min
                    fil = {var_name:{"$gte":v[i]}}
                    lista_cl.append(fil)
        
        elif type(var) == bool:
            fil = {var_name:var}
            lista_cl.append(fil)
        #filtros_anidados_clinical = {"clinical_update": {"$elemMatch": {"$and":lista_cl}}}
        super_filtro.append({"clinical_update": {"$elemMatch": {"$and":lista_cl}}})
        
    elif subclass == 'RX':
        for var in v:
            fil = {var_name:var}
            lista_rx.append(fil)   
        #filtros_anidados_chest = {"chest_rx": {"$elemMatch": {"$and":lista_rx}}}
        super_filtro.append( {"chest_rx": {"$elemMatch": {"$and":lista_rx}}})
        
    elif subclass == 'TestCovid':
        for var in v:
            fil = 	{"test_type":var_name}
            fil1 = {"result":var}
            lista_te.append(fil)
            lista_te.append(fil1)
        #filtros_anidados_covid = {"sars_cov2_test": {"$elemMatch": {"$and":lista_te}}}
        super_filtro.append({"sars_cov2_test": {"$elemMatch": {"$and":lista_te}}})
        
    elif subclass == 'Tratamiento':
         for i in range(len(v)):
            if i == 0:  #max
                fil = {"name":var_name}
                fil1 = {"dose":{"$lte":v[i]}}
                lista_dr.append(fil)
                lista_dr.append(fil1)
            
            elif i == 1: #min
                fil = {"name":var_name}
                fil1 = {"dose":{"$gte":v[i]}}
                lista_dr.append(fil)
                lista_dr.append(fil1)
         #filtros_anidados_drugs = {"drug": {"$elemMatch":{"$and":lista_dr}}}
         super_filtro.append({"drug": {"$elemMatch":{"$and":lista_dr}}})

# Creacion de un unico filtro anidado
filtros_anidados =  {"$and": super_filtro}
  

# Selected variables to display coming from Dashboard
Variables = ['Basic.height_cm', 'Basic.gender', 'Basic.drug', 'Basic.Condiciones_Previas']

v_lista = [] # to create the selection payload for the MongoDB query
v_post_sel = [] # to keep track of those variables that are not of 1st level and have to be selected later in python
for sel in Variables:
    dot = sel.find('.')
    subclass = sel[:dot]
    var_name = sel[dot+1:]
    
    if subclass == 'Basic' and var_name != "Condiciones_Previas": 
        v_lista.append(var_name)
    
    elif subclass == 'Basic' and var_name == "Condiciones_Previas":
        v_lista.append("previous_conditions") 
        v_post_sel.append(var_name)
    
    elif subclass == 'Analitica':
        v_lista.append("lab_tests") 
        v_post_sel.append(sel)
    
    elif subclass == 'Clinico':
        v_lista.append("clinical_update")
        v_post_sel.append(sel)
    
    elif subclass == 'RX':
        v_lista.append("chest_rx")
        v_post_sel.append(sel)
    
    elif subclass == 'TestCovid':
        v_lista.append("sars_cov2_test")
        v_post_sel.append(sel)
    
    elif subclass == 'Tratamiento':
        v_lista.append("drug")
        v_post_sel.append(sel)




# Create the payload according to Mongo nomenclature
filtro_MongoDB = {"filter": filtros_anidados, "select":v_lista}
     
payload = json.dumps(filtro_MongoDB, separators=(',',':'))

############################################ TILL HERE WORKS PERFECTLY



############################### DB not up to date, thus, structure does not mach with query request.

# # Perform the query
# resp_filter = requests.get('http://localhost:3000/patient', params=payload)    
# if resp_filter.status_code == 200:
#     data_filtered= resp_filter.json()   



# # Transform data into dataframe
# data_fs = pd.DataFrame(data_filtered)



# # Select data of 2nd and 3rd level that are stored in var: v_post_sel[] -- WITH THEIR TIMESTAMP!!! :D
# for sel in v_post_sel:
#     dot = sel.find('.')
#     subclass = sel[:dot]
#     var_name = sel[dot+1:]
    
#     if subclass == 'Basic' and var_name == "Condiciones_Previas": # It could only be the case of "previous_conditions", no timestamp in this case
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             valor = None
#             prev = patient['previous_conditions']
#             for (item, val) in prev.items():
#                 if item == 'name':
#                     valor = val
                    
#             var_col.append(valor)
#         dat[var_name]=var_col
    
#     elif subclass == 'Analitica':
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             lab_tests = patient['lab_tests']
#             for test in lab_tests:
#                 found =0
#                 valor = None
#                 time = None
#                 for (item, val) in test.items():
#                     if item == 'timestamp':
#                         time=val
#                     if item == 'concrete_result':
#                         for param in val:
#                             for (ky, v) in param.items():
#                                 if ky=='parameter_key' and v==var_name:
#                                     found = 1
#                                 if ky=='value':
#                                     valor=v
                                
#                         if found ==1 :
#                             value_array = np.append(value_array,valor)
#                 if found == 1:
#                     time_array = np.append(time_array,time)
            
#             var_col.append(pd.Series(value_array, name=var_name, index=time_array))
#         dat[var_name]=var_col
    
#     elif subclass == 'Clinico':
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             clinics = patient['clinical_update']
#             for updates in clinics:
#                 found =0
#                 valor = None
#                 time = None
#                 for (item, val) in updates.items():
#                     if item == 'timestamp':
#                         time=val
                        
#                     if item == var_name:
#                         valor=v
#                         found = 1
                        
#                 if found ==1 :
#                     value_array = np.append(value_array,valor)
#                     time_array = np.append(time_array,time)
                
#             var_col.append(pd.Series(value_array, name=var_name, index=time_array))
#         dat[var_name]=var_col
    
#     elif subclass == 'RX':
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             rxs = patient['chest_rx']
#             for updates in rxs:
#                 found =0
#                 valor = None
#                 time = None
#                 for (item, val) in updates.items():
#                     if item == 'timestamp':
#                         time=val
                        
#                     if item == var_name:
#                         valor=v
#                         found = 1
                        
#                 if found ==1 :
#                     value_array = np.append(value_array,valor)
#                     time_array = np.append(time_array,time)
                
#             var_col.append(pd.Series(value_array, name=var_name, index=time_array))
#         dat[var_name]=var_col
    
#     elif subclass == 'TestCovid':
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             COV = patient['sars_cov2_test']
#             for updates in COV:
#                 found =0
#                 valor = None
#                 time = None
#                 for (item, val) in updates.items():
#                     if item == 'timestamp':
#                         time=val
                        
#                     if item == "test_type" and val == var_name:
#                         found = 1
                    
#                     if item == "result":
#                         valor = val
                        
#                 if found ==1 :
#                     value_array = np.append(value_array,valor)
#                     time_array = np.append(time_array,time)
                
#             var_col.append(pd.Series(value_array, name=var_name, index=time_array))
#         dat[var_name]=var_col
    
#     elif subclass == 'Tratamiento': # date_end and interval not taken into account at this iteration.
#         var_col = []
#         dat=data_fs
#         for index, patient in dat.iterrows():
#             time_array = np.array([])
#             value_array = np.array([])
#             drugs = patient['drug']
#             for updates in drugs:
#                 found =0
#                 valor = None
#                 time = None
#                 for (item, val) in updates.items():
#                     if item == 'date_start':
#                         time=val
                        
#                     if item == "name" and val == var_name:
#                         found = 1
                    
#                     if item == "dose":
#                         valor = val
                        
#                 if found ==1 :
#                     value_array = np.append(value_array,valor)
#                     time_array = np.append(time_array,time)
                
#             var_col.append(pd.Series(value_array, name=var_name, index=time_array))
#         dat[var_name]=var_col
    
# # Droping the columns not needed, the ones with objects.
# #dat.drop[]
































