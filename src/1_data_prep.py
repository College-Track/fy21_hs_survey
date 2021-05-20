import pandas as pd
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
from ct_snippets.sf_bulk import sf_bulk, sf_bulk_handler, generate_data_dict
from reportforce import Reportforce
import numpy as np
import soql_queries as soql
import variables
import helpers
from itertools import compress

load_dotenv()


SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Salesforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)


project_id = "data-studio-260217"
filename = "../data/raw/fy21_hs_survey_analysis.pkl"


replace_data = False

if replace_data == True:
    # Read from CSV if already written to avoid repeatedly transferring data from BigQuery
    df = pd.read_pickle(filename)

else:
    query = "SELECT * FROM `data-studio-260217.surveys.fy21_hs_survey_analysis`"
    df = pd.read_gbq(query, project_id=project_id)
    df.to_pickle(filename)

    columns_query = "SELECT * FROM `data-studio-260217.surveys.fy21_hs_survey_columns`"
    column_df = pd.read_gbq(columns_query, project_id=project_id)
    column_df.to_pickle("../data/raw/fy21_hs_survey_columns.pkl")

#  Old data
replace_old_data = False
if replace_old_data == False:
    fy18_df = pd.read_pickle("../data/raw/fy18_hs_survey_analysis.pkl")
    fy19_df = pd.read_pickle("../data/raw/fy19_hs_survey_analysis.pkl")
    fy20_df = pd.read_pickle("../data/raw/fy20_hs_survey_analysis.pkl")


else:
    project_id_old = "data-warehouse-289815"
    fy18_query = "SELECT * FROM `data-warehouse-289815.surveys.fy18_hs_survey`"
    fy18_df = pd.read_gbq(fy18_query, project_id=project_id_old)
    fy18_df.to_pickle("../data/raw/fy18_hs_survey_analysis.pkl")

    fy19_query = "SELECT * FROM `data-warehouse-289815.surveys.fy19_hs_survey`"
    fy19_df = pd.read_gbq(fy19_query, project_id=project_id_old)
    fy19_df.to_pickle("../data/raw/fy19_hs_survey_analysis.pkl")
    fy19_df = pd.read_pickle("../data/raw/fy19_hs_survey_analysis.pkl")

    fy20_query = "SELECT * FROM `data-warehouse-289815.surveys.fy20_hs_survey`"
    fy20_df = pd.read_gbq(fy20_query, project_id=project_id_old)
    fy20_df.to_pickle("../data/raw/fy20_hs_survey_analysis.pkl")

fy21_ps_query = "SELECT * FROM `data-studio-260217.surveys.fy21_ps_survey_analysis`"
fy21_ps_df = pd.read_gbq(fy21_ps_query, project_id=project_id)
fy21_ps_df.to_pickle("../data/raw/fy21_ps_survey_analysis.pkl")


fy18_df.rename(
    columns={
        "check_ins_with_ct_staff_academic_coaches_etc": "check_ins_with_ct_staff_academic_coaches_success_coaches_etc"
    },
    inplace=True,
)
fy19_df.rename(
    columns={
        "check_ins_with_ct_staff_academic_coaches_etc": "check_ins_with_ct_staff_academic_coaches_success_coaches_etc"
    },
    inplace=True,
)

valid_fy21 = list(df.columns[7:])
valid_fy21.remove("inside_your_college_track_center")

valid_fy21.remove("in_the_area_outside_your_center")


fy20_bool = [x in list(valid_fy21) for x in list(fy20_df.columns)]

valid_fy20 = list(compress(fy20_df.columns, fy20_bool))


fy19_bool = [x in list(valid_fy20) for x in list(fy19_df.columns)]

valid_fy19 = list(compress(fy19_df.columns, fy19_bool))

fy18_bool = [x in list(valid_fy19) for x in list(fy18_df.columns)]

valid_fy18 = list(compress(fy18_df.columns, fy18_bool))

fy18_subset = fy18_df[valid_fy18]
fy19_subset = fy19_df[valid_fy18]
fy20_subset = fy20_df[valid_fy18]
df_subset = df[valid_fy18]

fy20_subset_one_year = fy20_df[valid_fy20]


def determine_positive_answer(answer):
    positive_answers = [
        "Strongly Agree",
        "Agree",
        "Very Safe",
        "Extremely helpful",
        "Very helpful",
        "Extremely Excited",
        "Quite Excited",
        "Almost Always",
        "Extremely Helpful",
        "Very Helpful",
        "10 - extremely likely",
        "9",
        "Almost always",
        "Frequently",
        "Extremely confident",
        "Quite confident",
        "Extremely likely",
        "Likely",
        "SomewhatÊagree",
        "Somewhat agree",
    ]

    positive_answers = [x.lower() for x in positive_answers]
    if pd.isna(answer):
        return np.nan

    elif answer.lower() in positive_answers:
        return 1
    else:
        return 0


for column in valid_fy18:

    fy18_subset.loc[:, column] = fy18_subset[column].apply(
        lambda x: determine_positive_answer(x)
    )
    fy19_subset.loc[:, column] = fy19_subset[column].apply(
        lambda x: determine_positive_answer(x)
    )
    fy20_subset.loc[:, column] = fy20_subset[column].apply(
        lambda x: determine_positive_answer(x)
    )

for column in valid_fy20:

    fy20_subset_one_year.loc[:, column] = fy20_subset_one_year[column].apply(
        lambda x: determine_positive_answer(x)
    )


df_one_year = df[valid_fy20]

fy18_positive = fy18_subset.mean()
fy19_positive = fy19_subset.mean()
fy20_positive = fy20_subset.mean()
df_positive = df_subset.mean()

fy20_subset_one_year_positive = fy20_subset_one_year.mean()
df_one_year_positive = df_one_year.mean()

fy18_positive.name = "FY18"
fy19_positive.name = "FY19"
fy20_positive.name = "FY20"
df_positive.name = "FY21"

fy20_subset_one_year_positive.name = "FY20"
df_one_year_positive.name = "FY21"


positive_growth = pd.concat(
    [fy18_positive, fy19_positive, fy20_positive, df_positive], axis=1
)

positive_growth_one_year = pd.concat(
    [fy20_subset_one_year_positive, df_one_year_positive], axis=1
)


positive_growth["change_from_first"] = positive_growth.FY21 - positive_growth.FY18

positive_growth_one_year["change_from_first"] = (
    positive_growth_one_year.FY21 - positive_growth_one_year.FY20
)


positive_growth.to_pickle("../data/interim/positive_growth_since_fy18.pkl")

positive_growth_one_year.to_pickle("../data/interim/positive_growth_since_fy20.pkl")
