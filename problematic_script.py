def run_file(file_key):
    """Run the selected GIS file and handle errors."""
    try:
        # Get the filename from the dictionary
        filename = gis_files[file_key]
        
        # Execute the file
        result = subprocess.run(["python", filename], check=True, capture_output=True, text=True)
        
        # Show success message
        messagebox.showinfo("Success", f"{file_key} executed successfully!\n\nOutput:\n{result.stdout}")
    
    except subprocess.CalledProcessError as e:
        # Show detailed error message from the script
        messagebox.showerror("Execution Error", f"Error while running {file_key}:\n\n{e.stderr}")
    
    except FileNotFoundError:
        # Handle file not found errors
        messagebox.showerror("File Not Found", f"The file {filename} does not exist!")
    
    except Exception as ex:
        # Handle any unexpected errors
        messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n\n{ex}")
