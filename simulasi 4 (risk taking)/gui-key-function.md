## Import necessery library
## Define the main aplication

# Initilize the main window
1. file and data initialization (pkl file, column and load_history) if 
2. init style
3. init subplots
4. create tab control(Notebook)
5. set all feature and selected features
5. init default train model setting
6. add tab to the notebook
7. init train model and the tabs

# function default value of training input
1. feature var=,join selected feature

# create reusable input

# init the predict tab
1. title
2. frame input
3. init feature entries
2. create input fields

# create_input_fields
1. winfo_children frame input destroy
2. set input title of prediction 
3. loop input based on feture_select define to feature entries
3. button predict & plot
4. frame result


# predict and plot (try excepetion)
1. value = blank arr
2. Validate and get input values (loop feature in selected try: value float fture entries feature get append to values except, messagebox)
3. full_feature_array = np.zeros(len all features)
4. loop feature all feature, if featuture selected idx = self selected feature index, insert value based on index
5. new_instance full feature array
6. get prediction path and get max_step
7. Handle visualization frame viz and canvas
   - Create frame if it doesn't exist
   - Create canvas
   - Just clear existing widgets except canvas
8. step scale
9. update_plot
10. make prediction and ratio
11. winfo clear frame result
12. title frame and prob_frame
13. create new_row
14. create input frame
15.             # Add all feature values (including zeros for unselected)
16. Loop the result all
17. history concat, save to pickle and update history

# update plot
1. fig.clf
2. ax = fig add subplot
3. plot prediction path
4. canvas draw

# Init History Tab
1. Title
2. Treeview init to history_tree
3. frame_compare1,2 & update history

# Compare History
1. get history tree selection
2. error handilnng if select != 2
3. winfo_children destroy
4. get item 1 and 2 with iloc
5. loop label item 1` and 2

# Init Setting Tab
1. title and create frame
2. create input for setting model & evaluation model
3. Feature Selection Listbox with default selection
4. Populate listbox with features and select defaults
5. Display current selection 
4. button train mode

# update_model_and_features 
Selected curselection
error if not select
selected features loop of curselection
feature_Var set(, join selected features)
create input fields
train model

# train model (try exception)
2. frame viz
3. FigureCanvasTk
4. w_info if widget not canvas, destroy
5. feature indiceis : list-range-len of selected feature
6. Call DecisionTreeClassifier
7. X Selected and Y df clean
8. cross validation
9. data df based on cross validation
10. tree visualization
11. fig.clf, addsubplot, canvas draw
12. Show classification Report
1. w_info_children destroy clf_frame
13. Success

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