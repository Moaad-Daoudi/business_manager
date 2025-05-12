# model/user_database_manager.py
import sqlite3
import hashlib
import os

USER_DATABASE_NAME = "user_database.db" # Explicitly for users

class UserDatabaseManager: # Renamed class
    def __init__(self, db_name=USER_DATABASE_NAME):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, db_name)
        print(f"[UserDBManager __init__] Path: {self.db_path}")
        self.conn = None
        self.cursor = None
        self._connect()
        if self.conn and self.cursor:
            self._create_users_table()
        else:
            print("[UserDBManager __init__] Skipping users table creation due to connection failure.")

    def _connect(self):
        print(f"[UserDBManager _connect] Connecting to: {self.db_path}")
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # PRAGMA foreign_keys = ON; might not be needed if this DB doesn't have FKs TO other tables
            # but doesn't harm. If users table IS a target of FKs, then it's good.
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            print(f"[UserDBManager _connect] Successfully connected to: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[UserDBManager _connect] FATAL Error connecting: {e}")
            self.conn = self.cursor = None

    def _create_users_table(self):
        if not self.cursor:
            print("[UserDBManager _create_users_table] Cannot create: No cursor.")
            return
        print("[UserDBManager _create_users_table] Creating 'users' table...")
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
            print("[UserDBManager _create_users_table] 'users' table checked/created.")
        except sqlite3.Error as e:
            print(f"[UserDBManager _create_users_table] Error creating 'users' table: {e}")

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def add_user(self, name, email, password):
        print(f"[UserDBManager add_user] Attempting for: Name='{name}', Email='{email}'")
        if not self.cursor or not self.conn:
            print("[UserDBManager add_user] DB not connected.")
            return False, "Database connection error."
        if not all([name, email, password]):
            return False, "Name, email, and password cannot be empty."

        hashed_password = self._hash_password(password)
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email.lower(), hashed_password)
            )
            self.conn.commit()
            print(f"[UserDBManager add_user] User '{name}' added successfully.")
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            print(f"[UserDBManager add_user] IntegrityError: Email '{email}' likely exists.")
            return False, "Email already registered."
        except sqlite3.Error as e:
            print(f"[UserDBManager add_user] SQLite Error: {e}")
            return False, f"An error occurred: {e}"

    def get_user_by_email(self, email):
        print(f"[UserDBManager get_user_by_email] For: '{email}'")
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email.lower(),))
            user_row = self.cursor.fetchone()
            if user_row:
                return {"id": user_row[0], "name": user_row[1], "email": user_row[2], "password_hash": user_row[3]}
            return None
        except sqlite3.Error as e:
            print(f"[UserDBManager get_user_by_email] SQLite Error: {e}")
            return None

    def verify_password(self, stored_hash, provided_password):
        return stored_hash == self._hash_password(provided_password)

    def close_connection(self):
        if self.conn:
            print(f"[UserDBManager close_connection] Closing connection to {self.db_path}")
            self.conn.close()
            self.conn = self.cursor = None
        else:
            print("[UserDBManager close_connection] No active connection to close.")

if __name__ == '__main__':
    print("--- Running user_database_manager.py directly for testing ---")
    user_db_manager = UserDatabaseManager()
    # success, msg = user_db_manager.add_user("Test User From UserDB", "testuser@example.com", "password123")
    # print(f"Add user: {success} - {msg}")
    # found_user = user_db_manager.get_user_by_email("testuser@example.com")
    # print(f"Found user: {found_user}")
    user_db_manager.close_connection()
    print("--- End of user_database_manager.py direct test ---")