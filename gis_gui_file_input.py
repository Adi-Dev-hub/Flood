import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import subprocess

# Map user-friendly names to Python filenames
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

# Function to browse for files
def browse_file(file_type, entry_widget):
    """Open a file dialog and update the entry field with the selected file path."""
    file_types = [("Shapefiles", "*.shp")] if file_type == "shp" else [("TIFF files", "*.tif")]
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        entry_widget.delete(0, tk.END)  # Clear previous entry
        entry_widget.insert(0, file_path)  # Insert the selected file path

# Function to execute the selected script
def run_file(file_key):
    """Run the selected GIS file with optional file inputs."""
    try:
        # Get the filename from the dictionary
        filename = gis_files[file_key]
        
        # Get file inputs from the entry widgets
        shp_file = shp_entry.get().strip()
        tif_file = tif_entry.get().strip()
        
        # Use default values if no file is provided
        if not shp_file:
            shp_file = "pune.shp"  # Default .shp placeholder
        if not tif_file:
            tif_file = "pune.tif"  # Default .tif placeholder
        
        # Prepare the command with file inputs
        command = ["python", filename, shp_file, tif_file]
        
        # Execute the script
        result = subprocess.run(command, capture_output=True, text=True)
        
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

# Create the GUI
root = tk.Tk()
root.title("GIS File Selector and Processor")
root.geometry("750x600")  # Set the size of the window
root.configure(bg="#f0f8ff")  # Light blue background

# Title label
title_label = tk.Label(root, text="GIS Script Executor with File Inputs", font=("Helvetica", 16, "bold"), bg="#f0f8ff", fg="#333")
title_label.pack(pady=10)

# Dropdown for selecting GIS functions
selected_file = tk.StringVar()
selected_file.set(list(gis_files.keys())[0])  # Default selection

dropdown_label = tk.Label(root, text="Select a GIS Function:", font=("Helvetica", 12), bg="#f0f8ff")
dropdown_label.pack(pady=5)

dropdown = tk.OptionMenu(root, selected_file, *gis_files.keys())
dropdown.config(font=("Helvetica", 10), bg="#e0e0e0", fg="#333")
dropdown.pack(pady=5)

# Input field for .shp file
shp_label = tk.Label(root, text="Select .shp File (Optional):", font=("Helvetica", 12), bg="#f0f8ff")
shp_label.pack(pady=5)

shp_entry = tk.Entry(root, width=50, font=("Helvetica", 10), fg="#999")
shp_entry.insert(0, "Default: pune.shp")  # Placeholder text
shp_entry.bind("<FocusIn>", lambda event: shp_entry.delete(0, tk.END) if shp_entry.get() == "Default: pune.shp" else None)
shp_entry.bind("<FocusOut>", lambda event: shp_entry.insert(0, "Default: pune.shp") if not shp_entry.get() else None)
shp_entry.pack(pady=5)

shp_button = tk.Button(root, text="Browse .shp", command=lambda: browse_file("shp", shp_entry), bg="#4caf50", fg="white", relief="raised")
shp_button.pack(pady=5)

# Input field for .tif file
tif_label = tk.Label(root, text="Select .tif File (Optional):", font=("Helvetica", 12), bg="#f0f8ff")
tif_label.pack(pady=5)

tif_entry = tk.Entry(root, width=50, font=("Helvetica", 10), fg="#999")
tif_entry.insert(0, "Default: pune.tif")  # Placeholder text
tif_entry.bind("<FocusIn>", lambda event: tif_entry.delete(0, tk.END) if tif_entry.get() == "Default: pune.tif" else None)
tif_entry.bind("<FocusOut>", lambda event: tif_entry.insert(0, "Default: pune.tif") if not tif_entry.get() else None)
tif_entry.pack(pady=5)

tif_button = tk.Button(root, text="Browse .tif", command=lambda: browse_file("tif", tif_entry), bg="#4caf50", fg="white", relief="raised")
tif_button.pack(pady=5)

# Run button
run_button = tk.Button(
    root, text="Run File", command=lambda: run_file(selected_file.get()),
    font=("Helvetica", 12), bg="#4caf50", fg="white", relief="raised"
)
run_button.pack(pady=10)

# Output text area
output_label = tk.Label(root, text="Script Output:", font=("Helvetica", 12), bg="#f0f8ff")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=85, height=15, font=("Courier", 10), bg="#fff")
output_text.pack(pady=10)

# Start the GUI loop
root.mainloop()
