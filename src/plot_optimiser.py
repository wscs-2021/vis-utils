import pandas as pd
import seaborn as sns
import numpy as np
import ast
import matplotlib.pyplot as plt


class PlotOptimiser:

    def __init__(self, input_path, x_axis=None, y_axis=None, 
        hue_axis=None, options=None, output_path=None):
        """
        The PlotOptimiser optimises plotting automatically for the given dataset. It reads
        the input file, applies the plotting and writes the final plots .png to disk.
        Example Schema
        # options = [
        #           [['<column_name>'], '<plot_name']
        #           ]
        @param input_path: string, path to input dataset file
        @param x_axis: variable displayed on x_axis of plot (optional)
        @param y_axis: variable displayed on y_axis of plot (optional)
        @param hue_axis: variable displayed by color on the plot (optional)
        @param options: string, path to options file (optional)
        @param input_path: string, path to output figure file (optional)
        """
        self.data = None
        self.input_path = input_path
        self.options = ast.literal_eval(options) if options else None
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.hue_axis = hue_axis
        self.output_path = output_path if output_path else self.input_path.rsplit('/', 1)[0]
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

    # Plot every possible column
    def _do_complete(self):
        final_string = "Wrote figures to:\n"
        count = 0
        # find proper y-axis column
        while not (self.data[self.data.columns[count]].nunique() < 10 and self.data.dtypes[count] == np.object) or \
                (self.data.dtypes[count] != np.object and "id" not in self.data.columns[count].lower()):
            count += 1
        if count > self.nr_of_cols:
            return "Error: Couldn't visualize columns, too many distinct values."
        for i in range(self.nr_of_cols):
            plt.figure()
            if i == count or self.data.columns[count] == self.data.columns[i]:
                continue
            elif self.data[self.data.columns[i]].nunique() > 10 and (self.data.dtypes[i] == np.object or
                                                                     "id" in self.data.columns[i].lower()):
                final_string += "Error: Column " + str(self.data.columns[i]) + \
                                " has too many distinct values to plot.\n"
                continue
            elif '[' in str(self.data.iloc[0][i]):
                final_string += "Error in" + str(self.data.columns[i]) + ": Column values can't be arrays.\n"
                continue
            elif self.data.dtypes[count] == np.object and self.data.dtypes[i] == np.object:
                self.sns_plot = sns.catplot(data=self.data,
                                            kind="count",
                                            y=self.data.columns[count],
                                            hue=self.data.columns[i])
            elif self.data.dtypes[count] == np.object and self.data.dtypes[i] != np.object:
                self.sns_plot = sns.barplot(data=self.data,
                                            x=self.data.columns[i],
                                            y=self.data.columns[count])
            elif self.data.dtypes[count] != np.object and self.data.dtypes[i] != np.object:
                self.sns_plot = sns.barplot(data=self.data,
                                            x=pd.to_numeric(self.data[self.data.columns[i]], errors='coerce'),
                                            y=pd.to_numeric(self.data[self.data.columns[count]], errors='coerce'))
            elif self.data.dtypes[count] != np.object and self.data.dtypes[i] == np.object and \
                    self.data[self.data.columns[i]].nunique() < 30:
                self.sns_plot = sns.barplot(data=self.data,
                                            x=pd.to_numeric(self.data[self.data.columns[count]], errors='coerce'),
                                            y=self.data.columns[i])
            else:
                final_string += "Error: Couldn't plot " + self.data.columns[i] + "_plot.png\n"
                continue
            plt.savefig(self.output_path + "/" + self.data.columns[i] + "-" + self.data.columns[count] + "_plot.png")
            final_string += self.output_path + "/" + self.data.columns[i] + "-" + self.data.columns[count] + "_plot.png\n"
        return final_string

    # Plot options
    def _plot_options(self):
        # options = [
        #           [['<column_name>'], '<plot_name']
        #           ]
        final_string = ""
        count = 1
        for option in self.options:
            plt.figure()
            fig_name = self.output_path + "/" + str(count)+"_"+option[0][0]+"_"+option[1]+".png"
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
            final_string += self.output_path + "/" + fig_name + "\n"
        return "Wrote figures to:\n" + str(final_string)

    # Plot with X axis
    def _do_dis(self):
        plt.figure()
        x_ax = self.x_axis
        if self.y_axis:
            x_ax = self.y_axis
        elif self.hue_axis:
            x_ax = self.hue_axis
        sns_plot = sns.displot(data=self.data, x=x_ax)
        sns_plot.savefig(self.output_path + "/" + "dis_plot.png")
        return "Wrote column figure "+x_ax+" to " + self.output_path + "/dis_plot.png file."

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
        self.sns_plot.savefig(self.output_path + "/" + "sns_plot.png")
        return "Wrote figure to " + self.output_path + "/sns_plot.png' file."

    # Read input parameters
    def decide_plot(self):
        if self.data.empty:
            return "Error: Not a .csv, .json or a .parquet file."
        elif self.options:
            return self._plot_options()
        elif not self.x_axis and not self.y_axis and not self.hue_axis:
            return self._do_complete()
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
