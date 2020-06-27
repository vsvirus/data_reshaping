import yaml
import json
import os
import re  # Regular expressions
import requests
import pandas as pd

# TODO: error handling...but we don't make mistakes :-P

class Data():

    def __init__(self, access, var_info, variables, translation):
        """
        access: path of jaml with user and pass
        var_info: path of json with var_info
        variables: path of json with variables
        translation: path of json with translation
        """

        # Get access to db
        with open(access, 'r') as f:
            self._access = yaml.load(f, Loader=yaml.FullLoader)

        self._var_info_name = var_info
        self._variables_name = variables
        self._translation_name = translation
        self._db_url = 'https://backend-demo.cobig19.com/patient'

        self._load_info_files()

    def _load_info_files(self):

        print('DB is loading')  # TODO: remove

        with open(self._var_info_name, 'r') as f:
            self._var_info = json.load(f)

        self._var_info_time = os.path.getmtime(self._var_info_name)

        with open(self._variables_name, 'r') as f:
            self._variables = json.load(f)

        self._variables_time = os.path.getmtime(self._variables_name)

        with open(self._translation_name, 'r') as f:
            self._translation = json.load(f)

        self._translation_time = os.path.getmtime(self._translation_name)

        # Create variables in the form name: label
        var_new = {}
        for k in self._variables:
            var_new[k] = []
            for var_name in self._variables[k]:
                if self._translation[var_name] is not None:
                    var_new[k].append({
                        'value': var_name,                     # Displayed on the dashboard
                        'label': self._translation[var_name],  # Used internally
                        }
                    )
        self._variables = var_new

    def get_variables(self, types=None):
        """
        This method returns the names of the variables present in the database.

        Parameters
        ----------
        types : list(str)
            List of types of variables to get. If None it returns all the
            variables.
            Possible types:
                - 'tc_bool'
                - 'tc_cat'
                - 'tc_num'
                - 'tv_bool'
                - 'tv_cat'
                - 'tv_num'
                - 'events'

        Returns
        -------
        list
            List with the names of the variables
        """

        # check if the file is updated
        if (os.path.getmtime(self._var_info_name) != self._var_info_time or
            os.path.getmtime(self._variables_name) != self._variables_time or
            os.path.getmtime(self._translation_name) != self._translation_time):

           self._load_info_files()

        output = []
        if types is None:
            types = self._variables.keys()

        for t in types:
            for v in self._variables[t]:
                output.append(v)

        return output

    def get_var_info(self, variables):

        # check if the file is updated
        if (os.path.getmtime(self._var_info_name) != self._var_info_time or
            os.path.getmtime(self._variables_name) != self._variables_time or
            os.path.getmtime(self._translation_name) != self._translation_time):

           self._load_info_files()

        output = {}

        for v in variables:

            output[v] = self._var_info[v]

        return output

    def get_patients_ids(self):
        """
        This method returns the list of patients.

        Returns
        -------
        list(str)
            List of the patients in the database
        """

        return self._var_info['patient_id']['value']  #TODO: this shouldn't be hardcoded

    def get_data(self, variables, filters, plot_type, time_variant_opt=None):
        """
        This method returns the data that are strictly needed for the plot.

        Parameters
        ----------
        filters : dict(str: list)
            Filters to apply to the data. Key: variable, value: options
        plot_options : dict(str: list)
            variables for the plot
        plot_type : str
            Type of plot

        Returns
        -------
        Depends on the type of plot
        """

        db_response = self._filter_and_select(filt=filters, sel=variables)  # It is a JSON

        # Select quickly the mogo ids of patients
        ids = [pat['_id'] for pat in db_response]

        data_as_table = pd.DataFrame(index=ids, columns=variables)

        for var in variables:
            search_path = self._var_info[var]['path_to_value'].split('.')
            condition_path = None if self._var_info[var]['condition'] is None else self._var_info[var]['condition'].split('==')[0].split('.')
            condition_equality = None if condition_path is None else self._var_info[var]['condition'].split('==')[1]
            if 'tc' in self._var_info[var]['type']:
                for pat in db_response:
                    pat_var = self._reshape_constant(pat, search_path, condition_path, condition_equality)
                    data_as_table.loc[pat['_id']][var] = pat_var
            elif 'tv' in self._var_info[var]['type']:
                timestamp_path = self._var_info[var]['path_to_timestamp'].split('.')
                for pat in db_response:
                    pat_var = self._reshape_variant(pat, search_path, condition_path, condition_equality, timestamp_path)
                    data_as_table.loc[pat['_id']][var] = pat_var[2]

        if plot_type in ['Constant']:
            # I just return the data_as_table which, when coupled with the dashboard will contain only constant variables
            return data_as_table
        elif plot_type in ['Variant_num']:
            return self._polish_data_num_variant(data_as_table, time_variant_opt, var_to_plot=variables[0]) # The dashboard asks only for 1 variable
        elif plot_type in ['Variant_cat']:
            return self._polish_data_cat_variant(data_as_table, time_variant_opt, var_to_plot=variables[0]) # The dashboard asks only for 1 variable

    def _polish_data(self, data_as_table, time_variant_opt, var_to_plot, agg_func):
        # 1) Get for each patient time reference
        patients_in_table = data_as_table.index.to_list()
        event_path_to_value = self._var_info[time_variant_opt['event_zero']]['path_to_value']

        db_output = self._filter_and_select(filt={'_id': patients_in_table}, sel=[event_path_to_value])

        data_as_table['e0'] = None

        for el in db_output:
            data_as_table.loc[el['_id']]['e0'] = self._reshape_constant(el, event_path_to_value.split('.'), None, None)

        # 2) Scale all data given the time reference

        all_patients = pd.DataFrame(index=pd.timedelta_range(start=time_variant_opt['start_plot'], end=time_variant_opt['end_plot'], freq='1D'))

        for row in data_as_table.iterrows():
            data = row[var_to_plot]
            data_series = pd.Series(data)
            data_series.index = pd.to_datetime(data_series.index)# TODO: force format (faster), format='%Y-%m-%dT%H:%M:%S.000Z')
            event_zero_time = datetime.datetime.strptime(row['e0'])
            data_series.index = data_series.index - event_zero_time
            data_series.index = data_series.index.round('1D')
            if agg_func == 'mean':
                aggregated_data_series = data_series.resample('1D').mean()
            else:
                raise KeyError()

            all_patients[row.index] = aggregated_data_series

        # 3) Get patients to plot over (check first if they are in already in the table)

        # 4) For patients not in table, scale

        return all_patients

    def _polish_data_num_variant(self, data_as_table, time_variant_opt, var_to_plot):

        all_patients, specific_patients = self._polish_data(data_as_table, time_variant_opt, var_to_plot, agg_func='mean')

        # DO the aggregation (quantiles)

        return all_patients, specific_patients

    def _polish_data_cat_variant(self, data_as_table, time_variant_opt, var_to_plot):

        all_patients, specific_patients = self._polish_data(data_as_table, time_variant_opt, var_to_plot)

        # DO the aggregation (quantiles)

        return all_patients, specific_patients

    def _reshape_constant(self, pat, search_path, condition_path, condition_equality):
        # Important assumption: search_path and condition_path are equal until the second-last
        # e.g. sp: a.b.c.d
        #      cp: a.b.c.e

        if condition_path is not None:
            if search_path[0] != condition_path[0] and len(search_path) > 1:
                raise ValueError('Unsupported case')

        if len(search_path) > 1:
            result = pat[search_path[0]]
        else:
            result = pat

        if isinstance(result, dict) and len(search_path) > 1:
            if condition_path is None:
                value = self._reshape_constant(result, search_path[1:], condition_path, condition_equality)
            else:
                value = self._reshape_constant(result, search_path[1:], condition_path[1:], condition_equality)
        elif isinstance(result, list) and ((not isinstance(result[0], bool)) or (not isinstance(result[0], str))):
            for res in result:
                if condition_path is None:
                    val = self._reshape_constant(res, search_path[1:], condition_path, condition_equality)
                else:
                    val = self._reshape_constant(res, search_path[1:], condition_path[1:], condition_equality)
                if val is not None:
                    value = val
        else:
            # We have reached the value
            value = result[search_path[0]]

            if condition_path is not None:
                condition = result[condition_path[0]]
                if str(condition) == condition_equality:
                    return value
                else:
                    return None
            else:
                return value

        return value

    def _reshape_variant(self, pat, search_path, condition_path, condition_equality, timestamp_path, timestamp=None, res_dict=None):
        # Important assumption: search_path and condition_path are equal until the second-last
        # e.g. sp: a.b.c.d
        #      cp: a.b.c.e
        # Important assumption 2: timestamp_path is shorter/equal than search path and equal until second last
        # e.g. sp: a.b.c.d.e
        #      tp: a.b.f

        if res_dict is None:
            res_dict = {}

        if condition_path is not None:
            if search_path[0] != condition_path[0] and len(search_path) > 1:
                raise ValueError('Unsupported case')

        if len(search_path) > 1:
            result = pat[search_path[0]]
        else:
            result = pat

        if len(timestamp_path) == 1:
            timestamp = pat[timestamp_path[0]]

        if isinstance(result, dict) and len(search_path) > 1:
            if condition_path is None:
                value, timestamp = self._reshape_variant(result, search_path[1:], condition_path, condition_equality, timestamp_path[1:], timestamp, res_dict)[:2]
            else:
                value, timestamp = self._reshape_variant(result, search_path[1:], condition_path[1:], condition_equality, timestamp_path[1:], timestamp, res_dict)[:2]
        elif isinstance(result, list) and ((not isinstance(result[0], bool)) or (not isinstance(result[0], str))):
            for res in result:
                if condition_path is None:
                    val, timestamp = self._reshape_variant(res, search_path[1:], condition_path, condition_equality, timestamp_path[1:], timestamp, res_dict)[:2]
                else:
                    val, timestamp = self._reshape_variant(res, search_path[1:], condition_path[1:], condition_equality, timestamp_path[1:], timestamp, res_dict)[:2]
                if val is not None:
                    value = val
                    if timestamp not in res_dict.keys():
                        res_dict[timestamp] = value
        else:
            # We have reached the value
            value = result[search_path[0]]

            if condition_path is not None:
                condition = result[condition_path[0]]
                if str(condition) == condition_equality:
                    return value, timestamp
                else:
                    return None, timestamp
            else:
                return value, timestamp

        return value, timestamp, res_dict

    def _filter_and_select(self, filt=None, sel=None):

        if filt is not None:
            filt = self._add_info_to_dashboard_filters(filt=filt)
            filt = self._build_filter(filt=filt)

        if sel is not None:
            sel = self._build_selection(sel=sel)

        data_from_db = self._get_data_out_of_mongo(filt=filt, sel=sel)

        return data_from_db

    def _build_selection(self, sel):
        """
        This extends the field needed
        """

        sel_out = []

        for s in sel:

            # Add path to value
            sel_out.append(self._var_info[s]['path_to_value'])

            # Add timestamp, in case
            if self._var_info[s]['path_to_timestamp'] is not None:
                sel_out.append(self._var_info[s]['path_to_timestamp'])

            # Add path to condition
            if self._var_info[s]["condition"] is not None:
                sel_out.append(self._var_info[s]["condition"].split('==')[0])

        return sel_out

    def _build_filter(self, filt):

        supported_types = [
            'tc_cat',
            'tc_bool',
            'tc_num',
            'events',
        ]

        supported_variables = [x['value'] for x in self.get_variables(types=supported_types)] + ['_id']

        for key in filt:
            if key not in supported_variables:
                raise KeyError('Filters work only for time constant')

        # Single key. Atomic filter for range
        def getDictFilterRangeSingleKey(path_to_value, minmax):
            dictFilter = {path_to_value: {"$gte": min(minmax), "$lte": max(minmax)}}
            return dictFilter

        # Atomic filter for categorical
        def getDictFilterCategoricalSingleKey(path_to_value, options):
            dictFilter = {path_to_value: {"$in": options}}
            return dictFilter

        # Atomic filter for bool
        def getDictFilterBoolSingleKey(path_to_value, truefalse):
            dictFilter = {path_to_value: truefalse}
            return dictFilter

        # dictItem = filt["gender"]
        def getDictFilter(dictItem):
            variableType = dictItem["type"]

            # Build filter for booleans
            if "bool" in variableType:
                dictFilter = getDictFilterBoolSingleKey(path_to_value=dictItem["path_to_value"],
                                            truefalse=dictItem["value"])

            # Build filter for categorical
            elif "cat" in variableType:
                dictFilter = getDictFilterCategoricalSingleKey(path_to_value=dictItem["path_to_value"],
                                                    options=dictItem["value"])
            # Build filter for numeric
            elif "num" in variableType:
                dictFilter = getDictFilterRangeSingleKey(path_to_value=dictItem["path_to_value"],
                                                minmax=dictItem["value"])
            else:
                raise Exception("Unknown variable type: {}".format(variableType))

            return dictFilter

        list_filters = []

        for _, item in filt.items():
            list_filters.append(getDictFilter(item))

        #fullFilter = {"$elemMatch" : {"$and": listFilters}}
        # TODO: integrate $elementMatch
        fullFilter = {"$and": list_filters}

        return fullFilter

    def _add_info_to_dashboard_filters(self, filt):
        """
        filt: query from dashboard
        """

        richer_filt = {}
        for key in filt:
            richer_filt[key] = self._var_info[key]
            richer_filt[key]['value'] = filt[key]

        return richer_filt

    def _get_data_out_of_mongo(self, filt=None, sel=None):
        """
        filt: filter from dashboard with more info added from _add_info_to_dashboard_filters
        """

        payload = {}

        if filt is not None:
            filter_MongoDB = json.dumps(filt, separators=(',',':'))
            payload['filter'] = filter_MongoDB

        if sel is not None:
            select_MongoDB = json.dumps(sel, separators=(',',':'))
            payload['select'] = select_MongoDB

        auth = (self._access["user"], self._access["password"])

        data_connection = requests.get(self._db_url, auth=auth, params=payload)
        if data_connection.status_code == 200:
            patients = data_connection.json()
        else:
            raise ConnectionRefusedError(data_connection.status_code)

        return patients

