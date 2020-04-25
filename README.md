# data_reshaping
db_stateV2.py
uses the function in dummy_data.py to create 100 patients and then 
the performs the same analysis that db_state.py.
It creates a variable called "choices" for the dashboard method
"get_choices" and a variable called "variables" for the dashboard method
"get_variables"



db_state.py

To get all names of variables and their categories or max and mins, and
create a dictionary with such an structure that Marco's dashboard can
understand it.
(the first lines are to get info from the database and create some other,
these lines can be replaced by the function dummy_data)


dummy_data.py

A script to create dummy data in JSON format as it would be in MongoDB.
It creates a local variable where all the information of all the patients
is. This structure respects the data structure proposed in the V2 "Data
Structure proposal.pdf" made by Guille
