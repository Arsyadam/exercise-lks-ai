import customtkinter as ctk
from tkinter import messagebox

def save_settings():
    messagebox.showinfo("Settings", "Settings saved successfully!")

def show_emissions():
    messagebox.showinfo("Emissions", "Your emissions data is being calculated...")

# Configure the appearance of the app
ctk.set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

# Create the main application window
root = ctk.CTk()
root.title("Custom TabView Example")
root.geometry("960x540")

# Create a TabView widget
tabs = ctk.CTkTabview(root, width=500, height=300)
tabs.pack(anchor="w", fill="both", expand=True)

# Tab 1: Home
home_tab = tabs.add("Home")
home_label = ctk.CTkLabel(home_tab, text="See the Emissions Unleashed", font=("Roboto", 30, "bold"))
home_label2 = ctk.CTkLabel(home_tab, text="One Prediction at a Time!", font=("Roboto", 30, "bold"))
home_label.pack(anchor="w", pady=0)
home_label2.pack(anchor="w", pady=0)

# Create a frame to hold the inputs and button
input_frame = ctk.CTkFrame(home_tab)
input_frame.pack(anchor="w", pady=20)

# Create 4 input fields with labels inside
engine_size_entry = ctk.CTkEntry(input_frame, placeholder_text="Engine Size")
engine_size_entry.grid(row=0, column=0, padx=5)

cylinder_entry = ctk.CTkEntry(input_frame, placeholder_text="Cylinder")
cylinder_entry.grid(row=0, column=1, padx=5)

fuel_consumption_l_entry = ctk.CTkEntry(input_frame, placeholder_text="Fuel Consumption (L/100km)")
fuel_consumption_l_entry.grid(row=0, column=2, padx=5)

fuel_consumption_mpg_entry = ctk.CTkEntry(input_frame, placeholder_text="Fuel Consumption (Mpg)")
fuel_consumption_mpg_entry.grid(row=0, column=3, padx=5)

emission_label = ctk.CTkLabel(home_tab, text="Emission Rate", font=("Roboto", 16, "bold"))
emission_label.pack(anchor="w", pady=5)

emission_frame = ctk.CTkFrame(home_tab,)
emission_rate_label = ctk.CTkLabel(emission_frame, text="323.00", font=("Roboto", 16))
emission_rate_label.pack(anchor="w", pady=5)
emission_frame.pack(anchor="w", pady=0)

# Add a button in the first row
calculate_button = ctk.CTkButton(input_frame, text="Calculate Emissions", command=show_emissions)
calculate_button.grid(row=0, column=4, padx=5)

# Model Performance Section
performance_label = ctk.CTkLabel(home_tab, text="Model Performance", font=("Roboto", 16, "bold"))
performance_label.pack(anchor="w", pady=5)


performance_frame = ctk.CTkFrame(home_tab)
performance_frame.pack(anchor="w", pady=0)

accuracy_label = ctk.CTkLabel(performance_frame, text="Accuracy: 95%", font=("Roboto", 16))
accuracy_label.pack(anchor="w", pady=5)

loss_curve_label = ctk.CTkLabel(performance_frame, text="Loss Curve: [Graph Placeholder]", font=("Roboto", 16))
loss_curve_label.pack(anchor="w", pady=5)

# Most Similar Data Section
similar_data_label = ctk.CTkLabel(home_tab, text="Most Similar Data", font=("Roboto", 16, "bold"))
similar_data_label.pack(anchor="w", pady=5)

similar_data_frame = ctk.CTkFrame(home_tab)
similar_data_frame.pack(anchor="w", pady=0)

# Create table headers
headers = ["Vehicle Type", "Make", "Fuel Type", "Fuel Consumption (Mpg)", "Emission Rate"]
for i, header in enumerate(headers):
    header_label = ctk.CTkLabel(similar_data_frame, text=header, font=("Roboto", 14, "bold"))
    header_label.grid(row=0, column=i, padx=5, pady=5)

# Example data for the table
data = [
    ["Avanza Xinea", "4", "8.5", "27.7", "200"],
    ["Avanza Xinea", "6", "10.0", "23.5", "250"],
    ["Avanza Xinea", "4", "7.0", "33.6", "180"],
    ["Avanza Xinea", "8", "12.0", "20.0", "300"],
    ["Avanza Xinea", "6", "9.0", "25.0", "220"]
]

# Populate the table with data
for row_index, row_data in enumerate(data, start=1):
    for col_index, item in enumerate(row_data):
        data_label = ctk.CTkLabel(similar_data_frame, text=item, font=("Roboto", 14))
        data_label.grid(row=row_index, column=col_index, padx=5, pady=5)

# Tab 2: Settings
settings_tab = tabs.add("Settings")
settings_label = ctk.CTkLabel(settings_tab, text="Adjust Your Preferences", font=("Roboto", 16))
settings_label.pack(anchor="w")

save_button = ctk.CTkButton(settings_tab, text="Save Settings", command=save_settings)
save_button.pack(anchor="w", pady=10)

# Tab 3: About
about_tab = tabs.add("About")
about_label = ctk.CTkLabel(about_tab, text="Moklet Dev\nVersion 1.0", font=("Roboto", 16), justify="left")
about_label.pack(anchor="w", pady=20)

# Run the application
root.mainloop()
