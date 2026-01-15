import tkinter as tk
from tkinter import ttk
import BackEnd

# Create main window
window = tk.Tk()
window.title("AQA Assembly Assistant")
window.geometry("1920x1008") #standard 1080p monitor without windows taskbar (40px) and header (32px)

# Buttons style
style = ttk.Style()
style.configure("style1.TButton", font=("Fixedsys", 20, "bold"))
style.configure("style1.TLabel", font=("Fixedsys", 20, "bold"), relief="sunken")

# Buttons and Frames
button_frame = ttk.Frame(master=window)
save_button = ttk.Button(master=button_frame, text="Save", style="style1.TButton")
load_button = ttk.Button(master=button_frame, text="Load", style="style1.TButton")
run_button = ttk.Button(master=button_frame, text="Run", style="style1.TButton")
runlbl_frame = ttk.Frame(master=button_frame)
runlbl_button = ttk.Button(master=runlbl_frame, text="Run line by line", style="style1.TButton")
step_button = ttk.Button(master=runlbl_frame, text="Step", style="style1.TButton")

# Packing Buttons
runlbl_button.pack(side="left", padx=1)
step_button.pack(side="left", padx=1)

save_button.pack(side="left", padx=1)
load_button.pack(side="left", padx=1)
run_button.pack(side="left", padx=1)
runlbl_frame.pack(side="left", padx=10)

button_frame.pack(side="top", anchor="nw", pady=10)

# Input box and Console
input_frame = ttk.Frame(master=window)
text_editor = tk.Text(master=input_frame, width=30, height=55)
text_console = tk.Text(master=input_frame, width=50, height=55)

# Packing Input and Console
text_editor.pack(side="left", padx=10, fill="y")
text_console.pack(side="left", padx=10)
input_frame.pack(side="left")

# Register Table
register_frame = ttk.Frame(master=window)

for i in range(0, 13):
    b = ttk.Label(register_frame, text="R{}".format(i), style="style1.TLabel")
    b.pack(side="top", pady=10)
register_frame.pack(side="left", anchor="ne", pady=25, padx=10)

window.mainloop()