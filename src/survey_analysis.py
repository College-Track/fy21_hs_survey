import pandas as pd
import variables
import helpers


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


# NPS Score Data
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

nps_table.nlargest(4, "nps_score")

nps_table.nlargest(4, "nps_detractor")


# Most Positive and Negative Answers

all_answers_grouped_by_site = df.groupby("site_short")[
    variables.question_columns
].mean()

all_answers_grouped = df[variables.question_columns].mean()

most_positive_answers = pd.DataFrame(all_answers_grouped.nlargest(5))
most_positive_answers.rename(
    columns={0: "% Student Answering Positively"}, inplace=True
)
most_positive_answers = most_positive_answers.rename(index=column_dict)
most_positive_answers.to_pickle("../data/interim/most_positive_answers.pkl")


most_negative_answers = pd.DataFrame(all_answers_grouped.nsmallest(5))
most_negative_answers.rename(
    columns={0: "% Student Answering Positively"}, inplace=True
)
most_negative_answers = most_negative_answers.rename(index=column_dict)
most_negative_answers.to_pickle("../data/interim/most_negative_answers.pkl")


count_of_positive_answers = (all_answers_grouped > 0.70).sum()

percent_positive = count_of_positive_answers / len(all_answers_grouped_by_site.columns)

count_of_positive_answers_by_site = pd.DataFrame(
    (all_answers_grouped_by_site > 0.75).sum(axis=1)
)
# ( all_answers_grouped_by_site <= 0.5 ).sum(axis=1)
count_of_positive_answers_by_site.rename(columns={0: "count_positive"}, inplace=True)
count_of_positive_answers_by_site[
    "percent_positive"
] = count_of_positive_answers_by_site["count_positive"] / len(
    all_answers_grouped_by_site.columns
)

most_positive_sites = count_of_positive_answers_by_site.nlargest(4, "percent_positive")

# sites_above_50 = count_of_positive_answers_by_site[count_of_positive_answers_by_site.percent_positive >= 0.5]

most_positive_sites.to_pickle("../data/interim/most_positive_sites.pkl")


# Find outliers by various groupings
from scipy import stats

groupings = [
    "site_short",
    "high_school_graduating_class_c",
    "Gender_c",
    "Ethnic_background_c",
    "NPS_Score",
    "Most_Recent_GPA_Cumulative_bucket",
]


notable_divergencies_df = helpers.determine_notable_questions_list(
    df, groupings, 0.15, 25
)

notable_divergencies_df.to_pickle("../data/interim/notable_divergencies_df.pkl")

notable_divergencies_df = pd.read_pickle("../data/interim/notable_divergencies_df.pkl")

promoters = notable_divergencies_df[
    (notable_divergencies_df.kind == "promoter")
    & (notable_divergencies_df.type == "above_average")
]

detractors = notable_divergencies_df[
    (notable_divergencies_df.kind == "detractor")
    & (notable_divergencies_df.type == "above_average")
]

positive_detractors = notable_divergencies_df[
    (notable_divergencies_df.kind == "detractor")
    & (notable_divergencies_df.type == "below_average")
]


df.ct_provides_a_supportive_learning_environment_for_me
test_grouping = pd.crosstab(
    df["site_short"],
    df.ct_provides_a_supportive_learning_environment_for_me,
    normalize="index",
    margins=True,
)
test_grouping[1]
