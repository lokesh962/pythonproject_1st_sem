import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database Connection Setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",     
        user="root",          
        password="Lokesh@9628",  
        database="notes_db"   
    )

# Functions
def add_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END)
    
    if title.strip() == "":
        messagebox.showwarning("Input Error", "Title cannot be empty.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    conn.commit()
    cursor.close()
    conn.close()
    
    messagebox.showinfo("Success", "Note added successfully!")
    clear_entries()
    load_notes()

def load_notes():
    notes_listbox.delete(0, tk.END)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM notes")
    for row in cursor.fetchall():
        notes_listbox.insert(tk.END, f"{row[0]} - {row[1]}")
    cursor.close()
    conn.close()

def view_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a note to view.")
        return
    
    note_id = int(notes_listbox.get(selected[0]).split(" - ")[0])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if note:
        title_entry.delete(0, tk.END)
        title_entry.insert(tk.END, note[0])
        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, note[1])

def delete_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a note to delete.")
        return

    note_id = int(notes_listbox.get(selected[0]).split(" - ")[0])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cursor.close()
    conn.close()

    messagebox.showinfo("Success", "Note deleted successfully!")
    clear_entries()
    load_notes()

def update_note():
    selected = notes_listbox.curselection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a note to update.")
        return

    note_id = int(notes_listbox.get(selected[0]).split(" - ")[0])
    title = title_entry.get()
    content = content_text.get("1.0", tk.END)
    
    if title.strip() == "":
        messagebox.showwarning("Input Error", "Title cannot be empty.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    messagebox.showinfo("Success", "Note updated successfully!")
    clear_entries()
    load_notes()

def clear_entries():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

# Widgets
root = tk.Tk()
root.title("Notes App")
root.config(bg="grey")
title_label = tk.Label(root, text="Title:")
title_label.grid(row=0, column=0, padx=10, pady=10)

title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=10)

content_label = tk.Label(root, text="Content:")
content_label.grid(row=1, column=0, padx=10, pady=10, sticky="N")

content_text = tk.Text(root, width=40, height=10)
content_text.grid(row=1, column=1, padx=10, pady=10)

add_button = tk.Button(root, text="Add Note", command=add_note)
add_button.grid(row=2, column=0, padx=10, pady=10)

view_button = tk.Button(root, text="View Note", command=view_note)
view_button.grid(row=2, column=1, padx=10, pady=10, sticky="W")

update_button = tk.Button(root, text="Update Note", command=update_note)
update_button.grid(row=2, column=1, padx=10, pady=10)

delete_button = tk.Button(root, text="Delete Note", command=delete_note)
delete_button.grid(row=2, column=1, padx=10, pady=10, sticky="E")

notes_listbox = tk.Listbox(root, width=50)
notes_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Load Notes on Start
load_notes()

root.mainloop()
