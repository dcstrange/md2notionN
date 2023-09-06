import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import threading
import json
import sys
import os

# try:
#     # PyInstaller creates a temp folder and stores path in _MEIPASS
#     base_path = sys._MEIPASS
# except Exception:
base_path = os.path.abspath(".")

corefile = os.path.join(base_path, 'main.py')

process = None  # 存储后台进程的全局变量



# Function to load parameters from a file
def load_parameters():
    try:
        with open("config.txt", "r") as f:
            params = json.load(f)
        connection_key_entry.delete(0, tk.END)
        connection_key_entry.insert(0, params.get("connection_key", ""))
        database_id_entry.delete(0, tk.END)
        database_id_entry.insert(0, params.get("database_id", ""))
    except FileNotFoundError:
        pass  # Handle the case where the file doesn't exist

# Function to save parameters to a file
def save_parameters():
    params = {
        "connection_key": connection_key_entry.get(),
        "database_id": database_id_entry.get()
    }
    with open("config.txt", "w") as f:
        json.dump(params, f)





def on_submit():
    global process
    
    def execute_command():

        output_text.insert(tk.END, ">>> New Uploading starts. \n")
        output_text.see(tk.END)  # Auto-scroll to the end
        
        global process
        connection_key = connection_key_entry.get().strip()
        database_id = database_id_entry.get().strip()
        file_path_str = file_path.get().strip()

        params = {
            "--connection_key": connection_key,
            "--database_id": database_id,
            "--file_path": f"{file_path_str}"
        }
        args = []
        for key, value in params.items():
            args.append(key)
            args.append(value)

        process = subprocess.Popen(['python', corefile] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, bufsize=1)

        print(sys.executable)
        print(corefile)
        # print(command)

        # stdout, stderr = process.communicate()
        # print("STDOUT:", stdout)
        # print("STDERR:", stderr)

        for line in iter(process.stdout.readline, ''):
            output_text.insert(tk.END, line)
            output_text.see(tk.END)  # Auto-scroll to the end
        process.stdout.close()

        # for line in iter(process.stderr.readline, ''):
        #     output_text.insert(tk.END, line)
        #     output_text.see(tk.END)  # Auto-scroll to the end
        # process.stderr.close()

        output_text.insert(tk.END, ">>> \n")
        output_text.see(tk.END)  # Auto-scroll to the end

        process.wait()

        

    thread = threading.Thread(target=execute_command)
    thread.start()

def terminate_process():
    global process
    if process:
        process.terminate()
    output_text.insert(tk.END, ">>> User terminates the upload. \n")
    output_text.see(tk.END)  # Auto-scroll to the end

def upload_file():
    filename = filedialog.askopenfilename()
    file_path.set(filename)

# Initialize the Tkinter app


root = tk.Tk()
root.title("md2notionN")
root.geometry("800x500")

# Frame for entries and buttons
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(1, weight=1)  # Make the entry widgets expandable

# Connection Key
connection_key_label = ttk.Label(frame, text="Connection Key:")
connection_key_label.grid(row=0, column=0, sticky=tk.W)
connection_key_entry = ttk.Entry(frame)
connection_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

# Database ID
database_id_label = ttk.Label(frame, text="Database ID:")
database_id_label.grid(row=1, column=0, sticky=tk.W)
database_id_entry = ttk.Entry(frame)
database_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

# File Upload
file_button = ttk.Button(frame, text="Upload File", command=upload_file)
file_button.grid(row=2, column=0, sticky=tk.W)
file_path = tk.StringVar()
file_label = ttk.Label(frame, textvariable=file_path)
file_label.grid(row=2, column=1, sticky=(tk.W, tk.E))

# Submit and Terminate Buttons
submit_button = ttk.Button(frame, text="Submit", command=on_submit)
submit_button.grid(row=3, column=0, sticky=tk.W)
# Save parameters when submit is clicked (or whenever appropriate)
submit_button.config(command=lambda: [on_submit(), save_parameters()])

terminate_button = ttk.Button(frame, text="Terminate", command=terminate_process)
terminate_button.grid(row=3, column=1, sticky=tk.E)

# Output text box with padding and dark gray background
output_text = tk.Text(root, wrap=tk.WORD, bg="#333333", fg="white")
output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Load parameters when the application starts
load_parameters()

root.mainloop()
