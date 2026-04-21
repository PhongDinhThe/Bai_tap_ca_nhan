import tkinter as tk

# ===== Window setup =====
root = tk.Tk()
root.title("Calculator")
root.geometry("320x450")
root.resizable(False, False)
root.configure(bg="#1e1e1e")

# ===== Display =====
expression = ""

input_text = tk.StringVar()

input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(expand=True, fill="both")

input_field = tk.Entry(
    input_frame,
    textvariable=input_text,
    font=("Segoe UI", 24),
    bd=0,
    bg="#1e1e1e",
    fg="white",
    justify="right"
)
input_field.pack(expand=True, fill="both", padx=10, pady=20)

# ===== Functions =====
def press(key):
    global expression
    expression += str(key)
    input_text.set(expression)


def clear():
    global expression
    expression = ""
    input_text.set("")


def equal():
    global expression
    try:
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""

# ===== Buttons =====
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(expand=True, fill="both")

buttons = [
    ("C", 1, 0), ("/", 1, 1), ("*", 1, 2), ("-", 1, 3),
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("+", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("=", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("0", 5, 0),
    (".", 5, 1)
]

for (text, row, col) in buttons:
    action = lambda x=text: press(x)
    if text == "C":
        action = clear
    elif text == "=":
        action = equal

    btn = tk.Button(
        btn_frame,
        text=text,
        font=("Segoe UI", 14),
        bd=0,
        fg="white",
        bg="#333333",
        activebackground="#555555",
        command=action
    )

    btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

# Grid config
for i in range(6):
    btn_frame.rowconfigure(i, weight=1)
for j in range(4):
    btn_frame.columnconfigure(j, weight=1)

# ===== Run =====
root.mainloop()