# data_reshaping

filter_creator.py

takes the filter that the dashboard generates, and transforms it into MongoDB query
that the endpoint can interpret.
Same for variables selected.
From the data that the DB sends back, a second level selection of variables is performed,
presenting time variables in pd.Series format, and all the structure as DataFrame.
(DB only allows by now a first level variable selection, thus, deeper selections are performed 
in this side)



db_stateV2.py

uses the function in dummy_data.py to create patients and then 
the get all names of variables and their categories or max and mins, and
create a dictionary with such an structure that Marco's dashboard can
understand it.
It creates a variable called "choices" for the dashboard method
"get_choices" and a variable called "variables" for the dashboard method
"get_variables".

choices = {name_var: {'type', 'value', 'route'}}
variables = {'tc_var': [variables correspondientes], ...}

Route indicates the parent of that variable.


dummy_data.py

A script to create dummy data in JSON format as it would be in MongoDB.
It creates a local variable where all the information of all the patients
is.
