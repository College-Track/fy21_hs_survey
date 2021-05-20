---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
import pandas as pd
import altair as alt

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


# largest_since_fy18_plot = helpers.plot_line_graph(
#     largest_since_fy18, "Questions With Largest Increase Since FY18"
# )

```

```python
_df = pd.melt(largest_since_fy18.iloc[:, :-1], ignore_index=False).reset_index()
```

```python
_df
```

```python
def urban_theme():
    # Typography
    font = "Lato"
    # At Urban it's the same font for all text but it's good to keep them separate in case you want to change one later.
    labelFont = "Lato" 
    sourceFont = "Lato"
    # Axes
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    # Colors
    main_palette = ["#1696d2", 
                    "#d2d2d2",
                    "#000000", 
                    "#fdbf11", 
                    "#ec008b", 
                    "#55b748", 
                    "#5c5859", 
                    "#db2b27", 
                   ]
    sequential_palette = ["#cfe8f3", 
                          "#a2d4ec", 
                          "#73bfe2", 
                          "#46abdb", 
                          "#1696d2", 
                          "#12719e", 
                         ]
return {
        "config": {
            "title": {
                "fontSize": 18,
                "font": font,
                "anchor": "start", # equivalent of left-aligned.
                "fontColor": "#000000"
            },
            "axisX": {
                "domain": True,
                "domainColor": axisColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": labelFont,
                "labelColor":fontColor
                "labelFontSize": 12,
                "labelAngle": 0, 
                "tickColor": axisColor,
                "tickSize": 5, # default, including it just to show you can change it
                "titleFont": font,
                "titleFontSize": 12,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "X Axis Title (units)", 
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": labelFont,
                "labelFontSize": 12,
                "labelAngle": 0, 
                "ticks": False, # even if you don't have a "domain" you need to turn these off.
                "titleFont": font,
                "titleFontSize": 12,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "Y Axis Title (units)", 
                # titles are by default vertical left of axis so we need to hack this 
                "titleAngle": 0, # horizontal
                "titleY": -10, # move it up
                "titleX": 18, # move it to the right so it aligns with the labels 
            },
            "range": {
                "category": main_palette,
                "diverging": sequential_palette,
            }
}
    }
```

```python
# %%html
# <style>
# @import url('https://fonts.googleapis.com/css?family=Lato');
# </style>
```

```python
# define the theme by returning the dictionary of configurations
def college_track():
    # Typography
    font = "Avenir"
    # At Urban it's the same font for all text but it's good to keep them separate in case you want to change one later.
    labelFont = "Avenir"
    sourceFont = "Avenir"
    fontColor = '#666'
    fontWeight = 425
    labelFontSize = 14
    axisTitleFontSize = 18
    titleFontSize = 22
    # Axes
    axisColor = "#666"
    gridColor = "#666"
    markColor = "#666"

    # Colors
    main_palette = [
        "#00a9e0",
        "#ffb81c",
        "#78be20",
        "#da291c",
        "#9063cd",
        "#97999b",
        "#007398",
        "#d0006f"
    ]


    return {
        'config': {

            "scale": {
                "padding": 100,
                "paddingInner":100,
                "paddingOuter":100
            },
            'view': {
                'height': 360,
                'width': 450,
                "strokeWidth": 0,
                "padding": 100
            },
            "title": {
                "fontSize": titleFontSize,
                "font": font,
                "color": fontColor,
                "anchor": "start",  # equivalent of left-aligned.
                "fontWeight": fontWeight,
                #                 "dx":50

            },
            "axisX": {
                "domain": True,
                "domainColor": axisColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": labelFont,

                "labelFontSize": labelFontSize,
                "labelColor": fontColor,
                "labelAngle": 0,
                "tickColor": axisColor,
                "ticks": False,
                "tickSize": 5,  # default, including it just to show you can change it
                "titleFont": font,
                "labelPadding": 8,
                'titleColor': fontColor,
                "titleFontSize": axisTitleFontSize,
                "titleFontWeight": fontWeight,
                "titlePadding": 10,  # guessing, not specified in styleguide
                #                 "title": "X Axis Title (units)",
            },
            "axisY": {
                "domain": True,
                "domainColor": axisColor,
                "grid": False,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": labelFont,
                "labelColor": fontColor,
                "labelFontSize": labelFontSize,
                "labelAngle": 0,
                "labelPadding": 8,
                # even if you don't have a "domain" you need to turn these off.
                "ticks": False,
                "titleFont": font,
                'titleColor': fontColor,
                "titleFontSize": axisTitleFontSize,
                "titleFontWeight": fontWeight,
                "titlePadding": 10,  # guessing, not specified in styleguide
#                 'padding':-.1
            },
            "range": {
                "category": main_palette,
                #                 "diverging": main_palette,
            },
            "legend": {
                "labelFont": labelFont,
                "labelFontSize": labelFontSize,
                "Orientation": "horizontal",
                #                 "symbolType": "square",  # just 'cause
                "symbolSize": 100,  # default
                "titleFont": font,
                "titleFontSize": 14,
                "title": "",  # set it to no-title by default

            },

            "area": {
                "fill": markColor,
            },
            "line": {
                "color": markColor,
                "stroke": markColor,
                "strokeWidth": 4,
            },
            "trail": {
                "color": markColor,
                "stroke": markColor,
                "strokeWidth": 0,
                "size": 1,
            },
            "path": {
                "stroke": markColor,
                "strokeWidth": 0.5,
            },
            "point": {
                "filled": True,
            },
            "text": {
                "font": sourceFont,
                "color": markColor,
                "fontSize": 11,
                "align": "right",
                "fontWeight": 400,
                "size": 11,
            },
            "bar": {
                "size": 40,
                "binSpacing": 1,
                "continuousBandSize": 30,
                "discreteBandSize": 30,
                "fill": main_palette[0],
                "stroke": False,
            },
            "chart":
            {"lineBreak":"\n"}

        }
    }


