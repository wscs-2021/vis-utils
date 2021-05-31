test_plot_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" src/run.py plot;

test_options_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" OPTIONS="[[['species', 'flipper_length_mm', 'sex'], 'violinplot'],[['species', 'bill_length_mm'], 'barplot']]" src/run.py plot_options;

test_axes_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" X_AXIS="species" src/run.py plot_axes;