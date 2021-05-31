import pandas as pd
import seaborn as sns
import numpy as np
import ast
import matplotlib.pyplot as plt


class PlotOptionsOptimiser:

    def __init__(self, input_path, options):
        """
        The PlotOptionsOptimiser parses the options Schema input.
        It can plot up to 4 column_names per plot.
        The plot_name has to correspond to one of the names in self.plots
        Example Schema
        # options = [
        #           [['<column_name>'], '<plot_name']
        #           ]
        @param input_path: string, path to input dataset file
        @param options: string, path to options file
        """
        self.data = ""
        self.input_path = input_path
        self.options = options
        self.plots = ['relplot', 'scatterplot', 'lineplot', 'displot', 'histplot', 'kdeplot',
                  'ecdfplot', 'rugplot', 'catplot', 'stripplot', 'swarmplot', 'boxplot',
                  'violinplot', 'pointplot', 'barplot']

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

    # Plot options
    def _plot_options(self):
        final_string = ""
        count = 1
        for option in self.options:
            plt.figure()
            fig_name = str(count)+"_"+option[0][0]+"_"+option[1]+".png"
            if option[1] not in self.plots:
                return "Error: Plot name not recognized. The following are supported: " + self.plots
            elif not set(option[0]).issubset(set(self.data.columns)):
                return "Error: Input column names do not correspond to the data column names."
            elif len(option[0]) == 1:
                self.sns_plot = eval("sns."+option[1]+"(data=self.data, x=option[0][0])")
            elif len(option[0]) == 2:
                self.sns_plot = eval("sns."+option[1]+"(data=self.data, x=option[0][0], y=option[0][1])")
            elif len(option[0]) == 3:
                self.sns_plot = eval("sns."+option[1] +
                                     "(data=self.data, x=option[0][0], y=option[0][1], hue=option[0][2])")
            elif len(option[0]) == 4:
                self.sns_plot = eval("sns."+option[1] +
                                     "(data=self.data, x=option[0][0], y=option[0][1], hue=option[0][2], col=option[0][3])")
            else:
                return "Error: Too many columns to plot for " + fig_name
                continue
            count += 1
            plt.savefig(fig_name)
            final_string += fig_name + "\n"
        return "Wrote figures to:\n" + str(final_string)

    # Read input parameters
    def decide_plot(self):
        if self.data.empty:
            return "Error: Not a .csv, .json or a .parquet file."
        elif self.options:
            return self._plot_options()
        else:
            return "Error: Options not set properly."
