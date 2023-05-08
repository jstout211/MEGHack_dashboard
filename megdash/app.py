
from shiny import App, render, ui, reactive
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import statsmodels.formula.api as smf
from io import StringIO
from pathlib import Path
import os, os.path as op

import megdash
data_path = op.join(megdash.__path__[0], 'data/TESTDATA.csv')

sns.set_theme()

data = pd.read_csv(data_path)

options_group = data["group"].unique().tolist()
options_parcel = data["Parcel"].unique().tolist()

app_ui = ui.page_fluid(
    ui.panel_title("MEG Dashboard"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize("group", "Group", options_group, multiple=False),
            ui.input_selectize("parcel", "Parcel", options_parcel, multiple=False),
            # ui.input_slider("min_age", "Minimum Age", 0, 114, 20),
            # ui.input_slider("max_age", "Maximum Age", 0, 114, 80),
        ),
        ui.panel_main(
            ui.output_ui("proc_parcel_regression"), #, class_="display-3 text-center"),
            ui.output_plot("a_scatter_plot"),
            ui.output_table("show_table"),
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def subset_df():
        # print(input.group())
        indx_group = data["group"].isin([int(i) for i in input.group()])
        indx_parcel = data["Parcel"].isin([input.parcel()])

        # subset data to keep only selected group
        sub_df = data[indx_group & indx_parcel]
        # sub_df = sub_df[sub_df['age'] > input.min_age()]
        # sub_df = sub_df[sub_df['age'] < input.max_age()]
        # print(proc_parcel_regression())
        return sub_df

    @reactive.Calc
    def group_age_range():
        age_range = []
        age_range[0] = data["group"].isin([int(input.group())]).age.min()
        age_range[1] = data["group"].isin([int(input.group())]).age.min()
        return age_range

    @reactive.Calc
    def group_subj_count():
        subj_ct = data.groupby(['group']).get_group(int(input.group())).nunique().subject
        return subj_ct

    @output
    @render.ui
    def proc_parcel_regression():
        '''Takes merged dataframe (subj_vars + parcel data)
        and performs regression of variables using statsmodels'''
        df = subset_df()
        results = smf.ols('Delta ~ age', data=df).fit()

        return ui.HTML(results.summary().as_html())

    @output
    @render.table
    def show_table():
        df = subset_df()
        return df.head()

    @output
    @render.plot(alt="Scatter Plot: Age vs Delta")
    def a_scatter_plot():
        sub_df = subset_df()
        return sns.regplot(data=sub_df, x='age', y='Alpha')


app = App(app_ui, server)
