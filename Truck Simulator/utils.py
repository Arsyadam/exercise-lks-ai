import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx

def get_distance(path, df_edgelist):
	distance = 0
	for i in range(1, len(path)):
		path1 = f'{path[i-1]} {path[i]}'
		path2 = f'{path[i]} {path[i-1]}'
		distance += int(df_edgelist.loc[df_edgelist['pair'].str.contains(f'{path1}|{path2}'), 'distance'].values[0])
	return distance

def get_side_job(route_df):
	input_total_side_job = int(input('Input how many side jobs: '))
	indices_side_job = []
	for i in range(input_total_side_job):
		input_index_side_job = int(input(f'{i+1} job: '))
		if input_index_side_job in route_df.index:
			indices_side_job.append(input_index_side_job)
		elif input_index_side_job not in route_df.index:
			raise ValueError("== THE INDEX IS NOT AVAILABLE ==")
	return indices_side_job

def check_combo(route_df, indices_side_job):
	jenis_muatan = np.sort(route_df.loc[indices_side_job, 'JENIS'].values)
	if set(jenis_muatan) == {'CAIR', 'GAS', 'PADAT'}:
		raise ValueError("== THIS COMBO IS NOT ALLOWED ==")
	return jenis_muatan

def check_combo_addition(jenis_muatan):
	jenis_counter = dict(Counter(jenis_muatan))
	addition_muatan = np.sum([
     	jenis_counter.get(jenis) for jenis in set(jenis_muatan) 
      	if (jenis == 'CAIR') | (jenis == 'GAS')
     ]) * 4
	return addition_muatan

def calc_muatan_after_addition(route_df, indices_side_job, addition_muatan, muatan):
	total_muatan = np.sum(route_df.loc[indices_side_job, 'BEBAN MUATAN (TON)'].values)
	total_muatan += addition_muatan
	if total_muatan > muatan:
		raise ValueError("== TRUCK CAPACITY IS NOT ENOUGH ==")
	return total_muatan

def get_reward_df(df, initial, goal):
	filtered = df[(df['INITIAL'] == initial) & (df['GOAL'] == goal)]
	if filtered.empty:
		return 0, 0
	filtered = filtered.sort_values(['REWARD', 'SOLAR (L)', 'DISTANCE'], ascending=[False, True, True])
	index = np.argmax(list(filtered['REWARD']))
	reward_end = filtered['REWARD'].iloc[index]
	return reward_end, 1

def highlight_path(G, pos, route):
	plt.figure(figsize=(15, 7), edgecolor='white')
	edge_list = list(zip(route, route[1:]))
	edge_label = nx.get_edge_attributes(G, 'distance')

	nx.draw_networkx_nodes(G, pos=pos)
	nx.draw_networkx_edges(G, pos=pos)

	nx.draw_networkx_nodes(G, pos=pos, node_color='red', nodelist=route)
	nx.draw_networkx_edges(G, pos=pos, edge_color='red', edgelist=edge_list)

	nx.draw_networkx_labels(G, pos=pos)
	nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_label)
	plt.show()