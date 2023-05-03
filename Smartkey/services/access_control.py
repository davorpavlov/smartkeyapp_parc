import sqlite3
from tkinter import messagebox
import tkinter as tk

def get_users():
    conn = sqlite3.connect('smartkey.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()

    users = []
    for row in rows:
        user = {
            'id': row[0],
            'name': row[1],
            'surname': row[2],
            'pin': row[3],
            'active': row[4]
        }
        users.append(user)

    return users

def check_pin(pin1_value, pin2_value, pin3_value, pin4_value, generated_message_text, panel_3):
    users = get_users()
    user_pin = str(f"{pin1_value.get()}{pin2_value.get()}{pin3_value.get()}{pin4_value.get()}")
    pin_found = False
    for user in users:
        if str(user['pin']) == "1234" and user_pin == "1234":
            generated_message_text.insert(tk.END, "Unijeli ste Admin pin, želite li otvoriti panel za upravljanje dodijeljenim ključevima? ")
            response = messagebox.askyesno("Administracija za dozvolu ulaza", "Odaberite DA za nastavak, NE samo za otkljucavanje vrata")
            if response == 1:
                panel_3()
            else:
                generated_message_text.insert(tk.END, f"Dobrodošao {user['name']} {user['surname']}")
            pin_found = True
            break
        elif str(user['pin']) == user_pin and user['active']:
            generated_message_text.insert(tk.END, f"Pin je točan, dobrodošao {user['name']} {user['surname']}")
            pin_found = True
            break
    if not pin_found:
        messagebox.showerror("Upozorenje", "Krivi PIN ili je korisnik neaktivan")

def clear_pin(pin1_value, pin2_value, pin3_value, pin4_value):
    pin1_value.set("")
    pin2_value.set("")
    pin3_value.set("")
    pin4_value.set("")
    
def update_pin(num, pin1_value, pin2_value, pin3_value, pin4_value):
    if not pin1_value.get():
        pin1_value.set(num)
    elif not pin2_value.get():
        pin2_value.set(num)
    elif not pin3_value.get():
        pin3_value.set(num)
    elif not pin4_value.get():
        pin4_value.set(num)

def ring_bell():
    popup = tk.Toplevel()
    popup.title("Zvono aktivirano")
    message = tk.Label(popup, text="Zvono je aktivirano.\nNetko će uskoro doći i otvoriti vrata.", font=("Helvetica", 14))
    message.pack(pady=10)
    message2 = tk.Label(popup, font=("Helvetica", 14))
    message2.pack(pady=10)

    
    count = 5
    def update_countdown():
        nonlocal count
        message2.config(text=f"Poruka se zatvara za {count} sekundi")
        count -= 1
        if count >= 0:
            popup.after(1000, update_countdown)
        else:
            popup.destroy()
    update_countdown()