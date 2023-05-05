import sqlite3
from tkinter import messagebox
import tkinter as tk

def on_select(event, listbox, name_entry, surname_entry, pin_entry, active_checkbutton):
        selected_rows = listbox.curselection()
        if not selected_rows:
            return
        selected_row = selected_rows[0]
        value = listbox.get(selected_row)
        
        user_id = value.split("ID: ")[1]
        name = value.split()[0]
        surname = value.split()[1]
        pin = value.split()[4][:-1]
        active = value.split()[6]
        
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)

        surname_entry.delete(0, tk.END)
        surname_entry.insert(0, surname)

        pin_entry.delete(0, tk.END)
        pin_entry.insert(0, pin)

        if active == "True":
            active_checkbutton.select()
        else:
            active_checkbutton.deselect()

def save_user_db(listbox, name_entry, surname_entry, pin_entry, active_var, messagebox):
    name = name_entry.get()
    surname = surname_entry.get()
    pin = pin_entry.get()
    active = active_var.get()

    if not pin.isdigit():
        messagebox.showerror("Greška", "PIN mora biti broj")
        return

    if not name or not surname or not pin:
        messagebox.showwarning("Upozorenje", "Polja ime, prezime i PIN su obavezna")
        return

    active_value = int(active)

    with sqlite3.connect('smartkey.db') as conn:
        c = conn.cursor()

        if listbox.curselection():
            selected_row = listbox.curselection()[0]
            value = listbox.get(selected_row)
            user_id = value.split("ID: ")[1]

            c.execute("SELECT active FROM users WHERE id=?", (user_id,))
            current_active = c.fetchone()[0]

            if active_value != current_active:
                c.execute("UPDATE users SET active=? WHERE id=?", (active_value, user_id))
                conn.commit()
                messagebox.showinfo("Uspjeh", "Status korisnika je ažuriran u bazi podataka.")
            else:
                messagebox.showinfo("Info", "Status korisnika nije promijenjen.")
        else:
            c.execute("SELECT * FROM users WHERE name=? AND surname=? AND pin=?", (name, surname, pin))
            existing_user = c.fetchone()

            if existing_user:
                if existing_user[3] != active_value:
                    c.execute("UPDATE users SET active=? WHERE id=?", (active_value, existing_user[0]))
                    conn.commit()
                    messagebox.showinfo("Uspjeh", "Status korisnika je ažuriran u bazi podataka.")
                else:
                    messagebox.showinfo("Info", "Korisnik već postoji u bazi podataka.")
            else:
                c.execute("INSERT INTO users (name, surname, pin, active) VALUES (?, ?, ?, ?)", (name, surname, pin, active_value))
                conn.commit()
                messagebox.showinfo("Uspjeh", "Korisnik je dodan u bazu podataka.")
    listbox.delete(0, tk.END)
    get_users_from_db(listbox)


def delete_user_db(listbox):
        selection = listbox.curselection()
        if not selection:
            return
        index = selection[0]
        
        data = listbox.get(index)
        
        parts = data.split(" - ")
        name, surname = parts[0].split()
        active = parts[1].split(": ")[1] == "True"
        
        if not messagebox.askyesno("Brisanje korisnika", "Jeste li sigurni da želite obrisati korisnika iz baze podataka?"):
            return
        
        conn = sqlite3.connect('smartkey.db')
        c = conn.cursor()
        
        c.execute("DELETE FROM users WHERE name=? AND surname=?", (name, surname))
        
        conn.commit()
        
        conn.close()
        
        listbox.delete(index)
        
        messagebox.showinfo("Uspjeh", "Korisnik je obrisan iz baze podataka.")
        listbox.delete(0, tk.END)
        get_users_from_db(listbox)

def get_users_from_db(listbox):
    conn = sqlite3.connect('smartkey.db')
    c = conn.cursor()
    c.execute("SELECT id, name, surname, pin, active FROM users")
    result = c.fetchall()

    for row in result:
        user_id = row[0]
        name = row[1]
        surname = row[2]
        pin = row[3]
        active = row[4]
        listbox.insert(tk.END, f"{name} {surname} - PIN: {pin}, Aktivan: {active}, ID: {user_id}")
    conn.close()

def clear_form(name_entry, surname_entry, pin_entry, active_checkbutton):
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    pin_entry.delete(0, tk.END)
    active_checkbutton.deselect()


# Kreiranje tablice u bazi
def create_database():
    conn = sqlite3.connect('smartkey.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, pin TEXT, active BOOLEAN)''')

    users = [
        {"id": 1, "name": "Ivan", "surname": "Horvat", "pin": "1234", "active": True},
        {"id": 2, "name": "Ana", "surname": "Kovačić", "pin": "5678", "active": False},
        {"id": 3, "name": "Marko", "surname": "Babić", "pin": "9876", "active": True},
        {"id": 4, "name": "Petra", "surname": "Knežević", "pin": "2468", "active": True},
        {"id": 5, "name": "Mario", "surname": "Novak", "pin": "1357", "active": False},
        {"id": 6, "name": "Lucija", "surname": "Horvat", "pin": "8642", "active": True}
    ]

    for user in users:
        c.execute("INSERT INTO users (id, name, surname, pin, active) VALUES (?, ?, ?, ?, ?)", (user['id'], user['name'], user['surname'], user['pin'], user['active']))

    conn.commit()
    conn.close()

