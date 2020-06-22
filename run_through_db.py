import requests
import yaml
import json

with open('user_pass.yml', 'r') as f:
    access = yaml.load(f, Loader=yaml.FullLoader)

data_connection = requests.get('https://backend-demo.cobig19.com/patient',
                               auth=(access['user'], access['password']),
                               )

if data_connection.status_code == 200:
    patients = data_connection.json()

variables = []

for pat in patients:
    for el in pat.keys():
        if isinstance(pat[el], list) or isinstance(pat[el], dict):
            look_into(pat[el], el, variables)
        else:
            variables.append(el)

def look_into(data, el, variables):
    pass