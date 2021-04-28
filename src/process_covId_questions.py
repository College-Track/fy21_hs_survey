import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np
import variables
import helpers
from gspread_pandas import Spread, Client, conf
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
import soql_queries as soql

SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Salesforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)


load_dotenv()


config = conf.get_config("./gspread_pandas/")
hs_spread = Spread("1u7fLc0Dlg1zhWfn8xVgedmYyedr0Z1D1NfZ6uSov5tc", config=config)

hs_spread_spanish = Spread(
    "1jvY7a9yncWMI44uFf8HMypHuKhoHNkOEQ6Fr9Rqza94", config=config
)

student_List = SF_SOQL("fy21_hs_survey_student_list", soql.student_list_query)
student_List.load_from_sf_soql(sf)
student_List.shorten_site_names("A_SITE__c")


english_df = hs_spread.sheet_to_df().reset_index()

english_df = english_df[
    [
        "Student: Contact Id",
        "If/When College Track is able to have students physically return to the site, are you interested in doing so?",
        "I will feel comfortable returning to the site for in-person programming if/when (check all that apply): ",
        "Other",
    ]
]

merged_df = english_df.merge(
    student_List.df, left_on="Student: Contact Id", right_on="C_Id", how="left"
)


merged_df["split"] = merged_df[
    "I will feel comfortable returning to the site for in-person programming if/when (check all that apply): "
].str.split(",")

# convert list of pd.Series then stack it
def rename_dup_columns(df):
    cols = pd.Series(df.columns)
    for dup in df.columns[df.columns.duplicated(keep=False)]:
        cols[df.columns.get_loc(dup)] = [
            dup + "_" + str(d_idx) if d_idx != 0 else dup
            for d_idx in range(df.columns.get_loc(dup).sum())
        ]
    return cols


cols = rename_dup_columns(merged_df)

merged_df.columns = cols


long_df = (
    merged_df.set_index(
        [
            "C_Id",
            "site_short",
            "C_HIGH_SCHOOL_GRADUATING_CLASS__c",
            "If/When College Track is able to have students physically return to the site, are you interested in doing so?",
            "Other_1",
        ]
    )["split"]
    .apply(pd.Series)
    .stack()
    .reset_index()
    #  .drop('level_4', axis=1)
    .rename(columns={0: "split_values"})
)

drop_values = [" distancing", " etc.)"]

long_df = long_df[~long_df.split_values.isin(drop_values)]

long_df.rename(
    columns={
        "If/When College Track is able to have students physically return to the site, are you interested in doing so?": "feel_safe_to_return"
    },
    inplace=True,
)
long_df["count"] = 1
long_df["num_responses"] = merged_df.C_Id.count()

long_df.to_gbq(
    "surveys.covid_response", project_id="data-studio-260217", if_exists="replace"
)

