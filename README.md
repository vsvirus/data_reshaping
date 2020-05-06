# data_reshaping

filter_creator.py

takes the filter that the dashboard generates, and transforms it into MongoDB query
that the endpoint can interpret.
Same for variables selected.
From the data that the DB sends back, a second level selection of variables is performed,
presenting time variables in pd.Series format, and all the structure as DataFrame.
(DB only allows by now a first level variable selection, thus, deeper selections are performed 
in this side) (it reads "choices.txt" as support info)
For the variables that are not of 1st level, a selection is done in the Python side, data
is transformed in to the dataframes "dat" and "data_fs" (they are identical). These, new selections
are appended to the dataframe, and in case of being time variant, they are appended as pd.Series for
each patient.



db_stateV2.py

reads the file "dummy_data.txt" and then 
the get all names of variables and their categories or max and mins, and
create a dictionary with such an structure that Marco's dashboard can
understand it.
It creates a variable called "choices" for the dashboard method
"get_choices" and a variable called "variables" for the dashboard method
"get_variables".

---choices = {name_var: {'type', 'value', 'route'}}
---variables = {'tc_var': [variables correspondientes], ...}

Route indicates the parent of that variable.
It creates two files: "choices.txt" and "variables.txt"


dummy_data.py

A script to create dummy data in JSON format as it would be in MongoDB.
It creates a local variable where all the information of all the patients
is, and it is stored in "dummy_data.txt"
