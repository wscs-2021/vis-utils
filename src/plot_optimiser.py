import pandas as pd
import seaborn as sns
import numpy as np
import ast
import matplotlib.pyplot as plt


class PlotOptimiser:

    def __init__(self, input_path):
        """
        The PlotOptimiser optimises plotting automatically for the given dataset. It reads
        the input file, applies the plotting and writes the final plots .png to disk.
        @param input_path: string, path to input dataset file
        """
        self.data = ""
        self.input_path = input_path

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
            plt.savefig(self.data.columns[i] + "-" + self.data.columns[count] + "_plot.png")
            final_string += self.data.columns[i] + "-" + self.data.columns[count] + "_plot.png\n"
        return final_string

    # Read input parameters
    def decide_plot(self):
        if self.data.empty:
            return "Error: Not a .csv, .json or a .parquet file."
        return self._do_complete()
