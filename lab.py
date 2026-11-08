"""Safe, isolated SQL-injection demonstration using an in-memory database."""
import sqlite3


def database():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (username TEXT, role TEXT)")
    db.executemany("INSERT INTO users VALUES (?, ?)",
                   [("alice", "analyst"), ("bob", "engineer"), ("carol", "auditor")])
    return db


def vulnerable_lookup(db, username):
    # Deliberately unsafe: use ONLY in this isolated teaching example.
    query = "SELECT username, role FROM users WHERE username = '" + username + "'"
    return db.execute(query).fetchall()


def safe_lookup(db, username):
    return db.execute("SELECT username, role FROM users WHERE username = ?", (username,)).fetchall()


def safe_role_lookup(db, role):
    """Second safe query demonstrating reusable parameterized search."""
    return db.execute("SELECT username FROM users WHERE role = ? ORDER BY username", (role,)).fetchall()


def main():
    payload = "' OR '1'='1"
    with database() as db:
        print("Normal lookup:", safe_lookup(db, "alice"))
        print("Injected unsafe lookup:", vulnerable_lookup(db, payload))
        print("Injected parameterized lookup:", safe_lookup(db, payload))
        print("Safe role lookup:", safe_role_lookup(db, "engineer"))


if __name__ == "__main__":
    main()
