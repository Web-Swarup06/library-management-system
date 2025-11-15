import mysql.connector

# ---------------- DB CONNECTION ----------------
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="library_db"
    )

# ---------------- ADD BOOK ----------------
def add_book():
    title = input("Title: ")
    author = input("Author: ")
    isbn = input("ISBN: ")
    copies = int(input("Total Copies: "))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO books (title, author, isbn, copies_total, copies_available)
    VALUES (%s, %s, %s, %s, %s)
    """, (title, author, isbn, copies, copies))

    conn.commit()
    print("Book added.")
    conn.close()

# ---------------- SEARCH BOOK ----------------
def search_book():
    key = input("Enter title/author keyword: ")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, title, author, copies_available
    FROM books
    WHERE title LIKE %s OR author LIKE %s
    """, ("%" + key + "%", "%" + key + "%"))

    rows = cur.fetchall()
    if not rows:
        print("No results.")
    else:
        for r in rows:
            print(r)

    conn.close()

# ---------------- ADD MEMBER ----------------
def add_member():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO members (name, phone, email)
    VALUES (%s, %s, %s)
    """, (name, phone, email))

    conn.commit()
    print("Member added.")
    conn.close()

# ---------------- ISSUE BOOK ----------------
def issue_book():
    book_id = int(input("Book ID: "))
    member_id = int(input("Member ID: "))

    conn = get_conn()
    cur = conn.cursor()

    # Check available
    cur.execute("SELECT copies_available FROM books WHERE id=%s", (book_id,))
    data = cur.fetchone()

    if not data:
        print("Book not found.")
        conn.close()
        return

    if data[0] <= 0:
        print("No copies available.")
        conn.close()
        return

    # Issue
    cur.execute("UPDATE books SET copies_available = copies_available - 1 WHERE id=%s", (book_id,))
    cur.execute("""
    INSERT INTO issued_books (book_id, member_id, issue_date)
    VALUES (%s, %s, CURDATE())
    """, (book_id, member_id))

    conn.commit()
    print("Book issued.")
    conn.close()

# ---------------- RETURN BOOK ----------------
def return_book():
    issue_id = int(input("Issue ID: "))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT book_id FROM issued_books
    WHERE id=%s AND return_date IS NULL
    """, (issue_id,))

    data = cur.fetchone()

    if not data:
        print("Invalid issue ID or already returned.")
        conn.close()
        return

    book_id = data[0]

    cur.execute("UPDATE issued_books SET return_date = CURDATE() WHERE id=%s", (issue_id,))
    cur.execute("UPDATE books SET copies_available = copies_available + 1 WHERE id=%s", (book_id,))

    conn.commit()
    print("Book returned.")
    conn.close()

# ---------------- MENU ----------------
def menu():
    while True:
        print("\n--- Library System ---")
        print("1. Add Book")
        print("2. Search Books")
        print("3. Add Member")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Exit")

        ch = input("Choice: ")

        if ch == "1": add_book()
        elif ch == "2": search_book()
        elif ch == "3": add_member()
        elif ch == "4": issue_book()
        elif ch == "5": return_book()
        elif ch == "6": break
        else: print("Invalid option.")

if __name__ == "__main__":
    menu()
