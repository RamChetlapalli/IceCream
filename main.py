# -*- coding: utf-8 -*-
import sqlite3
import os

# DB Setup
db = sqlite3.connect("icecreamdb.sqlite")
cursor = db.cursor()

# Create Tables
cursor.execute('''CREATE TABLE IF NOT EXISTS flavors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    is_seasonal INTEGER DEFAULT 0
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS allergens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    flavor_name TEXT
)''')

db.commit()

# Globals
cart = []

# CLI Functions
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("="*30)
    print("      ICE CREAM PARLOR")
    print("="*30)

def add_flavor():
    name = raw_input("Enter flavor name: ")
    seasonal = raw_input("Is it seasonal? (y/n): ").lower()
    is_seasonal = 1 if seasonal == 'y' else 0
    try:
        cursor.execute("INSERT INTO flavors (name, is_seasonal) VALUES (?, ?)", (name, is_seasonal))
        db.commit()
        print("Flavor added!")
    except:
        print("Error adding flavor. It might already exist.")

def view_flavors():
    cursor.execute("SELECT id, name, is_seasonal FROM flavors")
    rows = cursor.fetchall()
    print("\nAll Flavors:")
    for f in rows:
        label = "[SEASONAL]" if f[2] else ""
        print("  %d. %s %s" % (f[0], f[1], label))

def search_flavor():
    query = raw_input("Search flavor name: ")
    cursor.execute("SELECT id, name FROM flavors WHERE name LIKE ?", ('%' + query + '%',))
    result = cursor.fetchall()
    if result:
        for r in result:
            print("  %d. %s" % (r[0], r[1]))
            add = raw_input("Add to cart? (y/n): ")
            if add.lower() == 'y':
                cart.append(r[1])
    else:
        print("No matching flavor found.")

def add_allergen():
    name = raw_input("Enter new allergen: ")
    try:
        cursor.execute("INSERT INTO allergens (name) VALUES (?)", (name,))
        db.commit()
        print("Allergen added.")
    except:
        print("Already exists or error!")

def view_allergens():
    cursor.execute("SELECT id, name FROM allergens")
    data = cursor.fetchall()
    print("\nAllergens:")
    for a in data:
        print("  %d. %s" % (a[0], a[1]))

def suggest_flavor():
    name = raw_input("Your Name: ")
    flavor = raw_input("Suggest a new flavor: ")
    cursor.execute("INSERT INTO suggestions (customer_name, flavor_name) VALUES (?, ?)", (name, flavor))
    db.commit()
    print("Thank you for your suggestion!")

def view_cart():
    print("\nYour Cart:")
    if not cart:
        print("  [Empty]")
    else:
        for i, item in enumerate(cart):
            print("  %d. %s" % (i+1, item))

def main_menu():
    while True:
        print_header()
        print("1. Add New Flavor")
        print("2. View All Flavors")
        print("3. Search & Add to Cart")
        print("4. Add Allergen")
        print("5. View Allergens")
        print("6. Suggest a Flavor")
        print("7. View Cart")
        print("8. Exit")
        try:
            choice = int(raw_input("Select option: "))
        except:
            print("Invalid input")
            continue

        clear()
        if choice == 1:
            add_flavor()
        elif choice == 2:
            view_flavors()
        elif choice == 3:
            search_flavor()
        elif choice == 4:
            add_allergen()
        elif choice == 5:
            view_allergens()
        elif choice == 6:
            suggest_flavor()
        elif choice == 7:
            view_cart()
        elif choice == 8:
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

        raw_input("\nPress Enter to continue...")
        clear()

# Entry point
if __name__ == '__main__':
    clear()
    main_menu()
