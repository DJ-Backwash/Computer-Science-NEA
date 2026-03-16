import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import BackEnd
import ASSEMBLY as ASM
from functools import partial
import sys

# Main Button functionality

current_file_path = None  # Global variable to remember current working file

def save_to_file():
    global current_file_path
    if current_file_path is None:
        current_file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="./code/"
        )
    if current_file_path:
        try:
            with open(current_file_path, 'w') as file:
                text_content = text_editor.get("1.0", "end-1c")
                file.write(text_content)
            console_out(f"File saved: {current_file_path}", "Success")
        except Exception as e:
            console_out(f"Error saving file: {str(e)}", "Error")

def open_file():
    global current_file_path

    ASM.refresh_reg()
    draw_registers()

    file_path = filedialog.askopenfilename(
        title="Select a Text File", 
        filetypes=[("Text files", "*.txt")], 
        initialdir="./code/"
    )

    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_editor.delete(1.0, tk.END)  # Clear previous content
            text_editor.insert(tk.END, content)
        current_file_path = file_path  # Remember the opened file for saving
        console_out(f"Loaded from {file_path}", "Success")

def save_as_to_file():
    global current_file_path
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text_content = text_editor.get("1.0", "end-1c")
                file.write(text_content)
            current_file_path = file_path  # Update the remembered path
            console_out(f"File saved as: {current_file_path}", "Success")
        except Exception as e:
            console_out(f"Error saving file: {str(e)}", "Error")

# Check for halt at end of program, return True if there is
def check_halt():
    return text_editor.get("end-1c linestart", "end-1c") == "HALT"

# Autosave and run code
def Run(x = 0):
    checkspace()
    save_to_file()
    if x == 1:
        global line, lastline
        text_editor.insert("0.0", " ")
        line = 0
        lastline = 0
    ASM.refresh_reg()
    draw_registers()
        
    if check_halt():
        console_out(f"Running {current_file_path}...\n")
        ASM.run_code(sys.modules["__main__"], current_file_path, x)
    else:
        console_out("Error: No 'HALT' at end of program.", "Error")

def New():
    global current_file_path
    if current_file_path:
        save_to_file()
        current_file_path = None
        text_editor.delete("1.0", tk.END)
        console_out(f"Text cleared succesfully", "Success")
    else:
        save_as_to_file()
    

RunLBL = partial(Run, x = 1)

def Step(): # Lines work.
    global line, lastline
    lastline = line + 1
    line = ASM.execute(sys.modules["__main__"])
    text_editor.delete(f"{lastline}.0")
    if line != "HALT":
        #text_editor.tag_add("CurrentLine", f"{line+1}.0", f"{line+1}.0 lineend")
        text_editor.insert(f"{line+1}.0", " ")
    else:
        console_out(f"HALT reached", "Success")

def checkspace(): # Method to check for spaces at the start of lines (to clear from my indentation)
    pass
    # use text_editor.index("end")

# Add text to console
def console_out(text, tag = "Default"):
    text_console.insert("end", f"{text}\n", tag)

# Create main window
window = tk.Tk()
window.title("AQA Assembly Assistant")
window.geometry("1920x1008") #standard 1080p monitor without windows taskbar (40px) and header (32px)

# Buttons style
style = ttk.Style()
style.configure("style1.TButton", font=("Fixedsys", 20, "bold"))
style.configure("style1.TLabel", font=("Fixedsys", 20, "bold"))

# Buttons and Frames
button_frame = ttk.Frame(master=window)
new_button = ttk.Button(master=button_frame, text="New", style="style1.TButton", command=New)
save_button = ttk.Button(master=button_frame, text="Save", style="style1.TButton", command=save_to_file)
load_button = ttk.Button(master=button_frame, text="Load", style="style1.TButton", command=open_file)
run_button = ttk.Button(master=button_frame, text="Run", style="style1.TButton", command=Run)
runlbl_frame = ttk.Frame(master=button_frame)
runlbl_button = ttk.Button(master=runlbl_frame, text="Run line by line", style="style1.TButton", command=RunLBL)
step_button = ttk.Button(master=runlbl_frame, text="Step", style="style1.TButton", command=Step)
saveas_button = ttk.Button(master=button_frame, text="Save As", style="style1.TButton", command=save_as_to_file)

