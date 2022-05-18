import pandas as pd
import model.sql_loader as sl

def get_dropdown_values():
    dropdown_options = pd.read_sql(f'SELECT Valley FROM valley;', sl.get_connexion())[
        'Valley'].values.tolist()
    return dropdown_options


def get_unique_values_map(value):
    df_map = pd.read_sql(
        f'SELECT Station, station.Latitude, station.Longitude FROM station JOIN valley ON valley.Id_=Valley_id AND Valley = "{value}";',
        sl.get_connexion())
    print(df_map)
    return df_map


def get_groupby_values_df(value, groupby, select_variables):
    sub_df = pd.read_sql(
        f'SELECT * FROM harvest JOIN tree ON tree.Id_=Tree_id JOIN station ON station.Id_=Station_id AND Station="{value}";',
        sl.get_connexion())
    sub_df = sub_df.groupby(groupby)[select_variables].mean()
    if groupby == 'DD':
        sub_df.index.set_names(["Harvest day in julian"], inplace=True)
        # rename the 'DD' column by 'Harvest day in julian'
    return sub_df
