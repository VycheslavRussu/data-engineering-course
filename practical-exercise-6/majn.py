import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_list = []

df1 = pd.DataFrame()
df1_cols = ["h_score", "v_score", "day_of_week", "h_name", "length_outs", "v_hits", "v_doubles", "v_triples",
			"v_homeruns", "v_rbi"]

for chunk in pd.read_csv('[1]game_logs.csv', chunksize=10000,
						 usecols=df1_cols, low_memory=False, index_col=False):
	df1 = pd.concat([df1, chunk], ignore_index=True)
df_list.append(df1)


def plot_linear(data, x, y, name):
	plt.title(name)
	sns.lineplot(data=data.sample(1000), x=x, y=y, errorbar=None)
	plt.savefig(name+'.png')
	plt.close()


def plot_step(data, x, y, name):
	plt.title(name)
	sns.stripplot(data=data.sample(1000), x=x, y=y, dodge=True)
	plt.savefig(name+'.png')
	plt.close()


def plot_boxplot(df, x, y, name):
	sns.boxplot(data=df.sample(1000), x=x, y=y)
	plt.savefig(name+'.png')
	plt.close()


def plot_histogram(df, x, y, name):
	sns.histplot(data=df.sample(1000), x=x, y=y)
	plt.savefig(name+'.png')
	plt.close()


def analyze_data(source_dataframe: pd.DataFrame):
	file_size = source_dataframe.memory_usage(deep=True).sum()
	memory_usage = source_dataframe.memory_usage(deep=True).sum()
	col_sizes = []
	for col in source_dataframe.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		col_sizes.append({'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	sorted_df = source_dataframe.loc[:, source_dataframe.dtypes != object]
	sorted_sizes = []
	for col in sorted_df.columns:
		col_size = source_dataframe[col].memory_usage(deep=True)
		col_type = source_dataframe[col].dtype
		sorted_sizes.append(
			{'column': col, 'size': col_size, 'percent': col_size / memory_usage, 'type': str(col_type)})
	return {'file_size': file_size, 'memory_usage': memory_usage, 'col_sizes': col_sizes, 'sorted_sizes': sorted_sizes}


result_analyze = []
for df in df_list:
	result_analyze.append(analyze_data(df))

with open('answer.json', 'a') as f:
	for index, data in enumerate(result_analyze):
		json.dump({f'df{index}_memory_usage': data['col_sizes']}, f)


def convert_data(df):
	converted_data = df.copy()
	for column in converted_data.columns:
		if converted_data[column].dtype == 'object':
			unique_values = converted_data[column].unique()
			if len(unique_values) < 50:
				converted_data[column] = converted_data[column].astype('category')
			if converted_data[column].dtype == 'int64':
				converted_data[column] = converted_data[column].astype(np.int32)
			elif converted_data[column].dtype == 'float64':
				converted_data[column] = converted_data[column].astype(np.float32)
	return converted_data


def analyze_optimized_data(df):
	return convert_data(df)


def compare_memory_usage(source_data, optimized_data):
	source_data_memory = source_data.memory_usage(deep=True).sum()
	optimized_data_memory = optimized_data.memory_usage(deep=True).sum()
	if source_data_memory > optimized_data_memory:
		print("success optimization diff between src data and optimized data - " + str(
			source_data_memory - optimized_data_memory))
	else:
		print("fail optimization diff between src data and optimized data - " + str(
			optimized_data_memory - source_data_memory))


for index, data in enumerate(df_list):
	optimized_data = analyze_optimized_data(data)
	compare_memory_usage(data, optimized_data)
	optimized_data.to_csv(f'optimized_df_{index + 1}.csv')


plot_linear(df1, "v_score", "h_score", "df_1_plot_1")
plot_linear(df1, "v_hits", "v_doubles", "df_1_plot_2")
plot_linear(df1, "v_hits", "v_triples", "df_1_plot_3")
plot_step(df1, "v_homeruns", "v_hits", "df_1_plot_4")
plot_step(df1, "v_homeruns", "v_score", "df_1_plot_5")