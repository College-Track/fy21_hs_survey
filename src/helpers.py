import pandas as pd
import variables
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


def create_long_df(
    df, pivot_list, section_name="_section", subsection_name="_subsection"
):
    columns = list(df.columns)
    drop_columns = [
        col for col in columns if (section_name in col) or (subsection_name in col)
    ]

    question_sections, question_subsections = generate_question_list(
        columns, section_name, subsection_name
    )
    df = df.drop(columns=drop_columns)
    long_df = pd.melt(df, id_vars=pivot_list, var_name="question", value_name="answer")

    long_df["section"] = long_df["question"].map(question_sections)
    long_df["sub_section"] = long_df["question"].map(question_subsections)
    long_df["sub_section"] = long_df["sub_section"].fillna(long_df["section"])
    return long_df


def generate_question_list(columns, section_name, subsection_name):
    question_sections = {}
    question_subsections = {}
    for index, value in enumerate(columns):
        if section_name in value:
            section = value
            i = index + 1
            while i < len(columns) and section_name not in columns[i]:
                if subsection_name in columns[i]:
                    subsection = columns[i]
                    y = i + 1
                    while y < len(columns) and subsection_name not in columns[y]:
                        if section_name in columns[y]:
                            break
                        else:
                            question_subsections[columns[y]] = subsection
                            y += 1
                else:
                    question_sections[columns[i]] = section
                i += 1
    return question_sections, question_subsections


def determine_notable_questions_list(df, groupings, perent_threshold, n_threshold):
    notable_divergencies = []

    for question in variables.question_columns:
        for grouping in groupings:

            _group = pd.crosstab(
                df[grouping], df[question], normalize="index", margins=True
            )
            _group_all = _group[_group.index == "All"]
            _group.drop("All", inplace=True)
            _group_count = pd.crosstab(df[grouping], df[question])
            # for i in range(2):
            #     if i == 1:
            #         kind = "promoter"
            #     else:
            #         kind = "detractor"
            amount_above = _group[1].max() - _group_all[1].values[0]
            amount_below = _group_all[1].values[0] - _group[1].min()

            max_index = _group[_group[1] == _group[1].max()].index.values[0]
            max_count = _group_count[_group_count.index == max_index][1].values[0]

            min_index = _group[_group[1] == _group[1].min()].index.values[0]
            min_count = _group_count[_group_count.index == min_index][1].values[0]

            if (amount_above >= perent_threshold) & (max_count >= n_threshold):

                notable_divergencies.append(
                    {
                        "grouping": grouping,
                        "question": question,
                        # "kind": kind,
                        "type": "above_average",
                        "delta": amount_above,
                        "value": _group[1].max(),
                        "count": max_count,
                        "index": max_index,
                    }
                )
            elif (amount_below >= perent_threshold) & (min_count >= n_threshold):

                notable_divergencies.append(
                    {
                        "grouping": grouping,
                        "question": question,
                        # "kind": kind,
                        "type": "below_average",
                        "delta": amount_below,
                        "value": _group[1].min(),
                        "count": min_count,
                        "index": min_index,
                    }
                )

    notable_divergencies_df = pd.DataFrame(notable_divergencies)
    return notable_divergencies_df


def plot_line_graph(df, title):
    fig, ax = plt.subplots()
    df.sort_values(by="FY21", inplace=True, ascending=False)
    labels = ["\n".join(wrap(l, 55)) for l in df.index]

    fig.suptitle(title, fontsize=12)

    _df = pd.melt(df.iloc[:, :-1], ignore_index=False).reset_index()
    sns.lineplot(data=_df, x="variable", y="value", hue="index", ax=ax)

    ax.legend(
        labels, loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=1, fontsize=10
    )

    ax.set_ylabel("% Students Answering Positive")

    ax.set_xlabel(None)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    return fig


def plot_bar_graph(df, title):
    fig, ax = plt.subplots()
    df.sort_values(by="FY21", inplace=True, ascending=False)
    labels = ["\n".join(wrap(l, 25)) for l in df.index]

    fig.suptitle(title, fontsize=12)

    _df = pd.melt(df.iloc[:, :-1], ignore_index=False).reset_index()
    sns.barplot(
        data=_df, y="index", x="value", hue="variable", ax=ax, saturation=1, orient="h"
    )

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=8)

    ax.set_xlabel("% Students Answering Positive")

    ax.set_yticklabels(labels, fontsize=10)

    ax.set_ylabel("Question")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
    return fig


def determine_notable_questions(
    df, groupings, question_columns, perent_threshold, n_threshold
):
    notable_divergencies = []

    for question in question_columns:
        for grouping in groupings:
            # print(question, grouping)
            try:
                percent = pd.crosstab(
                    grouping, df[question], normalize="index", margins=True
                )[1]

                percent.name = "percent_positive"
                # percent.reset_index(inplace=True)
            except:
                continue

            count = pd.crosstab(grouping, df[question], margins=True)

            count.rename(
                columns={0: "count_not_positive", 1: "count_positive"}, inplace=True
            )
            count.drop(columns="All", inplace=True)

            _group = pd.concat([percent, count], axis=1)

            summary = _group.tail(1)
            # summary.drop(columns="All", inplace=True)
            _group.drop("All", inplace=True)
            _group = _group.reset_index()
            try:
                above_threshold = summary.percent_positive.values[0] + perent_threshold
                below_threshold = summary.percent_positive.values[0] - perent_threshold
            except:
                continue

            _group_subset_above = _group[
                (_group.percent_positive >= above_threshold)
                & (_group.count_positive >= n_threshold)
            ]

            _group_subset_below = _group[
                (_group.percent_positive <= below_threshold)
                & (_group.count_not_positive >= n_threshold)
            ]

            # _group_subset_above.reset_index(inplace=True)

            grouping_names = []
            for grouping_name in grouping:
                grouping_names.append(grouping_name.name)
            if len(_group_subset_above) > 0:

                notable_divergencies.extend(
                    _group_subset_above.apply(
                        lambda x: create_notable_dict(
                            x, "positive", grouping_names, question, summary
                        ),
                        axis=1,
                    )
                )
            # _group_subset_below.reset_index(inplace=True)
            if len(_group_subset_below) > 0:
                notable_divergencies.extend(
                    _group_subset_below.apply(
                        lambda x: create_notable_dict(
                            x, "not_positive", grouping_names, question, summary
                        ),
                        axis=1,
                    )
                )

    return pd.DataFrame(notable_divergencies)


def create_notable_dict(
    row, positive_or_not_positive, grouping_names, question, summary
):
    if positive_or_not_positive == "positive":
        type_name = "above_average"
        count = "count_positive"
    else:
        type_name = "below_average"
        count = "count_not_positive"

    grouping_columns = [x for x in row.keys()[:-3]]
    notable_groupings = [row[x] for x in grouping_columns]
    if len(notable_groupings) > 1:
        combined_single = "combined_groupings"
    else:
        combined_single = "single_grouping"
    return {
        "grouping": ", ".join(grouping_names),
        "question": question,
        "type": type_name,
        "value": row.percent_positive,
        "group_mean": summary.percent_positive.values[0],
        "count": row[count],
        "index_name": ", ".join(notable_groupings),
        "combined_or_single": combined_single,
    }

