import tkinter as tk  
from tkinter import messagebox  
import matplotlib.pyplot as plt  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
  
# Global variables for entry fields  
entry_x = None  
entry_y = None  
entry_z = None  
  
def plot_3d_scatter():  
    try:  
        # Get the input data from the entry fields  
        x_values = list(map(float, entry_x.get().split(',')))  
        y_values = list(map(float, entry_y.get().split(',')))  
        z_values = list(map(float, entry_z.get().split(',')))  
  
        if len(x_values) != len(y_values) or len(y_values) != len(z_values):  
            raise ValueError("All input lists must have the same length.")  
  
        # Clear the previous plot  
        ax.cla()  
  
        # Create the scatter plot  
        scatter = ax.scatter(x_values, y_values, z_values, label='Data Points', c='b', marker='o')  
  
        # Set labels  
        ax.set_xlabel('X values')  
        ax.set_ylabel('Y values')  
        ax.set_zlabel('Z values')  
        ax.set_title('3D Scatter Plot')  
  
        # Add a legend  
        ax.legend()  
  
        # Draw the updated plot  
        canvas.draw()  
  
    except ValueError as e:  
        messagebox.showerror("Input Error", f"Invalid input: {e}")  

def create_window():  
    global ax, canvas, entry_x, entry_y, entry_z  
  
    window = tk.Tk()  
    window.title("3D Scatter Plot Input")  
  
    # Create entry fields for x, y, and z values  
    tk.Label(window, text="Enter X values (comma-separated):").pack()  
    entry_x = tk.Entry(window, width=50)  
    entry_x.pack(pady=5)
  
    tk.Label(window, text="Enter Y values (comma-separated):").pack()  
    entry_y = tk.Entry(window, width=50)  
    entry_y.pack(pady=5)  
  
    tk.Label(window, text="Enter Z values (comma-separated):").pack()  
    entry_z = tk.Entry(window, width=50)  
    entry_z.pack(pady=5)  
  
    # Create a button to plot the data  
    plot_button = tk.Button(window, text="Plot 3D Scatter", command=plot_3d_scatter)  
    plot_button.pack(pady=20)  
  
    # Create a Matplotlib figure and axis  
    fig = plt.Figure(figsize=(6, 4), dpi=100)  
    ax = fig.add_subplot(111, projection='3d')  
  
    # Create a canvas to embed the plot in Tkinter  
    canvas = FigureCanvasTkAgg(fig, master=window)  
    canvas.get_tk_widget().pack()  
  
    window.mainloop()  
  
create_window()  
