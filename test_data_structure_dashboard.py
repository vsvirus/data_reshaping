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
        """
        This method returns the uniques options in the variables. If time and
        event_zero are None then it works only with tcant variables, if
        both defined, it looks for a snapshot in the data.
        If numeric variables, it returns min and max.

        Parameters
        ----------
        variables : list(str)
            List of variables to return the var_info.
        time : int
            Time stamp
        event_zero : str
            Event to start counting the days after

        Returns
        -------
        dict
            {variable: {type: 'type', value: var_info}}
        """

        # check if the file is updated
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

        if plot_type in ['Histogram', 'Scatter', 'Bar', 'Box']:
            data = self._prepare_data_for_time_constant(db_response, variables)
        elif plot_type in ['TimeSeries']:
            data = self._prepare_data_for_time_series(db_response, time_variant_opt)
        elif plot_type in ['HeatMap']:
            data = self._prepare_data_for_heatmap(db_response, time_variant_opt)
        else:
            raise ValueError('Plot type {} not handled'.format(plot_type))

        return data

    def _prepare_data_for_time_constant(self, db_response, variables):

        # data = pd.DataFrame(columns=variables + 'ID')

        # for el in db_response:
        #     el_content = {}
        #     el_content['ID'] = el['_id']
        #     for v in variables:
        #         path_to_value = self._var_info[v]['path_to_value']
        #         el_content[v] = el[]


        pass

    def _prepare_data_for_time_series(self, db_response, time_variant_opt):
        pass

    def _prepare_data_for_heatmap(self, db_response, time_variant_opt):
        pass

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
        ]

        supported_variables = [x['value'] for x in self.get_variables(types=supported_types)]

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
        'health_provider_id',
        'height_cm',
        'lab_tests.leucocytes_value',
        'clinical_updates.symptoms',
        'radiological_tests.has_pneumonia',
        'coronavirus_tests.result',
        ]

    data = Data(access=access_file, var_info=var_info_file, variables=variables_file, translation=translation_file)

    with open('tmp.json', 'w') as f:
        json.dump(data._filter_and_select(filter_from_dashboard, select_from_dashboard), f)