# Packing Buttons
runlbl_button.pack(side="left", padx=1)
step_button.pack(side="left", padx=1)

new_button.pack(side="left", padx=1)
save_button.pack(side="left", padx=1)
saveas_button.pack(side="left", padx=1)
load_button.pack(side="left", padx=1)
run_button.pack(side="left", padx=1)
runlbl_frame.pack(side="left", padx=10)

button_frame.pack(side="top", anchor="nw", pady=10)

# Input box and Console
input_frame = ttk.Frame(master=window)

editor_frame = ttk.Frame(master=input_frame)
text_editor = tk.Text(master=editor_frame, width=30, height=55)
editor_scroll = tk.Scrollbar(master=editor_frame)

console_frame = ttk.Frame(master=input_frame)
text_console = tk.Text(master=console_frame, width=50, height=55)
console_scroll = tk.Scrollbar(master=console_frame)

# Packing Input and Console

# Scroll Editor
editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_editor.pack(side=tk.LEFT, fill=tk.Y)
editor_scroll.config(command=text_editor.yview)
text_editor.config(yscrollcommand=editor_scroll.set)

# Scroll Console
console_scroll.pack(side=tk.RIGHT, fill=tk.Y)
text_console.pack(side=tk.LEFT, fill=tk.Y)
console_scroll.config(command=text_console.yview)
text_console.config(yscrollcommand=console_scroll.set)

# Console Tags

text_console.tag_config("Default")
text_console.tag_config("CurrentLine", background="black", foreground="white")
text_console.tag_config("Error", foreground="red")
text_console.tag_config("Success", foreground="green")
text_console.tag_config("Out", foreground="blue")

# Packing Frames
editor_frame.pack(side="left", padx=10, fill="y")
console_frame.pack(side="left", padx=10)
input_frame.pack(side="left")

# Register Table
register_frame = ttk.Frame(master=window)
def draw_registers():
    # Clear frame
    for widget in register_frame.winfo_children():
        widget.destroy()  # deleting widget

    for i in range(0, 13):
        try:
            with open("registers.txt", "r") as f:
                registers = eval(f.read())
                x = f"{registers["R"+str(i)]:^3}"
        except:
            registers = {}
            reg_names = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"]
            for reg in reg_names:
                registers[reg] = 0

            with open("registers.txt", "w") as f:
                f.write(str(registers))
            x = f"{registers["R"+str(i)]:^3}"

        reg_row = tk.Frame(register_frame, width=200, height=100, bd=3, relief=tk.SUNKEN)
        a = ttk.Label(reg_row, text=f"{x}", style="style1.TLabel")
        b = ttk.Label(reg_row, text=f"{"R" + str(i):>3} |", style="style1.TLabel")
        b.pack(side="left")
        a.pack(side="left")
        reg_row.pack(side="top", pady=10)

    cmp_frame = tk.Frame(register_frame, width=200, height=100, bd=3, relief=tk.SUNKEN)
    cmp_statusa = ttk.Label(cmp_frame, text="N/A ", style="style1.TLabel")
    cmp_statusb = ttk.Label(cmp_frame, text="CMP | ", style="style1.TLabel")
    cmp_statusb.pack(side="left")
    cmp_statusa.pack(side="left")
    
    cmp_frame.pack(side="top", pady=40)

draw_registers()
register_frame.pack(side="left", anchor="ne", pady=25, padx=10)

window.mainloop()
ASM.refresh_reg()
with open("memory.txt", "w") as f:
        f.write("{}")
