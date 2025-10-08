import os
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import networkx as nx
import pydeck as pdk

from utils import get_distance, get_side_job, check_combo, check_combo_addition, calc_muatan_after_addition, get_reward_df, highlight_path

# Pastikan path dataset relatif terhadap lokasi app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

connections_df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "edgelist.csv"))
location_df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "dataset_lat-long_jatim_processed.csv"))
shipment_df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "Dataset-barang-angkut_processed.csv"))


with open(os.path.join(BASE_DIR, 'data.pkl'), 'rb') as file:
	data = pickle.load(file)
INITIAL = list(data['INITIAL'])
GOAL = list(data['GOAL'])
DF = data['DF']
G = data['G']
DF_EDGELIST = data['DF_EDGELIST']
POSITIONS = data['POS']


tab1, tab2, tab3 = st.tabs(['Prime Trip', 'Ceperan Trip', 'Go Home Trip'])

with tab1:
	st.title('Truck Simulator East Java 🇮🇩')
	st.write("### We'll give you the best route!") 
	
	col1, col2 = st.columns(2)
	with col1:
		initial_input = st.selectbox('Initial', (INITIAL))
		muatan_start_input = st.number_input('Muatan (Ton): ', step=1, min_value=0, value=40, format='%d')
	with col2:
		goal_input = st.selectbox('Goal', (GOAL))
		solar_start_input = st.number_input('Solar (L): ', step=1, min_value=0, value=40, format='%d')


	path_start = nx.shortest_path(G,method="dijkstra", source=initial_input, target=goal_input)
	reward_start, get_start_job = get_reward_df(DF, initial=initial_input, goal=goal_input)
	distance_start = get_distance(path_start, DF_EDGELIST)
	solar_start = round(distance_start / 20,1)
 
	if initial_input == goal_input:
		st.error('== INPUT AND GOAL SAME ==')
	else:
		st.write('### Your Start Trip')
		st.write(f'Initial: {initial_input}')
		st.write(f'Goal: {goal_input}')
		st.write(f'Reward: {reward_start}')
		st.write(f'Distance: {distance_start}')
		st.write(f'Solar: {solar_start}')
		st.write(f'Path: {path_start}')

	if solar_start_input == 0:
		st.error("== NOT ENOUGH SOLAR ==")
	else:
		all_paths = []
		all_solar = []
		all_rewards = []
		all_distances = []
		all_job_back_home = []
		all_initial_back = []
		all_goal_back = []
		all_rewards_back = []
		all_distances_back = []
		
		route_df = DF[DF['INITIAL'] == goal_input]
		solar_filteration = route_df[route_df['SOLAR (L)'] <= solar_start_input]
		muatan_filteration = solar_filteration[solar_filteration['BEBAN MUATAN (TON)'] < muatan_start_input]
		route_df = muatan_filteration
		route_df = route_df.sort_values(['REWARD', 'SOLAR (L)', 'DISTANCE'], ascending=[False, True, True])
		if len(route_df) == 0:
			st.error("== NOT ENOUGH SOLAR ==")
   
		for i in route_df.index:
			paths = [] 
			job_back_home = 0
			total_rewards = 0
			paths.append(path_start)
			total_rewards += reward_start


			initial_bridge = goal_input
			goal_bridge = str(route_df.loc[i, 'GOAL'])
			path_bridge = nx.shortest_path(G, method="dijkstra", source=initial_bridge, target=goal_bridge)
			paths.append(path_bridge[1:])
			distance_bridge = get_distance(path_bridge, DF_EDGELIST)
			reward_bridge = route_df.loc[i, 'REWARD']

			initial_end = goal_bridge
			goal_end = initial_input
			path_end = nx.shortest_path(G, method="dijkstra", source=initial_end, target=initial_input)
			paths.append(path_end[1:])
			distance_back = get_distance(path_end, DF_EDGELIST)
			reward_end, job_back_home = get_reward_df(DF, initial=initial_end, goal=goal_end)
	
	
			total_rewards = (reward_start + reward_bridge + reward_end)
			all_rewards_back.append(reward_end)
			all_distances_back.append(distance_back)
			all_initial_back.append(initial_end)
			all_goal_back.append(goal_end)
			flattened_paths = [item for sublist in paths for item in sublist]  
			all_paths.append(flattened_paths)
			all_rewards.append(total_rewards)
			all_job_back_home.append(job_back_home)
	
	
		route_df['JOB_BACK_HOME'] = all_job_back_home
		route_df['INITIAL_BACK'] = all_initial_back
		route_df['GOAL_BACK'] = all_goal_back
		route_df['REWARDS_BACK'] = all_rewards_back
		route_df['DISTANCE_BACK'] = all_distances_back
		route_df['TOTAL_REWARDS'] = all_rewards
		route_df['PATH'] = all_paths

		for path in all_paths:
			distance = get_distance(path, DF_EDGELIST)
			all_distances.append(distance)
		route_df['TOTAL_DISTANCE_PATH'] = all_distances
		route_df['TOTAL_SOLAR'] = route_df['TOTAL_DISTANCE_PATH'] / 20	


