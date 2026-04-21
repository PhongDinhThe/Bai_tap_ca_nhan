import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Kết nối database
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()


# ================== HÀM ==================
def delete_low_gpa():
    confirm = messagebox.askyesno("Xác nhận", "Xóa tất cả sinh viên GPA < 2.0?")
    if not confirm:
        return

    cursor.execute("DELETE FROM students WHERE gpa < 2.0")
    conn.commit()
    load_data()
    messagebox.showinfo("OK", "Đã xóa sinh viên GPA < 2.0")

def filter_gpa():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def load_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)


def add_student():
    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (id_entry.get(), name_entry.get(), major_entry.get(), float(gpa_entry.get()))
        )
        conn.commit()
        load_data()
        clear_fields()
    except:
        messagebox.showerror("Lỗi", "ID bị trùng hoặc dữ liệu sai!")


def delete_student():
    selected = tree.selection()
    if not selected:
        return
    id = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    load_data()


def update_student():
    selected = tree.focus()
    values = tree.item(selected, "values")
    id = values[0]
    gpa = float(gpa_entry.get())
    cursor.execute("""
    UPDATE students
    SET name=?, major=?, gpa=?
    WHERE id=?
    """, (name_entry.get(), major_entry.get(), gpa, id))
    conn.commit()
    load_data()


def search_student():
    keyword = name_entry.get()
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + keyword + '%',))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)


def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    major_entry.delete(0, tk.END)
    gpa_entry.delete(0, tk.END)


def select_item(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])["values"]
        id_entry.delete(0, tk.END)
        id_entry.insert(0, values[0])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        major_entry.delete(0, tk.END)
        major_entry.insert(0, values[2])
        gpa_entry.delete(0, tk.END)
        gpa_entry.insert(0, values[3])


# ================== GIAO DIỆN ==================
root = tk.Tk()
root.title("Quản lý sinh viên")
root.geometry("700x500")

# Form nhập
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(frame)
id_entry.grid(row=0, column=1)

tk.Label(frame, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(frame)
name_entry.grid(row=1, column=1)

tk.Label(frame, text="Major").grid(row=2, column=0)
major_entry = tk.Entry(frame)
major_entry.grid(row=2, column=1)

tk.Label(frame, text="GPA").grid(row=3, column=0)
gpa_entry = tk.Entry(frame)
gpa_entry.grid(row=3, column=1)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Thêm", width=10, command=add_student).grid(row=0, column=0)
tk.Button(btn_frame, text="Sửa", width=10, command=update_student).grid(row=0, column=1)
tk.Button(btn_frame, text="Xóa", width=10, command=delete_student).grid(row=0, column=2)
tk.Button(btn_frame, text="Tìm", width=10, command=search_student).grid(row=0, column=3)
tk.Button(btn_frame, text="Làm mới", width=10, command=load_data).grid(row=0, column=4)
tk.Button(btn_frame, text="GPA > 3.0", width=12, command=filter_gpa).grid(row=2, column=1)
tk.Button(btn_frame, text="Xóa GPA < 2.0", width=15, command=delete_low_gpa).grid(row=2, column=3)

# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Major", "GPA"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Major", text="Major")
tree.heading("GPA", text="GPA")

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", select_item)

# Load dữ liệu ban đầu
load_data()
root.mainloop()
conn.close()
