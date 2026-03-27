from connect import connect
import csv


def insert_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Added")


def get_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def update_contact():
    name = input("Name: ")
    phone = input("New phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated")


def delete_contact():
    name = input("Name: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")


def find_by_prefix():
    prefix = input("Prefix: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (prefix + "%",)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row[0], row[1])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported")


def menu():
    while True:
        print("""
1 Add
2 Show
3 Update
4 Delete
5 Find by prefix
6 Import CSV
0 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            insert_contact()
        elif choice == "2":
            get_contacts()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            find_by_prefix()
        elif choice == "6":
            import_csv()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()