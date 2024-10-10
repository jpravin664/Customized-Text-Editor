import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import showinfo, askyesno, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk

def change_color():
    """Change the text color."""
    color = colorchooser.askcolor(title="Pick a color")
    if color[1]:
        text_area.config(fg=color[1])

def change_font(*args):
    """Update the font style and size based on user selection."""
    text_area.config(font=(font_name.get(), font_size.get()))

def new_file():
    """Create a new file."""
    if ask_save_changes():
        window.title("Untitled")
        text_area.delete(1.0, END)

def open_file():
    """Open an existing file."""
    if ask_save_changes():
        file_path = askopenfilename(defaultextension=".txt", 
                                    filetypes=[("All Files", "*.*"), 
                                               ("Text Documents", "*.txt")])
        if file_path:
            try:
                window.title(os.path.basename(file_path))
                text_area.delete(1.0, END)
                with open(file_path, "r") as file:
                    text_area.insert(1.0, file.read())
            except Exception as e:
                showerror("Error", f"Failed to open file: {e}")

def save_file():
    """Save the current file."""
    file_path = asksaveasfilename(initialfile='Untitled.txt', 
                                  defaultextension=".txt",
                                  filetypes=[("All Files", "*.*"), 
                                             ("Text Documents", "*.txt")])
    if file_path:
        try:
            window.title(os.path.basename(file_path))
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, END))
        except Exception as e:
            showerror("Error", f"Failed to save file: {e}")

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def about():
    """Show information about the program."""
    showinfo("About", "This is a Text Editor created using Python's Tkinter library!")

def ask_save_changes():
    """Ask user to save changes if any unsaved content exists."""
    if text_area.edit_modified():
        answer = askyesno("Unsaved Changes", "Do you want to save changes?")
        if answer:
            save_file()
        return not answer  # Return True to proceed with action if no save needed
    return True

def on_quit():
    """Confirm quitting the application."""
    if ask_save_changes():
        window.destroy()

def apply_theme(theme):
    """Switch between light and dark themes."""
    if theme == "Dark":
        window.config(bg="#2C2C2C")
        text_area.config(bg="#1E1E1E", fg="white", insertbackground="white")
    else:
        window.config(bg="#F0F0F0")
        text_area.config(bg="white", fg="black", insertbackground="black")

# Initialize main window
window = Tk()
window.title("Text Editor")
window.geometry("700x500")
window.iconbitmap("img/icon.ico")  # Add your custom icon here

# Configure grid layout
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Variables for font selection
font_name = StringVar(window)
font_name.set("Arial")
font_size = StringVar(window)
font_size.set("16")

# Create text area with a scrollbar
text_area = Text(window, font=(font_name.get(), font_size.get()), undo=True, wrap=WORD)
scroll_bar = Scrollbar(text_area)
text_area.config(yscrollcommand=scroll_bar.set)
text_area.grid(sticky=N + E + S + W, padx=10, pady=10)
scroll_bar.pack(side=RIGHT, fill=Y)

# Frame for font options and color
frame = ttk.Frame(window)
frame.grid(pady=10)

# Add buttons and widgets for font, size, and color
color_button = ttk.Button(frame, text="Text Color", command=change_color)
color_button.grid(row=0, column=0, padx=10)

font_box = ttk.OptionMenu(frame, font_name, *font.families(), command=change_font)
font_box.grid(row=0, column=1, padx=10)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font, width=5)
size_box.grid(row=0, column=2, padx=10)

# Create menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_quit)

# Edit menu
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

# Help menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

# Theme menu
theme_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
theme_menu.add_command(label="Light Theme", command=lambda: apply_theme("Light"))
theme_menu.add_command(label="Dark Theme", command=lambda: apply_theme("Dark"))

# Apply default theme
apply_theme("Light")

# Main loop
window.mainloop()
 