with tab2:
	if solar_start_input != 0:
		route_df = route_df[route_df['TOTAL_SOLAR'] < solar_start_input].sort_values(['REWARD', 'SOLAR (L)', 'DISTANCE'], ascending=[False, True, True])
		ceperan_goals = set(route_df['GOAL'].values)
		st.write(f'#### Ceperan Goal')
		ceperan_goal_input = st.selectbox('Input', (ceperan_goals))
		route_df = route_df[route_df['GOAL'] == ceperan_goal_input]
		st.write(f'#### Ceperan untuk pulang dari {goal_input}')
		goals_available = list(set(route_df['GOAL'].values))
		# Display as a single-column table
		route_df['SELECT'] = False
		route_df = route_df[['SELECT'] + [col for col in route_df.columns if col != 'SELECT']]
		route_df = st.data_editor(route_df,
					disabled=['ID','INITIAL','GOAL','BEBAN MUATAN (TON)','REWARD','JENIS'],
					column_config={
						'SELECT': st.column_config.CheckboxColumn(label="Select")
					},
					use_container_width=True,
					hide_index=True
					)
		st.write('#### Job 👷🏼‍♂ yang kamu pilih: ')
		selected_df = route_df[route_df['SELECT'] == True]
		total_rewards_side_job = 0
		total_muatan_side_job = 0
		addition_muatan_side_job = 0
		all_jenis_side_job = []
		if len(selected_df) != 0:
			for index in selected_df.index:
				from_point = route_df.loc[index, 'INITIAL']
				to_point = route_df.loc[index, 'GOAL']
				distance_side_job = route_df.loc[index, 'DISTANCE']
				reward_side_job = route_df.loc[index, 'REWARD']
				jenis_side_job = route_df.loc[index, 'JENIS']
				if jenis_side_job in ['CAIR', 'GAS']:
					addition_muatan_side_job = 4
				muatan_side_job = route_df.loc[index, 'BEBAN MUATAN (TON)'] + addition_muatan_side_job
				total_rewards_side_job += reward_side_job
				total_muatan_side_job += muatan_side_job
				all_jenis_side_job.append(jenis_side_job)
			st.write(f'Total Job: {len(selected_df)}')
			st.write(f'From point: {from_point}')
			st.write(f'To point: {to_point}')
			st.write(f'Reward side job: {total_rewards_side_job}')
			st.write(f'Muatan side job: {total_muatan_side_job}')
			st.write(f'Jenis side job: {all_jenis_side_job}')

	
		selected_jenis = set(selected_df['JENIS'].values)
		if selected_jenis == {'CAIR', 'GAS', 'PADAT'}:
			st.error("== COMBO CAIR GAS PADAT IS NOT ALLOWED ==")

		if len(route_df) == 0:
			st.error("== NO TRIP / NOT ENOUGH SOLAR ==")


with tab3:
	if solar_start_input != 0:	
		st.write(f'#### Go Back to {initial_input} from {ceperan_goal_input}')
		initial_back = route_df['INITIAL_BACK'].iloc[0]
		goal_back = route_df['GOAL_BACK'].iloc[0]
		rewards_back = route_df['REWARDS_BACK'].iloc[0]
		distance_back = route_df['DISTANCE_BACK'].iloc[0]
		initial_row = selected_df[(selected_df['INITIAL'] == initial_back) & (selected_df['GOAL'] == goal_back)]
		st.write(f'Initial back: {initial_back}')
		st.write(f'Goal back: {goal_back}')
		st.write(f'Rewards back: {rewards_back}')
		st.write(f'Distance back: {distance_back} \n')
		
		total_distance_path = route_df['TOTAL_DISTANCE_PATH'].iloc[0]
		total_solar = route_df['TOTAL_SOLAR'].iloc[0]
		total_rewards = (reward_start + total_rewards_side_job + rewards_back)
		path = route_df['PATH'].iloc[0]
		st.write(f'Total rewards: {total_rewards}')
		st.write(f'Total Distance: {total_distance_path}')
		st.write(f'Total solar: {total_solar}')
		st.write(f'Path: {path}')

		# Ensure each node has a 'pos' attribute
		for node in G.nodes:
			if 'pos' not in G.nodes[node]:
				G.nodes[node]['pos'] = (location_df.loc[location_df['Daerah'] == node, 'Longitude'].values[0],
										location_df.loc[location_df['Daerah'] == node, 'Latitude'].values[0])

		edge_paths = [
			{"path": [G.nodes[edge[0]]["pos"], G.nodes[edge[1]]["pos"]]}
			for edge in G.edges
		]

		edge_layer = pdk.Layer(
		"PathLayer",
		data=edge_paths,
		get_path="path",
		get_color=[173, 216, 230],  # Light blue color
		width_scale=20,
		width_min_pixels=2,
		get_width=3,
		)


		# Define the ScatterplotLayer for nodes
		node_layer = pdk.Layer(
		"ScatterplotLayer",
		data=[
			{"position": G.nodes[node]["pos"], "Daerah": node, "color": [255, 0, 0]}  # Red for nodes
			for node in G.nodes
		],
		get_position="position",
		get_fill_color="color",
		get_radius=2000,
		pickable=True,
		)
		
		path = route_df['PATH'].iloc[0]
		edge_list = [{"path": [G.nodes[edge[0]]["pos"], G.nodes[edge[1]]["pos"]]} for edge in zip(path, path[1:])]
		trip_layer = pdk.Layer(
			"PathLayer",
			data=edge_list,
			get_path="path",
			get_color=[0, 0, 230],  # Light blue color
			width_scale=20,
			width_min_pixels=2,
			get_width=3,
		)


		# Define the initial view state
		view_state = pdk.ViewState(
			latitude=location_df["Latitude"].mean(),
			longitude=location_df["Longitude"].mean(),
			zoom=7,
		)

		st.title("Graph on Map with Source-Target Connections")

		# # Render the Pydeck chart in Streamlit
		st.pydeck_chart(pdk.Deck(layers=[ edge_layer, node_layer, trip_layer], initial_view_state=view_state, tooltip={"text": "{Daerah}"}))