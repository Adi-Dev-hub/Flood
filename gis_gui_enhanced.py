import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess

# Step 1: Map user-friendly names to Python filenames
gis_files = {
    "Create Files": "createFiles.py",
    "Display Files": "displayFiles.py",
    "Interpolation": "interpolation.py",
    "LULC Prediction": "lulcpredict.py",
    "Rainfall Analysis": "rainele.py",
    "Rain Preparation": "rainpre.py",
    "Slope Calculation": "slope.py",
    "Slope and Rain": "sloperain.py",
    "TIF Prediction": "tifpredict.py",
    "HEAT MAP":"tifdis.py"
}

# Step 2: Function to execute the selected Python file
def run_file(file_key):
    """Run the selected GIS file and display output in the GUI."""
    try:
        # Get the filename from the dictionary
        filename = gis_files[file_key]
        
        # Execute the file and capture its output
        result = subprocess.run(["python", filename], capture_output=True, text=True)
        
        # Display the script's output in the text area
        output_text.delete(1.0, tk.END)  # Clear previous output
        if result.returncode == 0:
            output_text.insert(tk.END, f"--- {file_key} Output ---\n{result.stdout}\n")
        else:
            output_text.insert(tk.END, f"--- {file_key} Error ---\n{result.stderr}\n")
    
    except FileNotFoundError:
        # Handle file not found errors
        messagebox.showerror("File Not Found", f"The file {gis_files[file_key]} does not exist!")
    except Exception as ex:
        # Handle unexpected errors
        output_text.insert(tk.END, f"Unexpected Error: {ex}\n")

# Step 3: Create the GUI
root = tk.Tk()
root.title("GIS File Selector and Executor")
root.geometry("600x400")  # Set the size of the window
root.configure(bg="#f0f8ff")  # Light blue background

# Add a title label
title_label = tk.Label(root, text="FLOOD PREDICTION", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333")
title_label.pack(pady=10)

# Add a dropdown menu for selecting GIS functions
selected_file = tk.StringVar()
selected_file.set(list(gis_files.keys())[0])  # Default selection

dropdown_label = tk.Label(root, text="Select a Factor for Prediction:", font=("Helvetica", 12), bg="#f0f8ff")
dropdown_label.pack(pady=5)

dropdown = tk.OptionMenu(root, selected_file, *gis_files.keys())
dropdown.config(font=("Helvetica", 10), bg="#e0e0e0", fg="#333")
dropdown.pack(pady=5)

# Add a button to execute the selected file
run_button = tk.Button(
    root, text="Run File", command=lambda: run_file(selected_file.get()),
    font=("Helvetica", 12), bg="#4caf50", fg="white", relief="raised"
)
run_button.pack(pady=10)

# Add a text area to display the output
output_label = tk.Label(root, text="Script Output:", font=("Helvetica", 12), bg="#f0f8ff")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Courier", 10), bg="#fff")
output_text.pack(pady=10)

# Start the GUI loop
root.mainloop()
