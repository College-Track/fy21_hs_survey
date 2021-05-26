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


project_id = "data-studio-260217"
filename = "../data/raw/fy21_hs_survey_individual_responses.pkl"


replace_data = False

if replace_data == False:
    # Read from CSV if already written to avoid repeatedly transferring data from BigQuery
    df = pd.read_pickle(filename)

else:
    query = (
        "SELECT * FROM `data-studio-260217.surveys.fy21_hs_survey_individual_responses`"
    )
    df = pd.read_gbq(query, project_id=project_id)
    df.to_pickle(filename)

    columns_query = "SELECT * FROM `data-studio-260217.surveys.fy21_hs_survey_columns`"
    column_df = pd.read_gbq(columns_query, project_id=project_id)
    column_df.to_pickle("../data/raw/fy21_hs_survey_columns.pkl")

column_dict = (
    column_df[["clean_columns", "original_columns"]]
    .set_index("clean_columns")
    .to_dict()["original_columns"]
)

old_columns = list(df.columns)


new_columns = [column_dict.get(item, item) for item in old_columns]

df.columns = new_columns

df.rename(
    columns={
        "site_short": "Site",
        "full_name_c": "Full Name",
        "high_school_graduating_class_c": "High School Class",
        "Most_Recent_GPA_Cumulative_bucket": "Most Recent C. GPA Bucket",
        "Ethnic_background_c": "Ethnic Background (In Salesforce)",
        "Gender_c": "Gender",
    },
    inplace=True,
)


def write_to_excel(df, title):
    filename = "../data/processed/individual_responses/" + title + ".xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Responses")
    workbook = writer.book
    worksheet = writer.sheets["Responses"]

    fmt_header = workbook.add_format(
        {
            "bold": True,
            #  'width': 256,
            "text_wrap": True,
            # "valign": "top",
            "align": "left",
            "fg_color": "#505050",
            "font_color": "#FFFFFF",
            "border": 0,
        }
    )
    for col, value in enumerate(df.columns.values):
        worksheet.write(0, col, value, fmt_header)
    worksheet.set_column(0, len(df.columns), 60)

    writer.save()


for site in df.Site.unique():
    _df = df[df.Site == site]
    title = site + "_individual_responses"
    write_to_excel(_df, title)

