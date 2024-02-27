
import pandas as pd

def check_and_create_column(df, column_name, default_value="classes"):
    if column_name not in df.columns:
        df[column_name] = default_value
    return df


def get_values_as_list(df, column_name):
    values_list = df[column_name].dropna().tolist()
    if not values_list:
        return []
    return values_list


def replace_values_in_column(df, column_name, match_string, replace_string):
    df[column_name] = df[column_name].apply(lambda x: replace_string if x == match_string else x)
    return df



