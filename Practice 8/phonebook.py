from connect import connect


def search_contacts():
    pattern = input("Search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def get_paginated():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


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


def delete_contact():
    value = input("Name or phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted")


def menu():
    while True:
        print("""
1 Search
2 Pagination
3 Upsert (insert/update)
4 Delete
0 Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            get_paginated()
        elif choice == "3":
            upsert()
        elif choice == "4":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()