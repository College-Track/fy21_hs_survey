import pandas as pd
import variables
import helpers
import warnings

warnings.filterwarnings("ignore")


#  Load Data Needed
filename = "../data/raw/fy21_hs_survey_analysis.pkl"
df = pd.read_pickle(filename)

column_df = pd.read_pickle("../data/raw/fy21_hs_survey_columns.pkl")

column_dict = (
    column_df[["clean_columns", "original_columns"]]
    .set_index("clean_columns")
    .to_dict()["original_columns"]
)

historical_since_fy18 = pd.read_pickle("../data/interim/positive_growth_since_fy18.pkl")

historical_since_fy20 = pd.read_pickle("../data/interim/positive_growth_since_fy20.pkl")


# # NPS Score Data
nps_score = (
    df.nps_positive.value_counts(normalize=True).loc[1]
    - df.nps_detractor.value_counts(normalize=True).loc[1]
)

nps_table = df.groupby("site_short")[["nps_positive", "nps_detractor"]].mean()

nps_table["nps_score"] = nps_table["nps_positive"] - nps_table["nps_detractor"]

nps_summary = df[["nps_positive", "nps_detractor"]].mean()

nps_summary["nps_score"] = nps_summary["nps_positive"] - nps_summary["nps_detractor"]

nps_summary.name = "Total"

# nps_table = nps_table.append(nps_summary)

nps_table.nlargest(4, "nps_positive")

nps_table.nlargest(7, "nps_score")

nps_table.nlargest(4, "nps_detractor")


# # Most Positive and Negative Answers


all_answers_grouped = df[variables.question_columns].mean()

all_answers_grouped = all_answers_grouped[
    all_answers_grouped.index != "in_the_area_outside_your_center"
]

most_positive_answers = pd.DataFrame(all_answers_grouped.nlargest(5))
most_positive_answers.rename(
    columns={0: "% of Student Answering Positively"}, inplace=True
)
most_positive_answers = most_positive_answers.rename(index=column_dict)
most_positive_answers.to_pickle("../data/interim/most_positive_answers.pkl")


most_negative_answers = pd.DataFrame(all_answers_grouped.nsmallest(5))
most_negative_answers.rename(
    columns={0: "% of Student Answering Positively"}, inplace=True
)
most_negative_answers = most_negative_answers.rename(index=column_dict)
most_negative_answers.to_pickle("../data/interim/most_negative_answers.pkl")


count_of_positive_answers = (all_answers_grouped > 0.70).sum()

percent_positive = count_of_positive_answers / len(all_answers_grouped_by_site.columns)


def positive_by_group(df, grouping):
    _grouped = df.groupby(grouping)[variables.question_columns].mean()

    count_of_positive_answers = pd.DataFrame((_grouped > 0.70).sum(axis=1))
    # ( all_answers_grouped_by_site <= 0.5 ).sum(axis=1)
    count_of_positive_answers.rename(columns={0: "count_positive"}, inplace=True)
    count_of_positive_answers["percent_positive"] = count_of_positive_answers[
        "count_positive"
    ] / len(_grouped.columns)
    return count_of_positive_answers.sort_values("percent_positive")


count_of_positive_answers_by_site = positive_by_group(df, "site_short")

most_positive_sites = count_of_positive_answers_by_site.nlargest(4, "percent_positive")

most_positive_sites.to_pickle("../data/interim/most_positive_sites.pkl")

count_positive_by_class = positive_by_group(df, "high_school_graduating_class_c")

count_positive_by_nps = positive_by_group(df, "NPS_Score")

count_positive_by_gender = positive_by_group(df, "Gender_c")

count_positive_by_ethnicity = positive_by_group(df, ["Ethnic_background_c"])

count_positive_by_gpa = positive_by_group(df, ["Most_Recent_GPA_Cumulative_bucket"])


count_positive_by_gender_ethnicity = positive_by_group(
    df, ["Gender_c", "Ethnic_background_c"]
)
count_positive_by_gender_ethnicity

# # Find outliers by various groupings


groupings = [
    [df["site_short"]],
    [df["high_school_graduating_class_c"]],
    [df["Gender_c"]],
    [df["Ethnic_background_c"]],
    [df["NPS_Score"]],
    [df["Most_Recent_GPA_Cumulative_bucket"]],
    [df["site_short"], df["Gender_c"]],
    [df["Gender_c"], df["Ethnic_background_c"]],
    [df["site_short"], df["Ethnic_background_c"]],
    [df["site_short"], df["Most_Recent_GPA_Cumulative_bucket"]],
    [df["site_short"], df["Gender_c"], df["Ethnic_background_c"]],
]


notable_divergencies_df = helpers.determine_notable_questions(
    df, groupings, variables.question_columns, 0.10, 25
)

notable_divergencies_df.to_pickle(
    "../data/interim/notable_divergencies_df_with_multiple_groupings.pkl"
)

notable_divergencies_df = pd.read_pickle(
    "../data/interim/notable_divergencies_df_with_multiple_groupings.pkl"
)

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


with pd.ExcelWriter("../data/processed/hs_notable_groupings.xlsx") as writer:
    promoters.to_excel(writer, sheet_name="above_average", index=False)
    detractors.to_excel(writer, sheet_name="below_average", index=False)
    count_of_above_average.to_excel(
        writer, sheet_name="count_above_average", index=False
    )
    count_of_below_average.to_excel(
        writer, sheet_name="count_below_average", index=False
    )

