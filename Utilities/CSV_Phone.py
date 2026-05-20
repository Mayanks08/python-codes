import csv
import os

FILENAME = "Test-data.csv"

if not os.path.exists(FILENAME):
    with open(FILENAME, 'w' , newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(["Name", "Phone", "Email"])

def add_contact():
    name = input("Name:").strip()
    phone = input("Phone:").strip()
    email = input("Email:").strip()

    with open(FILENAME, 'r' , encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["name"].lower() == name.lower():
                print("contact Already exist")
                return

    with open(FILENAME, 'a' ,encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(name, phone, email)
    print("Contact added successfully")

def view_contacts():
    with open(FILENAME, 'r' , newline="", encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

        if len(rows) < 1:
            print("No contacts yet")
            return

        print("\n Your Contacts: \n")

        for row in rows[1:]:
            print(f"{row[0]}|{row[1]}|{row[2]}")
        print()

def search_contact():
    term = input("Enter name or phone to search: ").strip().lower()
    found = False
    with open(FILENAME, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if term in row['name'].lower() or term in row['phone'].lower():
                print(f"Name: {row['name']}")
                print(f"Phone: {row['phone']}")
                print(f"Email: {row['email']}")
                found = True
    if not found:
        print("Contact not found.")

def delete_contact():
    name = input("Enter name to delete: ").strip().lower()
    with open(FILENAME, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        found = False
        for row in rows:
            if row['name'].lower() == name:
                rows.remove(row)
                found = True
                break
    if found:
        with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(rows)
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

def edit_contact():
    name = input("Enter name to edit: ").strip().lower()
    with open(FILENAME, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        found = False
        for row in rows:
            if row['name'].lower() == name:
                found = True
                break
    if not found:
        print("Contact not found.")
        return
    print("\nEditing Contact: " + name)
    print("Leave empty to keep current value.")
    new_name = input(f"Name ({row['name']}): ").strip()
    new_phone = input(f"Phone ({row['phone']}): ").strip()
    new_email = input(f"Email ({row['email']}): ").strip()
    if new_name:
        row['name'] = new_name
    if new_phone:
        row['phone'] = new_phone
    if new_email:
        row['email'] = new_email
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
        writer.writeheader()
        writer.writerows(rows)
    print("Contact updated successfully.")

def main():
    print("\nContact Manager")
    print("1. View Contacts")
    print("2. Add Contact")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Edit Contact")
    print("6.   Exit")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        view_contacts()
    elif choice == '2':
        add_contact()
    elif choice == '3':
        search_contact()
    elif choice == '4':
        exit()
    else:
        print("Invalid choice. Please try again.")

while True:
    main()
