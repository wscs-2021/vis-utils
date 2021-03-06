from os import path, remove
from plot_optimiser import PlotOptimiser
from os import path

dummy_input_path = 'tests/dummy_data/penguins.csv'
dummy_options_path = "[[['species', 'flipper_length_mm', 'sex'], 'violinplot'],[['species', 'bill_length_mm'], 'barplot']]"
dummy_x_axis = "species"
dummy_y_axis = "island"
output_path = "tests"


def test_plot():
    plot_optimiser = PlotOptimiser(
        input_path=dummy_input_path,
        output_path=output_path
    )
    plot_optimiser.decide_plot()
    paths = ['tests/island-species_plot.png', 'tests/bill_length_mm-species_plot.png', 'tests/bill_depth_mm-species_plot.png',
             'tests/flipper_length_mm-species_plot.png', 'tests/body_mass_g-species_plot.png', 'tests/sex-species_plot.png']

    for path_r in paths:
        assert path.exists(path_r) is True
        remove(path_r)


def test_plot_options():
    options_optimiser = PlotOptimiser(
        input_path=dummy_input_path,
        options=dummy_options_path,
        output_path=output_path
    )
    options_optimiser.decide_plot()
    paths = ['tests/1_species_violinplot.png', 'tests/2_species_barplot.png']

    for path_r in paths:
        assert path.exists(path_r) is True
        remove(path_r)


def test_plot_axes():
    axes_optimiser = PlotOptimiser(
        input_path=dummy_input_path,
        x_axis=dummy_x_axis,
        y_axis=dummy_y_axis,
    )
    axes_optimiser.decide_plot()
    paths = ['tests/dummy_data/sns_plot.png']

    for path_r in paths:
        assert path.exists(path_r) is True
        remove(path_r)
