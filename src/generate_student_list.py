import pandas as pd
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
from ct_snippets.sf_bulk import sf_bulk, sf_bulk_handler, generate_data_dict
import numpy as np
import soql_queries as soql
import variables
import helpers

load_dotenv()


SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Salesforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)


# Sample for loading from SOQL
# query = """ """
student_List = SF_SOQL("fy21_hs_survey_student_list", soql.student_list_query)
student_List.load_from_sf_soql(sf)
student_List.shorten_site_names("A_SITE__c")

student_List.df["student_search"] = (
    student_List.df["C_Full_Name__c"] + " - " + student_List.df["site_short"]
)

student_List.df = student_List.df[
    [
        "student_search",
        "C_Id",
        # "site_short",
        # "C_Full_Name__c",
        "C_College_Track_Status__c",
        "C_HIGH_SCHOOL_GRADUATING_CLASS__c",
    ]
]

# Sample for saving data
student_List.write_file(subfolder="processed", file_type=".csv", file_level="child")

