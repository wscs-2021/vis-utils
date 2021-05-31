import pandas as pd
import seaborn as sns
import numpy as np
import ast
import matplotlib.pyplot as plt

class PlotAxesOptimiser:

    def __init__(self, input_path, x_axis, y_axis, hue_axis):
        """
        The PlotAxesOptimiser optimises plotting automatically for the given dataset. It reads
        the input file, applies the plotting and writes the final plots .png to disk.
        @param input_path: string, path to input dataset file
        @param x_axis: variable displayed on x_axis of plot
        @param y_axis: variable displayed on y_axis of plot
        @param hue_axis: variable displayed by color on the plot
        """
        self.data = ""
        self.input_path = input_path
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.hue_axis = hue_axis

        self._read_input()
        self.nr_of_cols = len(self.data.columns)

    def _read_input(self):
        i_ftype = self.input_path.split('.')[-1]

        if i_ftype == 'csv':
            self.data = pd.read_csv(self.input_path)
        elif i_ftype == 'json':
            self.data = pd.read_json(self.input_path)
        elif i_ftype == 'parquet':
            self.data = pd.read_parquet(self.input_path)

    # Plot with X axis
    def _do_dis(self):
        plt.figure()
        x = self.x_axis
        if self.y_axis:
            x_ax = self.y_axis
        elif self.hue_axis:
            x_ax = self.hue_axis
        sns_plot = sns.displot(data=self.data, x=x_ax)
        sns_plot.savefig("dis_plot.png")
        return "Wrote column figure "+x_ax+" to 'dis_plot.png' file."

    # Plot with X and Y or Hue axis
    def _do_rel(self):
        plt.figure()
        self.sns_plot = None
        if self.y_axis and self.hue_axis and self.x_axis:
            self.sns_plot = sns.relplot(data=self.data, x=self.x_axis, y=self.y_axis, hue=self.hue_axis)
        elif not self.hue_axis and self.x_axis and self.y_axis:
            self.sns_plot = sns.relplot(data=self.data, x=self.x_axis, y=self.y_axis)
        elif not self.y_axis and self.x_axis and self.hue_axis:
            self.sns_plot = sns.catplot(data=self.data,
                                        kind="count",
                                        y=self.x_axis,
                                        hue=self.hue_axis)
        elif not self.x_axis and self.y_axis and self.hue_axis:
            self.sns_plot = sns.catplot(data=self.data,
                                        kind="count",
                                        y=self.y_axis,
                                        hue=self.hue_axis)
        else:
            return "Error: Axes not properly specified."
        self.sns_plot.savefig("sns_plot.png")
        return "Wrote figure to 'sns_plot.png' file."

    # Read input parameters
    def decide_plot(self):
        if self.data.empty:
            return "Error: Not a .csv, .json or a .parquet file."
        elif not self.x_axis and not self.y_axis and not self.hue_axis:
            return "Error: No axes specified."
        elif (not self.y_axis and not self.hue_axis and self.x_axis in self.data.columns) or \
                (not self.x_axis and not self.hue_axis and self.y_axis in self.data.columns) or \
                (not self.x_axis and not self.y_axis and self.hue_axis in self.data.columns):
            return self._do_dis()
        elif (self.x_axis in self.data.columns and \
              (self.y_axis in self.data.columns or self.hue_axis in self.data.columns)) or \
                (self.y_axis in self.data.columns or self.hue_axis in self.data.columns):
            return self._do_rel()
        else:
            return "Error: Axis names don't correspond to file column names."
