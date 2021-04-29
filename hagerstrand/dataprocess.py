import pandas as pd
import json
import ipywidgets as widgets
import hagerstrand as hs


class ExtendedDataFrame(pd.DataFrame):
    """This ExtendedDataFrame class inherits the pandas DataFrame class

    Args:
        pd (pd.DataFrame()): A pandas DataFrame
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return ExtendedDataFrame

    def deduplicate(self, columns=None):
        """Drops duplicate records and resets the index of the ExtendedDataFrame

        Args:
            columns (list, optional): Columns for which to identify dupulicate records. Defaults to None.

        Returns:
            ExtendedDataFrame: A de-deuplicated ExtendedDataFrame with the index reset.
        """
        if columns == None:
            df = self.drop_duplicates()
            df = df.reset_index(drop=True)
            return df
        else:
            df = self.drop_duplicates(subset=columns)
            df = df.reset_index(drop=True)
            return df

    def jsoncol_newdf(self):
        """Unpack a JSON column and return a new ExtendedDataFrame

        Returns:
            ExtendedDataFrame: A new ExtendedDataFrame of an unpacked JSON column.
        """
        df = unpack_json(self)
        return df

    def jsoncol_merge(self):
        """Unpack a JSON column and merge to the existing DataFrame

        Returns:
            ExtendedDataFrame: A new ExtendedDataFrame that includes the original DataFrame and the unpacked JSON column.
        """
        df = unpack_json_and_merge(self)
        return df


# THE FOLLOWING FUNCTIONS ARE MODIFIED FROM https://github.com/SafeGraphInc/safegraph_py


def load_json_nan(df, json_col):
    """Load a JSON file even if there are NaNs.

    Args:
        df (pd.DataFrame): The DataFrame containing the JSON column to be loaded.
        json_col (str): The JSON column to be loaded.

    Returns:
        df (pd.Series): A pd.Series of a JSON column
    """
    return df[json_col].apply(lambda x: json.loads(x) if type(x) == str else x)


def unpack_json(
    df,
    json_column="visitor_home_cbgs",
    index_name=None,
    key_col_name=None,
    value_col_name=None,
):
    """Unpack a JSON column from a SafeGraph Patterns dataset.

    Args:
        df (pd.DataFrame): DataFrame containing the JSON column to be unpacked.
        json_column (str, optional): JSON column to be unpacked. Defaults to 'visitor_home_cbgs'.
        index_name (str, optional): Index name for new ExtendedDataFrame. Defaults to None.
        key_col_name (str, optional): Key name for new ExtendedDataFrame. Defaults to None.
        value_col_name (str, optional): Value name for new ExtendedDataFrame. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame of an unpacked JSON column.
    """
    import numpy as np

    # these checks are inefficent for multithreading, but it's not a big deal
    if key_col_name is None:
        key_col_name = json_column + "_key"
    if value_col_name is None:
        value_col_name = json_column + "_value"
    if df.index.unique().shape[0] < df.shape[0]:
        raise ("ERROR -- non-unique index found")
    df = df.copy()
    df[json_column + "_dict"] = load_json_nan(df, json_column)
    all_sgpid_cbg_data = []  # each cbg data point will be one element in this list
    if index_name is None:
        for index, row in df.iterrows():
            if row[json_column] == "" or pd.isnull(row[json_column]):
                next
            else:
                this_sgpid_cbg_data = [
                    {"orig_index": index, key_col_name: key, value_col_name: value}
                    for key, value in row[json_column + "_dict"].items()
                ]
                all_sgpid_cbg_data = all_sgpid_cbg_data + this_sgpid_cbg_data
    else:
        for index, row in df.iterrows():
            if row[json_column] == "" or pd.isnull(row[json_column]):
                next
            else:
                temp = row[index_name]
                this_sgpid_cbg_data = [
                    {
                        "orig_index": index,
                        index_name: temp,
                        key_col_name: key,
                        value_col_name: value,
                    }
                    for key, value in row[json_column + "_dict"].items()
                ]
                all_sgpid_cbg_data = all_sgpid_cbg_data + this_sgpid_cbg_data

    all_sgpid_cbg_data = pd.DataFrame(all_sgpid_cbg_data)
    all_sgpid_cbg_data.set_index("orig_index", inplace=True)
    return all_sgpid_cbg_data


def unpack_json_and_merge(
    df,
    json_column="visitor_home_cbgs",
    key_col_name="visitor_home_cbg",
    value_col_name="cbg_visitor_name",
    keep_index=False,
):
    """Unpack a JSON column from a SafeGraph Patterns dataset.

    Args:
        df (pd.DataFrame): DataFrame containing the JSON column to be unpacked
        json_column (str, optional): JSON column to be unpacked. Defaults to 'visitor_home_cbgs'.
        key_col_name (str, optional): Key name for new ExtendedDataFrame. Defaults to 'visitor_home_cbg'.
        value_col_name (str, optional): Value name for new ExtendedDataFrame. Defaults to 'cbg_visitor_name'.
        keep_index (bool, optional): Keep or do not keep the original index. Defaults to False.

    Returns:
        pd.DataFrame: DataFrame containing the original DataFrame and the unpacked JSON column as additional columns.
    """
    if keep_index:
        df["index_original"] = df.index
    df.reset_index(drop=True, inplace=True)  # Every row must have a unique index
    df_exp = unpack_json(
        df,
        json_column=json_column,
        key_col_name=key_col_name,
        value_col_name=value_col_name,
    )
    df = df.merge(df_exp, left_index=True, right_index=True).reset_index(drop=True)
    return df


def unique_sorted_values_plus_ALL(array):
    """Obtain a sorted array of all unique values in an array, including an additional value of 'ALL' to denote all values.

    Args:
        array (list|pd.Series|np.array): An array of values.

    Returns:
        list: A sorted array of unique values including an additional value of 'ALL'.
    """
    unique = array.unique().tolist()
    unique.sort()
    unique.insert(0, "ALL")
    return unique


def unique_sorted_columns_plus_ALL(gj):
    """Obtain a sorted array of all columns in a GeoJSON, including an additional value of 'ALL' to denote all values.

    Args:
        gj (GeoJSON): A GeoJSON.

    Returns:
        list: A sorted array of unique column names including an additional value of 'ALL'.
    """
    if isinstance(gj, json):
        array = gpd.GeoDataFrame.from_features(gj)
        unique = array.unique().tolist()
        unique.sort()
        unique.insert(0, "ALL")
        return unique

    else:
        raise TypeError("The provided argument for gj must be of type json.")


# Come back to this: https://stackoverflow.com/questions/42562895/return-dataframe-using-ipywidgets-button
