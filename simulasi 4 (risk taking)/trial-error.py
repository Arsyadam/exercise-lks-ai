# Import necessary libraries
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the main application class
class TkinterApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root    
        self.root.attributes('-fullscreen', True)
        self.root.title("Risk Rating Prediction App")
        
        # File and Data Initialization
        self.history_file = 'history.pkl'
        self.columns = ['client_name', 'predict', 'ratio', 'income', 'tenor', 'midoverdue', 
                        'age', 'employment_years', 'asset', 'debt', 'max_depth', 
                        'min_sample_split', 'min_sample_leaf', 'features', 'mode']
        self.history = self.load_history()
        
        if (self.history is None):
            self.history = pd.DataFrame(columns=self.columns)

        style = Style()
        style.configure('TNotebook.Tab', font=('Poppins', 18), padding="30 10 30 10")
        style.configure('Label.Text', font=('Poppins', 14))
        style.configure('Text.Input', font=('Poppins', 15)) 
        style.configure('Label.Description', font=('Poppins light', 15))

        # Initialize matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(6, 6))

        # Create tab control
        self.tab_control = Notebook(root)
        self.predict_tab = Frame(self.tab_control, padding="30")
        self.history_tab = Frame(self.tab_control, padding="30")
        self.setting_tab = Frame(self.tab_control, padding="30")

        # Add feature_names to class attributes
        self.all_features = ['income', 'tenor', 'dependents', 'midoverdue', 
                           'age', 'empyear', 'asset', 'debt']
        # Set default selected features (e.g. first 3 features)
        self.selected_features = self.all_features[:3]  # Default to first 3 features

        # Initialize StringVar variables for settings
        self.initialize_string_vars()

        # Add tabs to the notebook
        self.tab_control.add(self.predict_tab, text="Predict")
        self.tab_control.add(self.history_tab, text="History")
        self.tab_control.add(self.setting_tab, text="Setting")
        self.tab_control.pack(anchor='w', fill='x')

        # Initialize tabs first
        self.init_setting_tab()
        self.init_predict_tab()
        self.init_history_tab()
        
        # Then train the model
        self.train_model()

    # Initialize StringVar variables
    def initialize_string_vars(self):
        # Add default values for all variables
        self.max_depth_var = tk.StringVar(value='3')
        self.min_sample_split_var = tk.StringVar(value='2') 
        self.min_sample_leaf_var = tk.StringVar(value='1')
        self.mode_var = tk.StringVar(value='gini')
        self.post_pruning_var = tk.StringVar(value='False')
        self.alpha_var = tk.StringVar(value='1')
        # Add new StringVar for features
        self.features_var = tk.StringVar(value=', '.join(self.selected_features))

    # Input Label Creation
    def input_label(self, parent, label, value=None, textvariable=None, type='entry', help_text=None, col=None, row=None):
        Label(parent, text=label, font=('Poppins light', 14)).grid(column=col, row=row, sticky='w')
        if type == "entry":
            widget = Entry(parent, textvariable=textvariable, font=('Poppins light', 14), width=15)
        else:
            widget = Combobox(parent, textvariable=textvariable, value=value, width=15, font=('Poppins light', 17))
        
        widget.grid(column=col, row=row+1, sticky='w')
        if help_text:
            Label(parent, text=help_text, font=('Poppins italic', 8)).grid(column=col, row=row+2, sticky='w')
        return widget

    # Initialize Predict Tab
    def init_predict_tab(self):
        Label(self.predict_tab, text="BI Checking App with Decision Tree Algorithm", font=('Poppins medium', 25)).grid(column=0, row=0, sticky='w')
        Label(self.predict_tab, text="Give consideration if this type of client suit to give credit or not", font=('Poppins light', 15)).grid(column=0, row=1, sticky='w')

        self.frame_input = Frame(self.predict_tab)
        self.frame_input.grid(column=1, row=2, sticky='wn')

        # Dictionary to store entry widgets
        self.feature_entries = {}
        
        # Will be populated after feature selection
        self.create_input_fields()

        self.frame_result = Frame(self.frame_input)
        self.frame_result.grid(column=0, row=8, sticky='w')

    def create_input_fields(self):
        # Clear existing entries
        for widget in self.frame_input.winfo_children():
            widget.destroy()

        # Always show client name first
        self.client_name_entry = self.input_label(
            self.frame_input, 
            "Client Name",
            help_text="insert the name so easy to search",
            col=0, 
            row=0
        )

        # Create entries for selected features
        col = 0
        row = 3
        max_row = row
        for feature in self.selected_features:
            self.feature_entries[feature] = self.input_label(
                self.frame_input,
                feature.replace("_", " ").title(),
                help_text=f"Enter {feature} value",
                col=col,
                row=row
            )
            col += 1
            if col == 3:
                col = 0
                row += 3
                max_row = row

        # Add predict button below last input
        Button(
            self.frame_input, 
            text="Go Predict",
            command=self.predict_and_plot,
            padding="30 10 30 10"
        ).grid(column=0, row=max_row + 1, sticky='w', pady=(20,0))

        self.frame_result = Frame(self.frame_input)
        self.frame_result.grid(column=0, row=max_row + 3, sticky='w')

    # Prediction and Plotting
    def predict_and_plot(self): 
        if not self.selected_features:
            messagebox.showerror('Error', "No features selected. Please select features in Settings tab.")
            return
            
        try:
            # Validate and get input values
            values = []
            for feature in self.selected_features:
                try:
                    value = float(self.feature_entries[feature].get())
                    values.append(value)
                except ValueError:
                    messagebox.showerror('Error', f"Invalid value for {feature}")
                    return

            # Create input array and get prediction path
            full_feature_array = np.zeros(len(self.all_features))
            for i, feature in enumerate(self.all_features):
                if feature in self.selected_features:
                    idx = self.selected_features.index(feature)
                    full_feature_array[i] = values[idx]

            # Prepare input and get prediction path
            self.new_instance = full_feature_array
            self.path, decisions = self.viz.get_prediction_path(self.new_instance)
            max_step = len(decisions)

            # Handle visualization frame and canvas
            if not hasattr(self, 'frame_viz'):
                # Create frame if it doesn't exist
                self.frame_viz = Frame(self.predict_tab)
                self.frame_viz.grid(column=0, row=2, pady=(30, 0), sticky='w')
                
                # Create canvas
                self.canvas = FigureCanvasTkAgg(self.fig, self.frame_viz)
                self.canvas.get_tk_widget().grid(column=0, row=1, sticky='w')
            else:
                # Just clear existing widgets except canvas
                for widget in self.frame_viz.winfo_children():
                    if widget != self.canvas.get_tk_widget():
                        widget.destroy()

            # Add visualization slider
            self.step = tk.Scale(
                self.frame_viz, 
                from_=0, 
                to=max_step, 
                orient='horizontal',
                command=self.update_plot,
                length=500,
                tickinterval=1
            )
            self.step.grid(column=0, row=0)
             
            # Update plot
            self.update_plot(value=self.step.get())

            # Make prediction
            predict = self.model.make_predictions(self.new_instance, self.model.root)
            count = self.model.get_leaf_info(self.new_instance, self.model.root)[1]
            ratio = {k: round(v / sum(count.values()), 2) for k, v in count.items()}

            # Clear previous results
            for widget in self.frame_result.winfo_children():
                widget.destroy()

            # Create results frame
            self.title_frame = Frame(self.frame_result)
            self.title_frame.grid(column=0, row=0, sticky='w')

            # Show prediction result prominently
            Label(
                self.title_frame, 
                text=f"Risk Rating: {predict}", 
                font=('Poppins medium', 18)
            ).grid(column=0, row=0, sticky='w')

            # Show probabilities
            prob_frame = Frame(self.frame_result)
            prob_frame.grid(row=1, column=0, sticky='w', pady=(10,0))
            
            Label(
                prob_frame, 
                text="Confidence Scores:", 
                font=('Poppins medium', 12)
            ).grid(row=0, column=0, sticky='w')
            
            for i, (class_label, prob) in enumerate(ratio.items()):
                Label(
                    prob_frame,
                    text=f"Class {class_label}: {prob*100:.1f}%",
                    font=('Poppins', 10)
                ).grid(row=i+1, column=0, sticky='w')

            # Create history entry
            new_row = {
                'client_name': [self.client_name_entry.get()],
                'predict': [predict],
                'ratio': [ratio]
            }

            # Add all feature values (including zeros for unselected)
            for i, feature in enumerate(self.all_features):
                new_row[feature] = [full_feature_array[i]]

            # Add model parameters
            new_row.update({
                'max_depth': [self.max_depth_var.get()],
                'min_sample_split': [self.min_sample_split_var.get()],
                'min_sample_leaf': [self.min_sample_leaf_var.get()],
                'features': [self.features_var.get()],
                'mode': [self.mode_var.get()]
            })

            # Update history
            self.history = pd.concat([self.history, pd.DataFrame(new_row)], ignore_index=True)
            self.save_to_pickle()
            self.update_history()

            # Show input summary
            input_frame = Frame(self.frame_result)
            input_frame.grid(row=2, column=0, sticky='w', pady=(20,0))
            
            Label(
                input_frame,
                text="Input Values:",
                font=('Poppins medium', 12)
            ).grid(row=0, column=0, sticky='w', columnspan=3)

            # Display used features and their values
            col = 0
            row = 1
            for feature in self.selected_features:
                Label(
                    input_frame,
                    text=f"{feature.title()}: {self.feature_entries[feature].get()}",
                    font=('Poppins', 10)
                ).grid(row=row, column=col, sticky='w', padx=10)
                col += 1
                if col == 3:
                    col = 0
                    row += 1

        except Exception as e:
            messagebox.showerror('Error', f"Prediction error: {str(e)}")

    # Update Plot
    def update_plot(self, value):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.viz.plot_prediction_path(x=self.new_instance, step=self.step.get(), fig=self.fig, ax=self.ax)
        self.canvas.draw()  

    # Initialize History Tab
    def init_history_tab(self):
        Label(self.history_tab, text="Check History Prediction", font=('Poppins medium', 25)).grid(column=0, row=0, sticky='w')
        Label(self.history_tab, text="and compare the performance", font=('Poppins light', 15)).grid(column=0, row=1, sticky='w')

        self.history_tree = Treeview(self.history_tab, columns=('client_name', 'predict'), show='headings')
        self.history_tree.heading('client_name', text='Client Name')
        self.history_tree.heading('predict', text='Predict')
        self.history_tree.grid(column=0, row=3)
        
        Button(self.history_tab, text="Compare History", command=self.compare_history, padding="10").grid(column=0, row=5, sticky='e', pady=10)
        
        # Comparison Frames
        self.frame_compare1 = Frame(self.history_tab)
        self.frame_compare1.grid(column=0, row=6)        
        self.frame_compare2 = Frame(self.history_tab)
        self.frame_compare2.grid(column=4, row=6)
        self.update_history()

    # Compare History
    def compare_history(self):
        items_selected = self.history_tree.selection()
        
        if len(items_selected) != 2:
            messagebox.showerror('Error', "Please Select exactly 2 to Compare") 
            return

        # Clear previous contents in comparison frames
        for widget in self.frame_compare1.winfo_children():
            widget.destroy()
        for widget in self.frame_compare2.winfo_children():
            widget.destroy()

        # Get the data from history DataFrame for the selected items
        item1_data = self.history.iloc[self.history_tree.index(items_selected[0])]
        item2_data = self.history.iloc[self.history_tree.index(items_selected[1])]
        
        # Create labels for comparison in frame_compare1
        Label(self.frame_compare1, text="Comparison 1", font=('Poppins medium', 15)).grid(column=0, row=0, sticky='w')
        col = 0
        row = 1
        for column, value in item1_data.items():
            label_name = column.replace("_", " ").title()
            Label(self.frame_compare1, text=label_name, font=('Poppins light', 10)).grid(column=col, row=row, sticky='w')
            Label(self.frame_compare1, text=str(value), font=('Poppins.medium', 12)).grid(column=col, row=row+1, sticky='w')
            col += 1
            if col == 3:
                col = 0
                row += 2

        # Create labels for comparison in frame_compare2  
        Label(self.frame_compare2, text="Comparison 2", font=('Poppins medium', 15)).grid(column=0, row=0, sticky='w')
        col = 0
        row = 1
        for column, value in item2_data.items():
            label_name = column.replace("_", " ").title()
            Label(self.frame_compare2, text=label_name, font=('Poppins light', 10)).grid(column=col, row=row, sticky='w')
            Label(self.frame_compare2, text=str(value), font=('Poppins.medium', 12)).grid(column=col, row=row+1, sticky='w')
            col += 1
            if col == 3:
                col = 0
                row += 2

    # Initialize Setting Tab
    def init_setting_tab(self):
        Label(self.setting_tab, text="Adjust your best Model", font=('Poppins medium', 25)).grid(column=0, row=0, sticky='w')
        Label(self.setting_tab, text="Make your best model based on your need ", font=('Poppins light', 15)).grid(column=0, row=1, sticky='w')

        frame_input = Frame(self.setting_tab)
        frame_input.grid(column=0, row=3, sticky='n')

        # Regular settings inputs with default values
        self.max_depth_entry = self.input_label(
            frame_input, 
            "Max Depth",
            textvariable=self.max_depth_var,
            help_text="Maximum depth of the decision tree",
            col=0, row=0
        )
        self.min_sample_split_entry = self.input_label(
            frame_input,
            "Min Sample Split",
            textvariable=self.min_sample_split_var,
            help_text="Minimum samples required to split node",
            col=1, row=0
        )
        self.min_sample_leaf_entry = self.input_label(
            frame_input,
            "Min Sample Leaf",
            type='checkbox',
            textvariable=self.min_sample_leaf_var,
            help_text="Minimum samples required at leaf node",
            col=2, row=0
        )

        # Feature Selection Frame
        feature_frame = Frame(frame_input)
        feature_frame.grid(column=0, row=3, columnspan=3, sticky='w', pady=(20,0))
        
        Label(feature_frame, text="Selected Features", 
              font=('Poppins light', 14)).grid(column=0, row=0, sticky='w')
        
        # Feature Selection Listbox with default selection
        self.feature_listbox = tk.Listbox(
            feature_frame, 
            selectmode='multiple',
            height=len(self.all_features),
            font=('Poppins light', 12),
            width=20
        )
        self.feature_listbox.grid(column=0, row=1, sticky='w')

        # Populate listbox with features and select defaults
        for i, feature in enumerate(self.all_features):
            self.feature_listbox.insert(tk.END, feature)
            if feature in self.selected_features:
                self.feature_listbox.selection_set(i)

        # Display current selection
        Label(feature_frame, text="Current Selection:",
              font=('Poppins light', 10)).grid(column=0, row=2, sticky='w', pady=(5,0))
        
        self.selection_label = Label(
            feature_frame, 
            textvariable=self.features_var,
            font=('Poppins', 10),
            wraplength=400
        )
        self.selection_label.grid(column=0, row=3, sticky='w')

        self.mode_entry = self.input_label(frame_input, "Mode Impurity", 
                                         type='checkbox', 
                                         textvariable=self.mode_var, 
                                         value=['gini', 'entropy'], 
                                         help_text="Split criterion", 
                                         col=1, row=3)
        self.post_pruning_entry = self.input_label(frame_input, "Post Pruning", 
                                                 type='checkbox', 
                                                 textvariable=self.post_pruning_var, 
                                                 value=['CCP', 'REP', 'False'], 
                                                 help_text="Post-pruning method", 
                                                 col=2, row=3)
        self.alpha_entry = self.input_label(frame_input, "Alpha Value", 
                                          textvariable=self.alpha_var, 
                                          help_text="Complexity parameter for pruning", 
                                          col=3, row=3)

        Button(frame_input, 
               text="Update Model and Features", 
               command=self.update_model_and_features,
               padding="30 10 30 10").grid(column=0, row=6, sticky='w')

    def update_model_and_features(self):
        """Combined method to update features and train model"""
        # Get selected features
        selected_indices = self.feature_listbox.curselection()
        
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one feature")
            # Restore previous selection
            for i, feature in enumerate(self.all_features):
                if feature in self.selected_features:
                    self.feature_listbox.selection_set(i)
            return
        
        # Update selected features
        self.selected_features = [self.all_features[i] for i in selected_indices]
        self.features_var.set(', '.join(self.selected_features))
        
        # Update input fields in predict tab
        self.create_input_fields()
        
        # Train model
        self.train_model()

    # Train Model
    def train_model(self):
        if not self.selected_features:
            messagebox.showerror('Error', "No features selected. Please select features in Settings tab.")
            return
            
        try:
            # Handle visualization frame and canvas creation/update
            if not hasattr(self, 'frame_viz'):
                # Create visualization frame
                self.frame_viz = Frame(self.predict_tab)
                self.frame_viz.grid(column=0, row=2, pady=(30, 0), sticky='w')
                
                # Create canvas for the first time
                self.canvas = FigureCanvasTkAgg(self.fig, self.frame_viz)
                self.canvas.get_tk_widget().grid(column=0, row=1, sticky='w')
            else:
                # Clear existing widgets except canvas
                for widget in self.frame_viz.winfo_children():
                    if widget != self.canvas.get_tk_widget():
                        widget.destroy()

            # Train the model
            self.model = DecisionTreeClassifier(
                max_depth=int(self.max_depth_var.get()),
                min_sample_split=int(self.min_sample_split_var.get()),
                min_sample_leaf=int(self.min_sample_leaf_var.get()),
                features=None,
                mode=self.mode_var.get()
            )
            feature_names = ['income', 'tenor', 'dependents', 'midoverdue', 'age', 'empyear', 'asset', 'debt']
            target_col = 'riskrating'

            X = df_clean[feature_names].values
            Y = df_clean[target_col].values

            data = cross_validation(X, Y, self.model, k=5, prune=self.post_pruning_var.get(), alpha=self.alpha_var.get())
            data_df = pd.DataFrame(data['X_train'], columns=feature_names)
            data_df[target_col] = data['y_train'].flatten()

            # Update visualization
            self.viz = TreeVisualization(tree=self.model, data_df=data_df, target_col=target_col, feature_names=feature_names)
            
            # Clear and setup new plot
            self.fig.clf()
            self.ax = self.fig.add_subplot(111)
            self.viz.plot_prediction_path(fig=self.fig, ax=self.ax)
            self.canvas.draw()

            # Rest of classification report code...
            # [Previous code remains the same]

            messagebox.showinfo('Success', "Model Successfully updated")
            
        except Exception as e:
            messagebox.showerror('Error', str(e))

    # Load History from File
    def load_history(self):
        if os.path.exists(self.history_file):
            return pd.read_pickle(self.history_file)
        else:
            new_history = pd.DataFrame(columns=self.columns)
            new_history.to_pickle(self.history_file)
            return new_history

    # Save History to File
    def save_to_pickle(self):
        self.history.to_pickle(self.history_file)

    # Update History Display
    def update_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
            
        # Add new items
        for index, row in self.history.iterrows():
            values = tuple(row[col] for col in self.columns)
            self.history_tree.insert('', 'end', values=values)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = TkinterApp(root)
    root.mainloop()
