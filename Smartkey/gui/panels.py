import tkinter as tk
from tkinter import messagebox
from database import *
from services import *

root = tk.Tk()
root.title("SmartKey")
root.geometry("950x800")

def show_panel2():
    panel_2()

# Prvi panel
def panel_1():
    panel1 = tk.Frame(root, bg="#8ecae6", pady=2, borderwidth=1, relief="solid", height=200)
    panel1.pack(side="top", fill="both", expand=False, padx=5, pady=2)
    label = tk.Label(panel1, text="Panel s gumbima", font=("Arial", 10))
    label.pack(padx=10, pady=10)
    
    button1 = tk.Button(panel1, text="Pozvoni", font=("Helvetica", 14), width=8, height=2, command=lambda: ring_bell())
    button1.pack(side="left", padx=20)

    button2 = tk.Button(panel1, text="Otključaj", font=("Helvetica", 14), width=8, height=2, command=show_panel2)
    button2.pack(side="right", padx=20)
panel_1()
# Drugi panel
def panel_2():   
    panel2 = tk.Frame(root, bg="#dee2e6", borderwidth=1, relief="solid")
    panel2.pack(side="top", fill="both", expand=False, padx=5, pady=2)
    panel2.config(height=5)

    label2 = tk.Label(panel2, text="Pin panel", font=("Arial", 10))
    label2.pack(padx=10, pady=10)

    inner_frame1 = tk.Frame(panel2, bg="#dee2e6",  relief="solid", width=50, height=50)
    inner_frame2 = tk.Frame(panel2, bg="#ffffff", borderwidth=1, relief="solid", width=50, height=50)
    inner_frame2.config(width=200, height=200)

    inner_frame1.pack(side="left", padx=10, pady=10, expand=True, fill="both")
    inner_frame2.pack(side="left", padx=10, pady=10,ipady=60, expand=True, fill="x", anchor="ne")

    pin_box_frame = tk.Frame(inner_frame1, bg="#dee2e6", relief="solid")
    pin_box_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=(10,0))

    pin1_value = tk.StringVar()
    pin1 = tk.Label(pin_box_frame, textvariable=pin1_value, font=("Helvetica", 20), width=2, height=1, relief="groove")
    pin1.grid(row=0, column=0, padx=2, pady=2, sticky="W")

    pin2_value = tk.StringVar()
    pin2 = tk.Label(pin_box_frame, textvariable=pin2_value, font=("Helvetica", 20), width=2, height=1, relief="groove")
    pin2.grid(row=0, column=1, padx=2, pady=2, sticky="W")

    pin3_value = tk.StringVar()
    pin3 = tk.Label(pin_box_frame, textvariable=pin3_value, font=("Helvetica", 20), width=2, height=1, relief="groove")
    pin3.grid(row=0, column=2, padx=2, pady=2, sticky="W")

    pin4_value = tk.StringVar()
    pin4 = tk.Label(pin_box_frame, textvariable=pin4_value, font=("Helvetica", 20), width=2, height=1, relief="groove")
    pin4.grid(row=0, column=3, padx=2, pady=2, sticky="W")

    def enter_button_action():
        access_control.check_pin(pin1_value, pin2_value, pin3_value, pin4_value, generated_message_text, panel_3)
        access_control.clear_pin(pin1_value, pin2_value, pin3_value, pin4_value)

    def keyboard_button_action(num):
        access_control.update_pin(num, pin1_value, pin2_value, pin3_value, pin4_value)
    
    keyboard_frame = tk.Frame(inner_frame1, bg="#ffffff")
    keyboard_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=10)

    for i in range(1, 10):
        button = tk.Button(keyboard_frame, text=i, font=("Helvetica", 14), width=5, height=2, command=lambda num=i: keyboard_button_action(num))
        button.grid(row=(i-1)//3, column=(i-1)%3, pady=5)

    clear_button = tk.Button(keyboard_frame, text="C", font=("Helvetica", 14), width=5, height=2, command=lambda: access_control.clear_pin(pin1_value, pin2_value, pin3_value, pin4_value))

    clear_button.grid(row=3, column=1, pady=5)

    zero_button = tk.Button(keyboard_frame, text="0", font=("Helvetica", 14), width=5, height=2)
    zero_button.grid(row=3, column=2, pady=5)
        
    enter_button = tk.Button(keyboard_frame, text="Enter", font=("Helvetica", 14), width=5, height=2, command=enter_button_action)
    enter_button.grid(row=3, column=0, pady=5, padx=(5, 0), sticky="w")

    status_label = tk.Label(inner_frame2, text="Status i poruke", font=("Helvetica", 14), fg="#2a9d8f")
    status_label.pack(side="top", padx=2, pady=(1,10), fill="x")

    generated_message_text = tk.Text(inner_frame2, height=10, width=10, font=("Helvetica", 12), wrap=tk.WORD)
    generated_message_text.pack(side="top", padx=2, pady=(0,1), fill="x", expand=False)

# Treći panel
def panel_3():
    panel3 = tk.Frame(root, bg="#edf2f4", pady=10, borderwidth=1, relief="solid")
    panel3.pack(side="top", fill="both", expand=True, padx=5, pady=2)
    
    listbox_frame = tk.Frame(panel3, bg="#edf2f4")
    listbox_frame.pack(side="left",fill="both", padx=40)

    listbox_label = tk.Label(listbox_frame, text="Popis korisnika s ključevima", font=("Helvetica", 14), fg="#2a9d8f")
    listbox_label.pack(pady=10)

    listbox = tk.Listbox(listbox_frame, font=("Helvetica", 14), width=35, height=10)
    listbox.pack()
    
    get_users_from_db(listbox)
    
    form_frame = tk.Frame(panel3, bg="#edf2f4")
    form_frame.pack(side="left", padx=10, pady=10)

    name_label = tk.Label(form_frame, text="Ime", font=("Helvetica", 14))
    name_label.grid(row=0, column=0, padx=5, pady=5)

    name_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=20)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    surname_label = tk.Label(form_frame, text="Prezime", font=("Helvetica", 14))
    surname_label.grid(row=1, column=0, padx=5, pady=5)

    surname_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=20)
    surname_entry.grid(row=1, column=1, padx=5, pady=5)

    pin_label = tk.Label(form_frame, text="PIN", font=("Helvetica", 14))
    pin_label.grid(row=2, column=0, padx=5, pady=5)

    pin_entry = tk.Entry(form_frame, font=("Helvetica", 14),  width=20)
    pin_entry.grid(row=2, column=1, padx=5, pady=5)

    active_check = tk.Label(form_frame, text="Aktivan", font=("Helvetica", 14))
    active_check.grid(row=3, column=0,  padx=5, pady=5)
    
    active_var = tk.BooleanVar()
    active_checkbutton = tk.Checkbutton(form_frame, font=("Helvetica", 14), variable=active_var)
    active_checkbutton.grid(row=3, column=1, padx=5, pady=5, sticky="W")

    buttons_frame = tk.Frame(form_frame)
    buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)

    save_button = tk.Button(buttons_frame, text="Spremi", font=("Helvetica", 14), width=8, height=1, bg="#2a9d8f", fg="#fff", command=lambda: save_user_db(listbox, name_entry, surname_entry, pin_entry, active_var, messagebox))
    save_button.grid(row=0, column=0, padx=8)

    delete_button = tk.Button(buttons_frame, text="Obriši korisnika", font=("Helvetica", 14), width=16, height=1, bg="#e76f51", fg="#fff", command=lambda: delete_user_db(listbox))
    delete_button.grid(row=0, column=1, padx=8)

    cancel_button = tk.Button(buttons_frame, text="Odustani", font=("Helvetica", 14), width=8, height=1, bg="#f4a261", fg="#fff", command=lambda: clear_form(name_entry, surname_entry, pin_entry, active_checkbutton))
    cancel_button.grid(row=0, column=2, padx=8)


    
    
    listbox.bind('<<ListboxSelect>>', lambda event: on_select(event, listbox, name_entry, surname_entry, pin_entry, active_checkbutton))

root.mainloop()


