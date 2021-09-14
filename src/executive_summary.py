import pandas as pd
import datapane as dp
import variables
import helpers
import matplotlib.pyplot as plt
import matplotlib as mpl


class SafeDict(dict):
    def __missing__(self, key):
        return "{{" + key + "}}"


# dp.File(file='../images/largest_since_fy18_plot.png')

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

filename = "data/raw/fy21_hs_survey_analysis.pkl"
df = pd.read_pickle(filename)


executive_summary_pt1 = open("text/executive_summary_pt1.md", "r").read()

executive_summary_pt1 = executive_summary_pt1.format_map(
    SafeDict(previous_range="80% - 90%", nps_score="52%")
)


most_positive_answers = pd.read_pickle("data/interim/most_positive_answers.pkl")
most_positive_answers = most_positive_answers.style.format("{:.0%}")

most_negative_answers = pd.read_pickle("data/interim/most_negative_answers.pkl")
most_negative_answers = most_negative_answers.style.format("{:.0%}")

most_positive_sites = pd.read_pickle("data/interim/most_positive_sites.pkl")
most_positive_sites = list(most_positive_sites.index)
most_positive_sites_string = ", ".join(
    most_positive_sites[:-2] + [", and ".join(most_positive_sites[-2:])]
)

response_rate = "80%"

nps_score = "52%"

report = dp.Report(
    dp.Text(executive_summary_pt1).format(
        # nps_score=nps_score,
        # responce_rate=response_rate,
        most_positive=most_positive_answers,
        most_negative=most_negative_answers,
    ),
    dp.Text("#### Trend Charts"),
    dp.Group(
        dp.File(file="images/largest_since_fy18_plot.png"),
        dp.File(file="images/smallest_since_fy18_plot.png"),
        columns=2,
    ),
    dp.Group(
        dp.File(file="images/largest_since_fy20_plot.png"),
        dp.File(file="images/smallest_since_fy20_plot.png"),
        columns=2,
    ),
    dp.Text(file="text/executive_summary_pt2.md").format(
        ct_site_plot=dp.File(file="images/ct_site_section_plot.png"),
        academic_affairs_plot=dp.File(file="images/academic_affairs_section_plot.png"),
        student_life_plot=dp.File(file="images/student_life_section_plot.png"),
        college_prep_plot=dp.File(file="images/college_prep_section_plot.png"),
        coaching_plot=dp.File(file="images/coaching_programming_section_plot.png"),
        wellness_plot=dp.File(file="images/wellness_programming_section_plot.png"),
        virtual_programming_plot=dp.File(
            file="images/virtual_programming_section_plot.png"
        ),
    ),
    type=dp.ReportType.REPORT
    # dp.Group(*plots[:2], columns=2),
    # plots[2],
    # dp.DataTable(subset, caption=f'Dataset for {countries}'),
)

report.publish(
    name="FY21 HS Survey Executive Summary", open=True, visibility=dp.Visibility.PUBLIC
)