# register the custom theme under a chosen name
alt.themes.register('college_track', college_track)
# enable the newly registered theme
alt.themes.enable('college_track')
```

```python
alt.Chart(_df).mark_line().encode(
    alt.Y(
        'value:Q',
        scale=alt.Scale(domain=(0.25, 1))
    ),
    alt.X('variable:N',scale=alt.Scale(padding=.2)),

    color='index:N',
).configure_axis(
    grid=False
).configure_view(
    strokeWidth=0
).properties(
    title='Questions with Greatest Increase Since FY18'
)
```

```python
alt.Chart(_df).mark_line().encode(
    alt.Y(
        'value:Q',
        scale=alt.Scale(domain=(0.25, 1))
    ),
    x='variable:N',

    color='index:N',
)
```

```python

```

```python
alt.Chart(_df).mark_line().encode(
    alt.Y(
        'value:Q',
        scale=alt.Scale(domain=(0.25, 1))
    ),
    x='variable:N',

    color='index:N',
)
```

```python
_df
```

```python
_df = pd.melt(largest_since_fy18.iloc[:, :-1], ignore_index=False).reset_index()
```

```python
_df.rename(columns={'index':'test'},inplace=True)
```

```python
insert_newlines(_df['test'][0])
```

```python
_df.loc[:,'test'] = _df['test'].str.replace('\n', 'fdas', regex=True)
```

```python
def insert_newlines(string, every=64):
    return ' !n!'.join(string[i:i+every] for i in range(0, len(string), every))
```

```python
def insert_newlines(string, every=64):
    lines = []
    for i in range(0, len(string), every):
        lines.append(string[i:i+every])
    return '\n'.join(lines)
```

```python
_df.loc[:,'test'] = _df['test'].apply(lambda x:insert_newlines(x))
```

```python

```

```python

```

```python
_df
```

```python

```

```python
alt.Chart(_df).mark_bar().transform_calculate(
    y="split(datum.test, ' !n! ')"
).encode(
    x='value:Q',
    y='y:N',
).properties(
    height=300
)
```

```python
alt.Chart(_df).mark_bar().transform_calculate(
    y="split(datum.test,'!n')"
).encode(
    x='mean(value)',
    y='y:N',
)
```

```python
alt.Chart(_df).mark_bar().encode(
    ,
    
).encode(
    y='y:N'
)
```

```python

```

```python
from textwrap import wrap


```

```python

```
