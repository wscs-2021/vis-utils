test_executable: test_plot_executable test_options_executable test_axes_executable

test_plot_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" src/run.py plot;

test_options_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" OPTIONS="[[['species', 'flipper_length_mm', 'sex'], 'violinplot'],[['species', 'bill_length_mm'], 'barplot']]" OUTPUT_PATH="tests" src/run.py plot;

test_axes_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" X_AXIS="species" OUTPUT_PATH="tests" src/run.py plot;

test_none_arg_executable:
	INPUT_PATH="tests/dummy_data/penguins.csv" X_AXIS="None" Y_AXIS="None" OPTIONS="None" OUTPUT_PATH="None" src/run.py plot;