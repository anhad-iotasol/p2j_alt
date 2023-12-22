import json
import pandas as pd
from paths import TABLE_BASE_PATH
from pathlib import Path

# Builds a DataFrame acc. to the form schema and saves it as csv
def build_df(columns:list[str],table_name:str):
    data = dict([(column,[]) for column in columns])
    df = pd.DataFrame(data)
    df.to_csv(f"{TABLE_BASE_PATH}{table_name}.csv",index=False)


# Adds an entry to the existing csv file.
def add_data(data:dict,table_name:str):
    print(f"data={data}")
    df_row = dict([(column,[data[column]]) for column in data])
    print(f"df_row = {df_row}")
    df = pd.DataFrame(df_row)
    df.to_csv(f"{TABLE_BASE_PATH}{table_name}.csv",mode='a',index=False,header=False)
