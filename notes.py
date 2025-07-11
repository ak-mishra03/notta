import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_notes():
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

def refresh_list():
    notes_listbox.delete(0, tk.END)
    for title in notes:
        notes_listbox.insert(tk.END, title)

def add_note():
    title = simpledialog.askstring("New Note", "Enter note title:")
    if title and title not in notes:
        notes[title] = ""
        save_notes()
        refresh_list()
    elif title in notes:
        messagebox.showwarning("Duplicate", "A note with this title already exists.")

def delete_note():
    selected = notes_listbox.curselection()
    if not selected:
        return
    title = notes_listbox.get(selected)
    if messagebox.askyesno("Delete", f"Delete note '{title}'?"):
        del notes[title]
        save_notes()
        refresh_list()
        text.delete(1.0, tk.END)

def load_selected_note(event=None):
    selected = notes_listbox.curselection()
    if not selected:
        return
    title = notes_listbox.get(selected)
    text.delete(1.0, tk.END)
    text.insert(tk.END, notes[title])

def save_current_note():
    selected = notes_listbox.curselection()
    if not selected:
        return
    title = notes_listbox.get(selected)
    notes[title] = text.get(1.0, tk.END).strip()
    save_notes()

# Load data
notes = load_notes()

# UI
root = tk.Tk()
root.title("Gnote-like Notes App")
root.geometry("700x400")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

notes_listbox = tk.Listbox(frame_left, width=30)
notes_listbox.pack(fill=tk.Y, expand=True)
notes_listbox.bind('<<ListboxSelect>>', load_selected_note)

btn_add = tk.Button(frame_left, text="Add Note", command=add_note)
btn_add.pack(fill=tk.X, pady=2)

btn_delete = tk.Button(frame_left, text="Delete Note", command=delete_note)
btn_delete.pack(fill=tk.X, pady=2)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

text = tk.Text(frame_right, wrap=tk.WORD)
text.pack(fill=tk.BOTH, expand=True)

btn_save = tk.Button(root, text="Save Note", command=save_current_note)
btn_save.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

refresh_list()
root.mainloop()