if __name__ == "__main__":
    THIS_FOLDER = os.path.abspath(os.path.dirname(__file__))
    var_info_file = os.path.join(THIS_FOLDER, 'data_tmp', 'choices.json')
    variables_file = os.path.join(THIS_FOLDER, 'data_tmp', 'variables.json')
    access_file = os.path.join(THIS_FOLDER, 'user_pass.yml')
    translation_file = os.path.join(THIS_FOLDER, 'data_tmp', 'translation.json')

    filter_from_dashboard = {'gender': ['female']}
    select_from_dashboard = [
        # 'health_provider_id',
        # 'height_cm',
        'lab_tests.leucocytes_value',
        # 'clinical_updates.symptoms',
        # 'radiological_tests.has_pneumonia',
        # 'coronavirus_tests.result',
        ]

    data = Data(access=access_file, var_info=var_info_file, variables=variables_file, translation=translation_file)

    data.get_data(variables=select_from_dashboard, filters=filter_from_dashboard, plot_type='Variant_num', time_variant_opt={'event_zero': 'date_of_first_symptoms', 'start_plot': '-10 days', 'end_plot': '10 days'})

    # with open('tmp.json', 'w') as f:
    #     json.dump(data._filter_and_select(filter_from_dashboard, select_from_dashboard), f, indent=4)