from connect import connect
import json

# ---------- SEARCH ----------
def search_contacts():
    pattern = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------- PAGINATION ----------
def paginate():
    limit = int(input("Limit: "))
    offset = 0

    conn = connect()
    cur = conn.cursor()

    while True:
        cur.execute("SELECT name, email FROM contacts LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        else:
            break

    cur.close()
    conn.close()


# ---------- UPSERT ----------
def upsert():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

    print("Done")


# ---------- DELETE ----------
def delete_contact():
    value = input("Name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted")


# ---------- ADD PHONE ----------
def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added")


# ---------- MOVE GROUP ----------
def move_to_group():
    name = input("Contact name: ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL move_to_group(%s, %s)", (name, group))

    conn.commit()
    cur.close()
    conn.close()

    print("Moved to group")


# ---------- FILTER ----------
def filter_group():
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name = %s
    """, (group,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------- SORT ----------
def sort_contacts():
    print("Sort by: name / birthday / email")
    field = input("Field: ")

    conn = connect()
    cur = conn.cursor()

    query = f"SELECT name, email, birthday FROM contacts ORDER BY {field}"
    cur.execute(query)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ---------- EXPORT ----------
def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w") as f:
        json.dump(data, f, default=str)

    cur.close()
    conn.close()

    print("Exported")


# ---------- IMPORT ----------
def import_json():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for row in data:
        name, email, birthday, group, phone, ptype = row

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. overwrite? (y/n): ")
            if choice == "n":
                continue
            cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, email, birthday))

        c_id = cur.fetchone()[0]

        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (c_id, phone, ptype))

    conn.commit()
    cur.close()
    conn.close()

    print("Imported")


# ---------- MENU ----------
def menu():
    while True:
        print("""
1 Search
2 Pagination
3 Upsert
4 Delete
5 Add phone
6 Move to group
7 Filter by group
8 Sort
9 Export JSON
10 Import JSON
0 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            paginate()
        elif choice == "3":
            upsert()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            add_phone()
        elif choice == "6":
            move_to_group()
        elif choice == "7":
            filter_group()
        elif choice == "8":
            sort_contacts()
        elif choice == "9":
            export_json()
        elif choice == "10":
            import_json()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()    