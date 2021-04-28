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


mpl.rcParams.update({"figure.figsize": [3.85, 3.75]})
mpl.rcParams.update({"figure.dpi": 130})

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

