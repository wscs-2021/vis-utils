from os import path, remove
from pathlib import Path
from plot_optimiser import PlotOptimiser
from plot_axes_optimiser import PlotAxesOptimiser
from plot_options_optimiser import PlotOptionsOptimiser

dummy_input_path = 'tests/dummy_data/penguins.csv'
dummy_options_path = "[[['species', 'flipper_length_mm', 'sex'], 'violinplot'],[['species', 'bill_length_mm'], 'barplot']]"
dummy_x_axis = "species"
dummy_y_axis = "island"

plot_optimiser = PlotOptimiser(
    input_path=dummy_input_path
)
options_optimiser = PlotOptionsOptimiser(
    input_path=dummy_input_path,
    options=dummy_options_path
)
axes_optimiser = PlotAxesOptimiser(
    input_path=dummy_input_path,
    x_axis=dummy_x_axis,
    y_axis=dummy_y_axis,
    hue_axis=""
)

def test_plot():
    data = plot_optimiser.decide_plot()
    paths = ['island-species_plot.png', 'bill_length_mm-species_plot.png', 'bill_depth_mm-species_plot.png',
             'flipper_length_mm-species_plot.png', 'body_mass_g-species_plot.png', 'sex-species_plot.png']
    for path in paths:
        assert path.exists(Path(path)) is True
        remove(Path(path))



def test_plot_options():
    data = options_optimiser.decide_plot()
    paths = ['1_species_violinplot.png', '2_species_barplot.png']

    for path in paths:
        assert path.exists(Path(path)) is True
        remove(Path(path))


def test_plot_axes():
    data = axes_optimiser.decide_plot()
    paths = ['sns_plot.png']

    for path in paths:
        assert path.exists(Path(path)) is True
        remove(Path(path))
