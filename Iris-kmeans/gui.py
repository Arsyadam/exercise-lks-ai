import pickle
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from components import KNN, elbow_method_silhoutte, euclidean, elbow_method_inertia

def load():
    with open("data.pkl", "rb") as file:
        data = pickle.load(file)
    return data

loaded_var = load()

silhoutte_scores = loaded_var["silhouette"]
inertia_scores = loaded_var["inertia"]
df = loaded_var["df"]
standard_df = loaded_var["standard_df"]
independent = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
dependent = df['labels']

KNN = KNN()
KNN.fit(np.array(independent), np.array(dependent))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")

        self.frames = {}
        self.buttons = {}
        for page in ("Predict", "Settings", "Information"):
            frame = ttk.Frame(self)
            frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
            self.frames[page] = frame

        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="ew", padx=50, pady=(50, 20))
        for page in self.frames:
            button = ttk.Button(button_frame, text=page, command=lambda p=page: self.show_frame(p))
            button.pack(side="left", padx=10, pady=10)
            self.buttons[page] = button

        # ============= Predict Page ================
        self.show_frame("Predict")
        label = ttk.Label(self.frames["Predict"], text="Get Appropriate, \rBeautiful Iris Flower", font=("Roboto", 64), justify="left")
        label.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        
        input_frame = ttk.Frame(self.frames["Predict"], width=1500, height=200)
        input_frame.grid(row=1, column=0, padx=0, pady=(60, 20), sticky="nsew")
        
        label_sepal_length = ttk.Label(input_frame, text="Sepal Length", font=("Roboto", 16), justify="left")
        label_sepal_length.grid(row=0, column=0, sticky="w", padx=50, pady=(50, 0))
        input_sepal_length = ttk.Entry(input_frame, width=20)
        input_sepal_length.grid(row=1, column=0, padx=50, pady=(0, 50))
        
        label_sepal_width = ttk.Label(input_frame, text="Sepal Width", font=("Roboto", 16), justify="left")
        label_sepal_width.grid(row=0, column=1, sticky="w", padx=50, pady=(50, 0))        
        input_sepal_width = ttk.Entry(input_frame, width=20)
        input_sepal_width.grid(row=1, column=1, padx=50, pady=(0, 50))

        label_petals_length = ttk.Label(input_frame, text="Petals Length", font=("Roboto", 16), justify="left")
        label_petals_length.grid(row=0, column=2, sticky="w", padx=50, pady=(50, 0))
        input_petals_length = ttk.Entry(input_frame, width=20)
        input_petals_length.grid(row=1, column=2, padx=50, pady=(0, 50))
        
        label_petals_width = ttk.Label(input_frame, text="Petals Width", font=("Roboto", 16), justify="left")
        label_petals_width.grid(row=0, column=3, sticky="w", padx=50, pady=(50, 0))
        input_petals_width = ttk.Entry(input_frame, width=20)
        input_petals_width.grid(row=1, column=3, padx=50, pady=(0, 50))
        
        def predict_input():
            new_input = np.array([float(input_sepal_length.get()), float(input_sepal_width.get()), float(input_petals_length.get()), float(input_petals_width.get())])
            result = KNN._predict(new_input)
            predict_result_label.config(text=result)
        
        submit_button = ttk.Button(input_frame, text="Predict", command=predict_input)
        submit_button.grid(row=1, column=4, padx=50, pady=(0, 50))
        
        frame = ttk.Frame(self.frames["Predict"])
        frame.grid(row=2, column=0, padx=0, pady=0, sticky="nsew")
        
        predict_result = ttk.Label(frame, text="Prediction Result", font=("Roboto", 18), justify="left")
        predict_result.grid(row=1, column=1, padx=0, pady=0, sticky="w")
        predict_result_label = ttk.Label(frame, text="*Make Prediction First", font=("Roboto", 45), justify="left")
        predict_result_label.grid(row=2, column=1, padx=0, pady=0, sticky="w")
        
        # ============= Settings Page ================
        self.show_frame("Settings")
        
        label = ttk.Label(self.frames["Settings"], text="Customize your needs, \rMake the predict more precise", font=("Roboto", 64), justify="left")
        label.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        fig = elbow_method_silhoutte(silhoutte_scores)  
        canvas = FigureCanvasTkAgg(fig, master=self.frames["Settings"])
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        
        fig = elbow_method_inertia(inertia_scores)  
        canvas = FigureCanvasTkAgg(fig, master=self.frames["Settings"])
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=1, padx=0, pady=0, sticky="nsew")

    def show_frame(self, page):
        for p, button in self.buttons.items():
            if p == page:
                button.config(style="TButton")
            else:
                button.config(style="TButton")
        frame = self.frames[page]
        frame.tkraise()

app = App()
app.mainloop()
