import tkinter as tk
from tkinter import messagebox
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
    "TIF Prediction": "tifpredict.py"
}

# Step 2: Function to execute the selected Python file
def run_file(file_key):
    try:
        # Get the filename from the dictionary
        filename = gis_files[file_key]
        
        # Step 3: Use subprocess to run the selected Python file
        subprocess.run(["python", filename], check=True)
        
        # Show success message
        messagebox.showinfo("Success", f"{file_key} executed successfully!")
    except subprocess.CalledProcessError as e:
        # Show error message if the script fails
        messagebox.showerror("Error", f"Error executing {file_key}:\n{e}")
    except Exception as ex:
        # Handle unexpected errors
        messagebox.showerror("Error", f"Unexpected error:\n{ex}")

# Step 4: Create the GUI
root = tk.Tk()
root.title("GIS File Selector")

# Step 5: Add a dropdown menu for selecting GIS functions
label = tk.Label(root, text="Select a GIS Function:")
label.pack(pady=10)

selected_file = tk.StringVar()
selected_file.set(list(gis_files.keys())[0])  # Default selection

dropdown = tk.OptionMenu(root, selected_file, *gis_files.keys())
dropdown.pack(pady=10)

# Step 6: Add a button to execute the selected file
run_button = tk.Button(root, text="Run File", command=lambda: run_file(selected_file.get()))
run_button.pack(pady=10)

# Step 7: Start the GUI loop
root.mainloop()
import tkinter as tk
from tkinter import messagebox
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
    "TIF Prediction": "tifpredict.py"
}

# Step 2: Function to execute the selected Python file
def run_file(file_key):
    try:
        # Get the filename from the dictionary
        filename = gis_files[file_key]
        
        # Step 3: Use subprocess to run the selected Python file
        subprocess.run(["python", filename], check=True)
        
        # Show success message
        messagebox.showinfo("Success", f"{file_key} executed successfully!")
    except subprocess.CalledProcessError as e:
        # Show error message if the script fails
        messagebox.showerror("Error", f"Error executing {file_key}:\n{e}")
    except Exception as ex:
        # Handle unexpected errors
        messagebox.showerror("Error", f"Unexpected error:\n{ex}")

# Step 4: Create the GUI
root = tk.Tk()
root.title("GIS File Selector")

# Step 5: Add a dropdown menu for selecting GIS functions
label = tk.Label(root, text="Select a GIS Function:")
label.pack(pady=10)

selected_file = tk.StringVar()
selected_file.set(list(gis_files.keys())[0])  # Default selection

dropdown = tk.OptionMenu(root, selected_file, *gis_files.keys())
dropdown.pack(pady=10)

# Step 6: Add a button to execute the selected file
run_button = tk.Button(root, text="Run File", command=lambda: run_file(selected_file.get()))
run_button.pack(pady=10)

# Step 7: Start the GUI loop
root.mainloop()
