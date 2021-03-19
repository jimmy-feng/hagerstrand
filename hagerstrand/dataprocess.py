import pandas as pd
import json

#@pd.api.extensions.register_dataframe_accessor("dataprocess")
class ExtendedDataFrame(pd.DataFrame):

    def __init__(self, *args, **kwargs):    
        super(ExtendedDataFrame, self).__init__(*args, **kwargs)   
    
    @property
    def _constructor(self):
        return ExtendedDataFrame

    def deduplicate(self, columns=None):
        # Drop duplicate rows and reset index

        if columns==None:
            df = self.drop_duplicates()
            df = df.reset_index(drop=True)
            return df
        else:
            df = self.drop_duplicates(subset=columns)
            df = df.reset_index(drop=True)            
            return df

    def jsoncol_newdf(self):
        # Unpack a JSON column and return a new DataFrame
        df = unpack_json(self)
        return df

    def jsoncol_merge(self):
        # Unpack a JSON column and merge to the existing DataFrame
        df = unpack_json_and_merge(self)
        return df
     

# THE FOLLOWING FUNCTIONS ARE MODIFIED FROM https://github.com/SafeGraphInc/safegraph_py

def load_json_nan(df, json_col):
  return df[json_col].apply(lambda x: json.loads(x) if type(x) == str else x)


def unpack_json(df, json_column='visitor_home_cbgs', index_name= None, key_col_name=None,
                         value_col_name=None):
    
    import numpy as np
    
    # these checks are a inefficent for multithreading, but it's not a big deal
    if key_col_name is None:
        key_col_name = json_column + '_key'
    if value_col_name is None:
        value_col_name = json_column + '_value'
    if (df.index.unique().shape[0] < df.shape[0]):
        raise ("ERROR -- non-unique index found")
    df = df.copy()
    df[json_column + '_dict'] = load_json_nan(df,json_column)
    all_sgpid_cbg_data = []  # each cbg data point will be one element in this list
    if index_name is None:
        for index, row in df.iterrows():
            if row[json_column] == '' or pd.isnull(row[json_column]):
                next
            else:
                this_sgpid_cbg_data = [{'orig_index': index, key_col_name: key, value_col_name: value} for key, value in
                                row[json_column + '_dict'].items()]
                all_sgpid_cbg_data = all_sgpid_cbg_data + this_sgpid_cbg_data
    else:
        for index, row in df.iterrows():
            if row[json_column] == '' or pd.isnull(row[json_column]):
                next
            else:
                temp = row[index_name]
                this_sgpid_cbg_data = [{'orig_index': index, index_name:temp, key_col_name: key, value_col_name: value} for key, value in
                               row[json_column + '_dict'].items()]
                all_sgpid_cbg_data = all_sgpid_cbg_data + this_sgpid_cbg_data
    
    all_sgpid_cbg_data = pd.DataFrame(all_sgpid_cbg_data)
    all_sgpid_cbg_data.set_index('orig_index', inplace=True)
    return all_sgpid_cbg_data


def unpack_json_and_merge(df, json_column='visitor_home_cbgs', key_col_name=None,
                         value_col_name=None, keep_index=False):
    if (keep_index):
        df['index_original'] = df.index
    df.reset_index(drop=True, inplace=True)  # Every row must have a unique index
    df_exp = unpack_json(df, json_column=json_column, key_col_name=key_col_name, value_col_name=value_col_name)
    df = df.merge(df_exp, left_index=True, right_index=True).reset_index(drop=True)
    return df