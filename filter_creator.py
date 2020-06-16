# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:40:52 2020
@author: Jesús S. Alegre
"""
import json
import requests
import pandas as pd
import numpy as np
import yaml


# Filter coming from Dashboard
filters = {'gender': ['female'], 'height_cm': [20, 200],'Amoxicilina':[0,10], 'hemoglobine': [10,30], 'Clinico.other_symptoms': ['locura']}
filters = {'gender': ['female'], 'height_cm': [20, 200]}
# 'Amoxicilina':[10,0], 'Clinico.other_symptoms': ['locura']
#filters = {'gender': ['male']}

# https://backend-demo.cobig19.com/patient?filter={"$and":[{"gender":"male"}]}&select=["height_cm","prescriptions","lab_tests","previous_conditions"]

# Lo transformo en :
# {'$and': [{'height_cm': {'$lte': 164.6}}, {'height_cm': {'$gte': 190.65}}, {'episode_index': {'$lte': 1.7}}, {'episode_index': {'$gte': 3}}, {'clinical_update': {'$elemMatch': {'$and': [{'other_symptoms': 'locura'}]}}}]}

# Other examples of Mongo filters:
# {lab_tests: {$elemMatch: {concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}
# {$and: [{lab_tests: {$elemMatch: { concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}, {previous_contitions: {$elemMatch: {name: 'diabetes'}}}]}
# payload = { filter : {filtroMierdas}, select : ['gender', 'episode_number', 'lab_tests'] }
# filtroMierdas = TIENE QUE SER UN UNICO FILTRO
# {lab_tests: {$elemMatch: {concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}
# {$and: [{lab_tests: {$elemMatch: { concrete_result: {$elemMatch : {$and: [{value : 15},{parameter_key:'aaaaa'}]}}}}}, {previous_contitions: {$elemMatch: {name: 'diabetes'}}}]}


with open("choices.txt") as json_file: #--> in case no __.notation, I have to find the subclass importing choices variable
    ch = json.load(json_file)

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
    if dot == -1: # not found --> in case no __.notation
        subclass = ch[k]['Route']
        var_name = k
    else:
        subclass = k[:dot]
        var_name = k[dot+1:]

    if subclass == 'Basic': # this categories should match the dot notation index of the variables
        if var_name == 'Condiciones_Previas':
            for var in v:
                fil = {"name":var}
                lista_cd.append(fil)
            super_filtro.append({"previous_conditions": {"$elemMatch" : {"$and": lista_cd}}})

        else:
            if type(v[0])==bool or type(v[0])==str: # categories and booleans
                for var in v:
                    fil = {var_name:var}
                    lista_bs.append(fil)
                    super_filtro.append(fil)

            elif type(v[0])==int or type(v[0])==float:  # numebers, go for max and mins
                for i in range(len(v)):
                    if i == 0:  #min
                        fil = {var_name:{"$gte":v[i]}}
                        super_filtro.append(fil)

                    elif i == 1: #max
                        fil = {var_name:{"$lte":v[i]}}
                        super_filtro.append(fil)

    elif subclass == 'Analitica':
         for i in range(len(v)):
            if i == 0:  #min
                 fil = {"parameter_key":var_name}
                 fil1= {"value":{"$gte":v[i]}}
                 lista_an.append(fil)
                 lista_an.append(fil1)

            elif i == 1: #max
                 fil = {"parameter_key":var_name}
                 fil1= {"value":{"$lte":v[i]}}
                 lista_an.append(fil)
                 lista_an.append(fil1)
         super_filtro.append({"lab_tests": {"$elemMatch": { "items": {"$elemMatch" : {"$and": lista_an}}}}})

    elif subclass == 'Clinico':
        if var_name == "other_symptoms" or var_name == "other_complications":
            for var in v:
                fil = 	{var_name:var}
                lista_cl.append(fil)

        elif type(var) == int or type(var) == float:
            for i in range(len(v)):
                if i == 0:  #min
                    fil = {var_name:{"$gte":v[i]}}
                    lista_cl.append(fil)

                elif i == 1: #max
                    fil = {var_name:{"$lte":v[i]}}
                    lista_cl.append(fil)

        elif type(var) == bool:
            fil = {var_name:var}
            lista_cl.append(fil)
        super_filtro.append({"clinical_updates": {"$elemMatch": {"$and":lista_cl}}})

    elif subclass == 'Radiologia':
        for var in v:
            fil = {var_name:var}
            lista_rx.append(fil)
        super_filtro.append( {"radiological_tests": {"$elemMatch": {"$and":lista_rx}}})

    elif subclass == 'TestCovid':
        for var in v:
            fil = 	{"test_type":var_name}
            fil1 = {"result":var}
            lista_te.append(fil)
            lista_te.append(fil1)
        super_filtro.append({"coronavirus_tests": {"$elemMatch": {"$and":lista_te}}})

    elif subclass == 'Tratamiento':
         for i in range(len(v)):
            if i == 0:  #min
                fil = {"name":var_name}
                fil1 = {"dose":{"$gte":v[i]}}
                lista_dr.append(fil)
                lista_dr.append(fil1)

            elif i == 1: #max
                fil = {"name":var_name}
                fil1 = {"dose":{"$lte":v[i]}}
                lista_dr.append(fil)
                lista_dr.append(fil1)
         super_filtro.append({"prescriptions": {"$elemMatch":{"$and":lista_dr}}})

# Creacion de un unico filtro anidado
filtros_anidados =  {"$and": super_filtro}









# Selected variables to display coming from Dashboard
# Variables = ['Basic.height_cm','Basic.gender','Amoxicilina', 'Morphin', 'hemoglobine', 'Basic.Condiciones_Previas']
Variables = ['temperature_celsius']

v_lista = [] # to create the selection payload for the MongoDB query
v_lista_2 = [] # to know which ones are 2nd order --> to be deleted at the end of the code
v_post_sel = [] # to keep track of those variables that are not of 1st level and have to be selected later in python
for sel in Variables:

    dot = sel.find('.')
    if dot == -1: # not found --> in case no __.notation
        subclass = ch[sel]['Route']
        var_name = sel
    else:
        subclass = sel[:dot]
        var_name = sel[dot+1:]


    if subclass == 'Basic' and var_name != "Condiciones_Previas" and var_name not in v_lista:
        v_lista.append(var_name)

    elif subclass == 'Basic' and var_name == "Condiciones_Previas":
        v_post_sel.append(var_name)
        if "previous_conditions" not in v_lista:
            v_lista.append("previous_conditions")


    elif subclass == 'Analitica':
        if "lab_tests" not in v_lista:
            v_lista.append("lab_tests")
            v_lista_2.append("lab_tests")
        v_post_sel.append(sel)

    elif subclass == 'Clinico':
        if "clinical_updates" not in v_lista:
            v_lista.append("clinical_updates")
            v_lista_2.append("clinical_updates")
        v_post_sel.append(sel)

    elif subclass == 'Radiologia':
        if "radiological_tests" not in v_lista:
            v_lista.append("radiological_tests")
            v_lista_2.append("radiological_tests")
        v_post_sel.append(sel)

    elif subclass == 'TestCovid':
        if "coronavirus_tests" not in v_lista:
            v_lista.append("coronavirus_tests")
            v_lista_2.append("coronavirus_tests")
        v_post_sel.append(sel)

    elif subclass == 'Tratamiento':
        if "prescriptions" not in v_lista:
            v_lista.append("prescriptions")
            v_lista_2.append("prescriptions")
        v_post_sel.append(sel)




# Create the payload according to Mongo nomenclature
#filtro_MongoDB = {"filter": filtros_anidados, "select":v_lista}

filter_MongroDB = json.dumps(filtros_anidados, separators=(',',':'))
select_MongoDB = json.dumps(v_lista, separators=(',',':'))

payload = {"filter": filter_MongroDB, "select": select_MongoDB}


# Loading user and password from text file
# @Jesus: create file user_pass.yml with the following content (change password)
# user: demo
# password: you_know_it
# @Jesus: remember not to git it!!!

with open('user_pass.yml', 'r') as f:
    access = yaml.load(f, Loader=yaml.FullLoader)

# Perform the query
resp_filter = requests.get('https://backend-demo.cobig19.com/patient',
                           auth=(access['user'], access['password']),
                           params=payload)

if resp_filter.status_code == 200:
    data_filtered= resp_filter.json()

with open('db_output.json', 'w') as f:
    json.dump(data_filtered, f)

print('There are {} patients'.format(len(data_filtered)))
############################################ TILL HERE WORKS PERFECTLY



############################## DB not up to date, thus, structure does not mach with query request.

# Transform data into dataframe
data_fs = pd.DataFrame(data_filtered)

# Select data of 2nd and 3rd level that are stored in var: v_post_sel[] -- WITH THEIR TIMESTAMP!!! :D
for sel in v_post_sel:

    dot = sel.find('.')
    if dot == -1: # not found --> in case no __.notation
        subclass = ch[sel]['Route']
        var_name = sel
    else:
        subclass = sel[:dot]
        var_name = sel[dot+1:]

    if subclass == 'Basic' and var_name == "Condiciones_Previas": # It could only be the case of "previous_conditions", no timestamp in this case
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            valor = None
            prev = patient['previous_conditions']
            for (item, val) in prev.items():
                if item == 'name':
                    valor = val

            var_col.append(valor)
        dat[var_name]=var_col

    elif subclass == 'Analitica':
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            lab_tests = patient['lab_tests']
            for test in lab_tests:
                found =0
                valor = None
                time = None
                for (item, val) in test.items():
                    if item == 'timestamp':
                        time=val
                    if item == 'items':
                        for param in val:
                            for (ky, v) in param.items():
                                if ky=='parameter_key' and v==var_name:
                                    found = 1
                                if ky=='value':
                                    valor=v

                        if found ==1 :
                            value_array = np.append(value_array,valor)
                if found == 1:
                    time_array = np.append(time_array,time)

            var_col.append(pd.Series(value_array, name=var_name, index=time_array))
        dat[var_name]=var_col

    elif subclass == 'Clinico':
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            clinics = patient['clinical_updates']
            for updates in clinics:
                found =0
                valor = None
                time = None
                for (item, val) in updates.items():
                    if item == 'timestamp':
                        time=val

                    if item == var_name:
                        valor=val
                        found = 1

                if found ==1 :
                    value_array = np.append(value_array,valor)
                    time_array = np.append(time_array,time)

            var_col.append(pd.Series(value_array, name=var_name, index=time_array))
        dat[var_name]=var_col

    elif subclass == 'Radiologia':
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            rxs = patient['radiological_tests']
            for updates in rxs:
                found =0
                valor = None
                time = None
                for (item, val) in updates.items():
                    if item == 'timestamp':
                        time=val

                    if item == var_name:
                        valor=v
                        found = 1

                if found ==1 :
                    value_array = np.append(value_array,valor)
                    time_array = np.append(time_array,time)

            var_col.append(pd.Series(value_array, name=var_name, index=time_array))
        dat[var_name]=var_col

    elif subclass == 'TestCovid':
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            COV = patient['coronavirus_tests']
            for updates in COV:
                found =0
                valor = None
                time = None
                for (item, val) in updates.items():
                    if item == 'timestamp':
                        time=val

                    if item == "test_type" and val == var_name:
                        found = 1

                    if item == "result":
                        valor = val

                if found ==1 :
                    value_array = np.append(value_array,valor)
                    time_array = np.append(time_array,time)

            var_col.append(pd.Series(value_array, name=var_name, index=time_array))
        dat[var_name]=var_col

    elif subclass == 'Tratamiento': # date_end and interval not taken into account at this iteration.
        var_col = []
        dat=data_fs
        for index, patient in dat.iterrows():
            time_array = np.array([])
            value_array = np.array([])
            drugs = patient['prescriptions']
            for updates in drugs:
                found =0
                valor = None
                time = None
                for (item, val) in updates.items():
                    if item == 'date_start':
                        time=val

                    if item == "name" and val == var_name:
                        found = 1

                    if item == "dose":
                        valor = val

                if found ==1 :
                    value_array = np.append(value_array,valor)
                    time_array = np.append(time_array,time)

            var_col.append(pd.Series(value_array, name=var_name, index=time_array))
        dat[var_name]=var_col

# Droping the columns not needed, the ones with objects.
dat = dat.drop(columns=v_lista_2)
data_fs = dat






















