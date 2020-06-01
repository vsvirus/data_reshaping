import requests
import yaml
import json
import os
THIS_FILE_PATH = os.path.abspath(os.path.dirname(__file__))
import sys
sys.path.insert(0, THIS_FILE_PATH)
from linearize_db_utils import linearize

with open('user_pass.yml', 'r') as f:
    access = yaml.load(f, Loader=yaml.FullLoader)

data_connection = requests.get('https://backend-demo.cobig19.com/patient',
                               auth=(access['user'], access['password']))

if data_connection.status_code == 200:
    patients = data_connection.json()

keys = {}
choices = {}

for pat in patients:
    linearize(keys, choices, pat, '')

# Look for time variant
time_variant = []

for k in keys:
    splitted = k.split('.')
    if 'timestamp' in splitted:
        prefix = k.replace('.timestamp', '')
        time_variant.append(prefix)

for k in keys:
    found = False
    for p in time_variant:
        if k[:len(p)] == p:
            choices[k]['path_to_ts'] = '{}.timestamp'.format(p)
            keys[k] += '_tv'
            found = True
    if (not found) and ('_tv' not in keys[k]):
        keys[k] += '_tc'


variables = {
    'tc_bool': [],
    'tc_cat': [],
    'tc_num': [],
    'tv_bool': [],
    'tv_cat': [],
    'tv_num': [],
}

for k in keys:
    if keys[k] == 'bool_tc':
        variables['tc_bool'].append(k)
        choices[k]['type'] = 'tc_bool'
    elif keys[k] == 'cat_tc':
        variables['tc_cat'].append(k)
        choices[k]['type'] = 'tc_cat'
    elif keys[k] == 'num_tc':
        variables['tc_num'].append(k)
        choices[k]['type'] = 'tc_num'
    elif keys[k] == 'bool_tv':
        variables['tv_bool'].append(k)
        choices[k]['type'] = 'tv_bool'
    elif keys[k] == 'cat_tv':
        variables['tv_cat'].append(k)
        choices[k]['type'] = 'tv_cat'
    elif keys[k] == 'num_tv':
        variables['tv_num'].append(k)
        choices[k]['type'] = 'tv_num'

translation = {k: None for k in choices}

for k in choices:
    if choices[k]['condition'] is None:
        choices[k]['field_type'] = 'single_key'
    else:
        choices[k]['field_type'] = 'double_key'


CHOICES_FILE = os.path.join(THIS_FILE_PATH, 'data_tmp', 'choices.json')
VARIABLES_FILE = os.path.join(THIS_FILE_PATH, 'data_tmp', 'variables.json')
LINEARIZED_FILE = os.path.join(THIS_FILE_PATH, 'data_tmp', 'linearized.txt')
TRANSLATIONS_FILE = os.path.join(THIS_FILE_PATH, 'data_tmp', 'translation.json')

with open(LINEARIZED_FILE, 'w') as f:
    for el in keys:
        f.write('{}: {}\n'.format(el, keys[el]))

with open(CHOICES_FILE, 'w') as outfile:
    json.dump(choices, outfile)

with open(VARIABLES_FILE, 'w') as outfile:
    json.dump(variables, outfile)

with open(TRANSLATIONS_FILE, 'w') as outfile:
    json.dump(translation, outfile)
