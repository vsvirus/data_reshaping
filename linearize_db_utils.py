def linearize(keys, choices, item, name):
    # Handle bad db
    if name == 'previous_conditions':
        handle_previous_conditions(keys, choices, item, name)
    elif name == 'lab_tests':
        handle_lab_test(keys, choices, item, name)
    elif name == 'prescriptions':
        handle_prescriptions(keys, choices, item, name)

    # Handle regular db
    elif isinstance(item, dict):
        for i in item:
            if len(name) == 0:
                linearize(keys, choices, item[i], '{}'.format(i))
            else:
                linearize(keys, choices, item[i], '{}.{}'.format(name, i))
    elif isinstance(item, list):
        for i, el in enumerate(item):
            linearize(keys, choices, el, name)
    else:  # I can populate
        if isinstance(item, str):  # Categorical
            if name not in keys:
                keys[name] = 'cat'
                choices[name] = {'type': None, 'value': [], 'path_to_value': name, 'path_to_timestamp': None, 'condition': None}
            if item not in choices[name]['value']:
                choices[name]['value'].append(item)
        elif isinstance(item, bool):  # Boolean
            if name not in keys:
                keys[name] = 'bool'
                choices[name] = {'type': None, 'value': [True, False], 'path_to_value': name, 'path_to_timestamp': None, 'condition': None}
        elif isinstance(item, float) or isinstance(item, int):  # Numeric
            if name not in keys:
                keys[name] = 'num'
                choices[name] = {'type': None, 'value': [], 'path_to_value': name, 'path_to_timestamp': None, 'condition': None}
            if len(choices[name]['value']) == 0:
                choices[name]['value'] = [item, item]
            else:
                if item < choices[name]['value'][0]:
                    choices[name]['value'][0] = item
                elif item > choices[name]['value'][1]:
                    choices[name]['value'][1] = item
        else:
            raise TypeError('Unsupported type: {}'.format(type(item)))

def handle_previous_conditions(keys, choices, item, name):
    if name not in keys:
        keys[name] = 'cat'
        choices[name] = {'type': None, 'value': [], 'path_to_value': '{}.name'.format(name), 'path_to_timestamp': None, 'condition': None}

    for i in item:
        if i['name'] not in choices[name]['value']:
            choices[name]['value'].append(i['name'])

def handle_lab_test(keys, choices, item, name):
    for test in item:
        for single_test in test['items']:
            par_name = single_test['parameter_key']
            par_value = single_test['value']

            if '{}.{}_value'.format(name, par_name) not in keys:
                keys['{}.{}_value'.format(name, par_name)] = 'num_tv'
                choices['{}.{}_value'.format(name, par_name)] = {'type': None, 'value': [],
                                                                 'path_to_value': '{}.items.value'.format(name),
                                                                 'path_to_timestamp': '{}.timestamp'.format(name),
                                                                 'condition': '{}.items.parameter_key=={}'.format(name, par_name)}

            if '{}.{}_out_of_bounds'.format(name, par_name) not in keys:
                keys['{}.{}_out_of_bounds'.format(name, par_name)] = 'bool_tv'
                choices['{}.{}_out_of_bounds'.format(name, par_name)] = {'type': None, 'value': [True, False],
                                                                         'path_to_value': '{}.items.is_out_of_bounds'.format(name),
                                                                         'path_to_timestamp': '{}.timestamp'.format(name),
                                                                         'condition': '{}.items.parameter_key=={}'.format(name, par_name)}

            if len(choices['{}.{}_value'.format(name, par_name)]['value']) == 0:
                choices['{}.{}_value'.format(name, par_name)]['value'] = [par_value, par_value]
            else:
                if par_value < choices['{}.{}_value'.format(name, par_name)]['value'][0]:
                    choices['{}.{}_value'.format(name, par_name)]['value'][0] = par_value
                elif par_value > choices['{}.{}_value'.format(name, par_name)]['value'][1]:
                    choices['{}.{}_value'.format(name, par_name)]['value'][1] = par_value

def handle_prescriptions(keys, choices, item, name):
    pass