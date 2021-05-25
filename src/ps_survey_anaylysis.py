import pandas as pd

# from pandas.core.frame import DataFrame
import variables
import helpers


#  Load Data Needed
filename = "../data/raw/fy21_ps_survey_analysis.pkl"
df = pd.read_pickle(filename)


groupings = [
    [df["site_short"]],
    [df["high_school_graduating_class_c"]],
    [df["Ethnic_background_c"]],
    [df["Gender_c"]],
    [df["college_elig_gpa_bucket"]],
    [df["Most_Recent_GPA_Cumulative_bucket"]],
    [df["school_type"]],
    [df["credit_accumulation_pace_c"]],
    [df["comms_bucket"]],
    [df["nps_bucket"]],
    [df["covid_bucket"]],
    [df["cca_count_to_date"]],
    [df["site_short"], df["Gender_c"]],
    [df["Gender_c"], df["Ethnic_background_c"]],
    [df["site_short"], df["Ethnic_background_c"]],
    [df["site_short"], df["Most_Recent_GPA_Cumulative_bucket"]],
    [df["site_short"], df["Gender_c"], df["Ethnic_background_c"]],
]


# notable_divergencies_df = helpers.determine_notable_questions_list(
#     df, groupings, 0.15, 30
# )
# notable_divergencies_df = pd.read_pickle("../data/interim/notable_divergencies_df.pkl")

# percent = pd.crosstab(
#     df["site_short"],
#     df["in_the_past_12th_months_were_you_involved_in_a_club_organiza"],
#     normalize="index",
#     margins=True,
# )

notable_divergencies_df = helpers.determine_notable_questions(
    df, groupings, variables.ps_question_columns, 0.05, 15
)

notable_divergencies_df.to_csv("../data/interim/ps_notable_divergencies_df.csv")


promoters = notable_divergencies_df[notable_divergencies_df.type == "above_average"]

detractors = notable_divergencies_df[notable_divergencies_df.type == "below_average"]


count_of_above_average = pd.DataFrame(promoters.index_name.value_counts()).reset_index()

count_of_above_average.rename(
    columns={"index": "grouping", "index_name": "count_of_above_average"}, inplace=True
)


count_of_below_average = pd.DataFrame(
    detractors.index_name.value_counts()
).reset_index()

count_of_below_average.rename(
    columns={"index": "grouping", "index_name": "count_of_below_average"}, inplace=True
)


with pd.ExcelWriter("../data/processed/ps_notable_groupings.xlsx") as writer:
    promoters.to_excel(writer, sheet_name="above_average", index=False)
    detractors.to_excel(writer, sheet_name="below_average", index=False)
    count_of_above_average.to_excel(
        writer, sheet_name="count_above_average", index=False
    )
    count_of_below_average.to_excel(
        writer, sheet_name="count_below_average", index=False
    )


# test = df.groupby('site_short').count()

# pd.crosstab(df.site_short, df.besides_my_ct_college_advisor_i_have_at_least_one_ct_staff_m)
