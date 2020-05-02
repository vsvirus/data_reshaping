#%%
import requests
import yaml
import json
import pandas as pd
import datetime

#%%
with open('user_pass.yml', 'r') as f:
    access = yaml.load(f, Loader=yaml.FullLoader)

pay = json.dumps({"$and":[{"gender":'male' }]}, separators=(',', ':'))

data_connection = requests.get('https://backend-demo.cobig19.com/patient',
                               auth=(access['user'], access['password']),
                               params={"filter":pay})

if data_connection.status_code == 200:
    patients = data_connection.json()

with open('db_output.json', 'w') as f:
    json.dump(patients, f)

#%%
event_zero_time = datetime.datetime.strptime('2020-04-09T10:25:34.000Z', '%Y-%m-%dT%H:%M:%S.000Z')

data = {
    '2020-04-07T12:25:32.000Z': 10.5,
    '2020-04-08T09:25:54.000Z': 1.2,
    '2020-04-08T21:13:34.000Z': 14.2,
    '2020-04-09T10:25:34.000Z': 24.2,
    '2020-04-09T14:25:34.000Z': 23.1,
    '2020-04-09T15:25:34.000Z': 12.1,
    '2020-04-13T12:25:34.000Z': 12.3,
}

data_series = pd.Series(data)

# Transform index to time stamp. TODO: handle milliseconds
data_series.index = pd.to_datetime(data_series.index, format='%Y-%m-%dT%H:%M:%S.000Z')

#%%
data_series.index = data_series.index - event_zero_time

#%%
data_series.index = data_series.index.round('1D')

#%%
# Change the function for categorical data
aggregated_data_series = data_series.resample('1D').mean()

#%%
# This works only if regular time step..maybe it should be done at the dataframe level
# Use fill_na for categorical
# filled_time_series = aggregated_data_series.interpolate('linear')

#%%
all_patients = pd.DataFrame(index=pd.timedelta_range(start='-10 days', end='10 days', freq='1D'))

# %%
for i in range(10):
    all_patients[i] = aggregated_data_series

# %%
all_patients = all_patients.interpolate('linear')

# %%
# Calculate quantiles
quantiles = all_patients.quantile(q=[0.05, 0.5, 0.95], axis=1)
# %%
