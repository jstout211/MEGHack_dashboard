#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 11:27:37 2023

@author: stoutjd
"""



# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from shiny import ui, render, App
# # import MEGHack_dashboard


# choices = list(range(5)) #list(filter(lambda x: re.match(r'[a-z].*', x), dir(__builtins__)))

# dframe_fname = '/home/stoutjd/src/MEGHack_dashboard/data/TESTDATA.csv'
# dframe = pd.read_csv(dframe_fname, nrows=3000)
# dframe = dframe.loc[list(range(0,3000, 400))]

# app_ui = ui.page_fluid(
#     ui.input_selectize("plot", "Selectize (single)", choices),
#     ui.output_plot('a_scatter_plot')
# )


# # app_ui = ui.page_fluid(
# #     ui.output_plot("a_scatter_plot"),
# # )

# def server(input, output, session):
#     @output
#     @render.plot
#     def a_scatter_plot():
#         return plt.scatter(dframe.age.values, dframe.Delta.values)


# # def server(input, output, session):
# #     @output
# #     @render.plot
# #     def plot():
# #         fig, ax = plt.scatter(
# #         im = ax.imshow(data2d, cmap=input.cmap(), vmin=input.range()[0], vmax=input.range()[1])
# #         fig.colorbar(im, ax=ax)
# #         return fig


# app = App(app_ui, server)



# =============================================================================
# 
# =============================================================================

from shiny import App, render, ui
import pandas as pd
import seaborn as sns
from io import StringIO
from pathlib import Path

sns.set_theme()

data = pd.read_csv('/home/stoutjd/src/MEGHack_dashboard/data/TESTDATA.csv')

options_group = data["group"].unique().tolist()
options_parcel = data.Parcel.unique().tolist()

app_ui = ui.page_fluid(
    ui.input_selectize("group", "Group", options_group, multiple=False),
    ui.input_selectize("parcel", "Parcel", options_parcel, multiple=False),
    ui.output_table("parsed_data"),
)


def server(input, output, session):
    @output
    @render.table
    def parsed_data():
        # print(input.group())
        indx_group = data["group"].isin([int(i) for i in input.group()])

        # subset data to keep only selected group
        sub_df = data[indx_group]
        print(sub_df.shape)
        
        sub_df = sub_df[sub_df.Parcel==input.parcel()]
        return sub_df


app = App(app_ui, server)
