import pandas as pd
import variables
import helpers
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import matplotlib.ticker as mtick
import numpy as np

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib import collections as matcoll

from textwrap import wrap


plt.style.use("college_track")
mpl.rcParams.update({"font.size": 8})


mpl.rcParams.update({"figure.figsize": [4.35, 4.15]})
mpl.rcParams.update({"figure.dpi": 115})

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]


#  Load Data Needed
filename = "../data/raw/fy21_hs_survey_analysis.pkl"
df = pd.read_pickle(filename)

column_df = pd.read_pickle("../data/raw/fy21_hs_survey_columns.pkl")

column_df.loc[:, "original_columns"] = column_df["original_columns"].str.strip()

column_dict = (
    column_df[["clean_columns", "original_columns"]]
    .set_index("clean_columns")
    .to_dict()["original_columns"]
)
historical_since_fy18 = pd.read_pickle("../data/interim/positive_growth_since_fy18.pkl")

historical_since_fy18 = historical_since_fy18.rename(index=column_dict)

historical_since_fy20 = pd.read_pickle("../data/interim/positive_growth_since_fy20.pkl")

historical_since_fy20 = historical_since_fy20.rename(index=column_dict)


largest_since_fy18 = historical_since_fy18.nlargest(4, "change_from_first")
smallest_since_fy18 = historical_since_fy18.nsmallest(4, "change_from_first")

largest_since_fy20 = historical_since_fy20.nlargest(4, "change_from_first")
smallest_since_fy20 = historical_since_fy20.nsmallest(4, "change_from_first")


largest_since_fy18.to_pickle("../data/interim/largest_since_fy18.pkl")
smallest_since_fy18.to_pickle("../data/interim/smallest_since_fy18.pkl")
largest_since_fy20.to_pickle("../data/interim/largest_since_fy20.pkl")
smallest_since_fy20.to_pickle("../data/interim/smallest_since_fy20.pkl")


largest_since_fy18_plot = helpers.plot_line_graph(
    largest_since_fy18, "Questions With Largest Increase Since FY18"
)

largest_since_fy18_plot.savefig("../images/largest_since_fy18_plot.png")

smallest_since_fy18_plot = helpers.plot_line_graph(
    smallest_since_fy18, "Questions With Largest Decrease Since FY18"
)

smallest_since_fy18_plot.savefig("../images/smallest_since_fy18_plot.png")


largest_since_fy20_plot = helpers.plot_bar_graph(
    largest_since_fy20, "Questions With Largest Increase Since FY20"
)
largest_since_fy20_plot.savefig("../images/largest_since_fy20_plot.png")

smallest_since_fy20_plot = helpers.plot_bar_graph(
    smallest_since_fy20, "Questions With Largest Decrease Since FY20"
)

smallest_since_fy20_plot.savefig("../images/smallest_since_fy20_plot.png")

notable_divergencies_df = pd.read_pickle(
    "../data/interim/notable_divergencies_df_with_multiple_groupings.pkl"
)

nd_df = notable_divergencies_df.merge(
    column_df, left_on="question", right_on="clean_columns", how="left"
)

nd_df.loc[:, "original_columns"] = nd_df.original_columns.str.strip()

nd_df["abs_diff"] = abs(nd_df.group_mean - nd_df.value)

nd_df_subset = nd_df[nd_df["count"] >= 30]

nd_df_subset.sort_values(["abs_diff"], ascending=False, inplace=True)


nd_df_subset = nd_df_subset[nd_df_subset.grouping != "NPS_Score"]
nd_df_subset = nd_df_subset[nd_df_subset.question != "in_the_area_outside_your_center"]

nd_df_subset = nd_df_subset[~nd_df_subset["grouping"].str.contains("site_short")]

most_divergent = nd_df_subset.groupby(["section", "type"]).head(1)

most_divergent.sort_values(["value"], ascending=False, inplace=True)


