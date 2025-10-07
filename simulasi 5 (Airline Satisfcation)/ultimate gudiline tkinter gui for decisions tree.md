## Import necessery library
## Define the main aplication

# Initilize the main window
1. file and data initialization (pkl file, column and load_history)
2. init style
3. init subplot
4. create tab control(Notebook)
5. init default train model setting
6. add tab to the notebook
7. init train model and the tabs

# function default value of training input

# create reusable input
# init the predict tab
1. title
2. create input
3. button predict & plot

# predict and plot
1. new_instance array of int input
2. get prediction path to get max step
3. Scale step (slider)
4. fig.clf
5. make predict, count and ratio
6. plot predict path and canvas draw
7. create new_row. concat to history, with new row convert df
8. save pickle & update history
9. loop and print all new row

# update plot
1. fig.clf
2. ax = fig add subplot
3. plot prediction path
4. canvas draw

# Init History Tab
1. Title
2. Treeview init to history_tree
3. frame_compare & update history

# Compare History
1. get history tree selection
2. error handilnng if select != 2
3. loop frame compare winfo_children destroy
4. get item 1 and 2 
5. loop label item 1 and 2

# Init Setting Tab
1. title and create frame
2. create input for setting model & evaluation model
3. button train mode

# train model (try exception)
1. fig.clf
2. FigureCanvas, canvas draw and get_tk_widget
3. define the model based on default setting
4. set feature names and target col
5. split X Y data and crossvalidation
6. classification report
7. loop label classification report

# Load history
if exist: read pickle
else blank dataframe, to pickle

# save to pickle 
history to pickle

# update history
1. loop item history tree to get children
2. history tree delete item
3. loop iterrows history
4. values loop tuple row col in columns
5. history tree insert '', 'end' and values