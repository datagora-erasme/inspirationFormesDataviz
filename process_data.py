import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import dotenv_values
import gspread

credentials = json.loads(dotenv_values()["SERVICE_ACCOUNT"])
service_account = gspread.service_account_from_dict(credentials)
sheets = service_account.open("Ils sont venus à l'urbanlab")
worksheet_2018 = sheets.worksheet("2018")
worksheet_2017 = sheets.worksheet("2017")
wks_dict_2018 = worksheet_2018.get_all_values()
wks_dict_2017 = worksheet_2017.get_all_values()

df = pd.DataFrame(
    wks_dict_2018[2:],
    columns = wks_dict_2018[1]
)
df_17 = pd.DataFrame(
    wks_dict_2017[2:],
    columns = wks_dict_2017[1]
)

col_interest = [
    "Date",
    "Nombre",
    
]
df = df[col_interest]
df_17 = df_17[col_interest]
df["Date"] = pd.to_datetime(df["Date"])
df_17["Date"] = pd.to_datetime(df_17["Date"])
df.dropna(inplace=True)
df.reset_index(inplace=True, drop=True)
df_17.dropna(inplace=True)
df_17.reset_index(inplace=True, drop=True)

new_df = pd.DataFrame()
for index, line in df.iterrows():
    for i in range(int(line["Nombre"])):
        new_df = pd.concat([new_df, pd.DataFrame({
            "Nombre": [1],
            "Date": [line["Date"]],
            "year": 2018
        })])
new_df_17 = pd.DataFrame()
for index, line in df_17.iterrows():
    for i in range(int(line["Nombre"])):
        new_df_17 = pd.concat([new_df_17, pd.DataFrame({
            "Nombre": [1],
            "Date": [line["Date"]],
            "year": 2017
        })])

new_df = new_df.append(new_df_17)
new_df["MM-DD"] = new_df.apply(
    axis=1,
    func=lambda x: x["Date"].replace(year=2000)
)

new_df.reset_index(
    drop=True,
    inplace=True
)
print(new_df.info())

new_df.to_csv("processed_data.csv", index=False)