# nd_df_above = nd_df[nd_df.type == "above_average"]


# top_nd_df_above = nd_df_above.groupby(["section"]).head(3)

nd_df_long = pd.melt(
    most_divergent,
    id_vars=["question", "index_name", "section", "type", "original_columns"],
    value_vars=["value", "group_mean"],
)

nd_df_long.loc[nd_df_long.variable == "value", "variable"] = nd_df_long.loc[
    nd_df_long.variable == "value", "index_name"
]

nd_df_long.loc[nd_df_long.variable == "group_mean", "variable"] = "Question Avg."


survey_sections = {
    "ct_site_section": "Notable CT Site and Safety Questions",
    "academic_affairs_section": "Notable Academic Affairs Questions",
    "student_life_section": "Notable Student Life Questions",
    "college_prep_section": "Notable College Prep Questions",
    "coaching_programming_section": "Notable Coaching Questions",
    "wellness_programming_section": "Notable Wellness Questions",
    "virtual_programming_section": "Notable Virtual Programming Questions",
}


def plot_notable_questions_graph(df, title, colors):
    fig, ax = plt.subplots(figsize=(6.5, 3.75))
    labels = ["\n".join(wrap(l, 25)) for l in df.original_columns]
    labels = list(np.unique(labels))
    colors = ["#78BE20", "#DA291C", "#666"]
    if len(df.variable) == 2:
        colors = ["#78BE20", "#666"]
    fig.suptitle(title, fontsize=12)

    sns.barplot(
        data=df,
        x="value",
        y="original_columns",
        hue="variable",
        ax=ax,
        saturation=1,
        orient="h",
        palette=colors,
    )

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=8)

    ax.set_xlabel("% Students Answering Positive")

    ax.set_yticklabels(labels, fontsize=10)

    ax.set_ylabel("Question")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))

    for p in ax.patches:
        width = p.get_width()  # get bar length
        ax.text(
            width + 0.01,  # set the text at 1 unit right of the bar
            p.get_y() + p.get_height() / 2,  # get Y coordinate + X coordinate / 2
            "{:.0%}".format(width),  # set variable to display, 2 decimals
            ha="left",  # horizontal alignment
            va="center",
        )  # vertical alignment
    return fig


for survey_section, title in survey_sections.items():
    _df = nd_df_long[nd_df_long.section == survey_section]
    # _df.sort_values('value',inplace=True)
    _plot = plot_notable_questions_graph(_df, title, colors)
    plot_filename = "../images/" + survey_section + "_plot.png"
    _plot.savefig(plot_filename)


custom_palette = {}
for q in set(nd_df_long.original_columns):
    score_type = nd_df_long[nd_df_long.original_columns == q]["type"]
    if score_type == "above_average":
        custom_palette[q] = "#78BE20"
    elif score_type == "below_average":
        custom_palette[q] = "#DA291C"
    else:
        custom_palette[q] = "#666666"

#####

test = nd_df_subset[nd_df_subset.section == "virtual_programming_section"]

test[test.type == "above_average"].index_name.value_counts()

test[test.type == "below_average"].index_name.value_counts()


test.index_name.value_counts()


df[
    [
        "site_short",
        "because_of_coaching_i_have_been_able_to_form_supportive_relationships_with_ct_st",
        "because_of_coaching_i_have_been_able_to_form_supportive_relationships_with_peers",
        "because_of_coaching_i_am_more_self_motivated_and_have_a_sense_of_ownership_to_ac",
    ]
].groupby("site_short").mean()

test_df = df[
    [
        # 'site_short',
        "because_of_coaching_i_have_been_able_to_form_supportive_relationships_with_ct_st",
        "because_of_coaching_i_have_been_able_to_form_supportive_relationships_with_peers",
        "because_of_coaching_i_am_more_self_motivated_and_have_a_sense_of_ownership_to_ac",
    ]
]

test_df.melt().mean()
