import sqlite3
import hashlib
import os

DATABASE_NAME = "app_database.db"

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        """
        Initializes the DatabaseManager.
        Connects to the SQLite database and ensures the users table exists.
        """
        # Determine the absolute path for the database file in the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Goes up two levels
        self.db_path = os.path.join(project_root, db_name)
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_users_table()

    def _connect(self):
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            # Consider how to handle this more gracefully in a real app (e.g., exit, retry)

    def _create_users_table(self):
        """
        Creates the 'users' table if it doesn't already exist.
        The table will store user credentials.
        """
        if not self.cursor:
            print("Cannot create table: No database cursor.")
            return
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
            print("'users' table checked/created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating 'users' table: {e}")

    def _hash_password(self, password):
        """Hashes a password using SHA256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def add_user(self, name, email, password):
        """
        Adds a new user to the database.
        Passwords are hashed before storage.
        Returns True on success, False on failure (e.g., email already exists).
        """
        if not self.cursor:
            print("Cannot add user: No database cursor.")
            return False, "Database connection error."

        hashed_password = self._hash_password(password)
        try:
            self.cursor.execute("""
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
            """, (name, email.lower(), hashed_password)) # Store email in lowercase for consistency
            self.conn.commit()
            print(f"User '{name}' with email '{email}' added successfully.")
            return True, "User registered successfully!"
        except sqlite3.IntegrityError: # This usually means UNIQUE constraint failed (email exists)
            print(f"Error adding user: Email '{email}' already exists.")
            return False, "Email already registered."
        except sqlite3.Error as e:
            print(f"Database error adding user: {e}")
            return False, f"An error occurred: {e}"

    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.
        Returns a user dictionary or None if not found.
        """
        if not self.cursor:
            print("Cannot get user: No database cursor.")
            return None
        try:
            self.cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email.lower(),))
            user_row = self.cursor.fetchone()
            if user_row:
                return {
                    "id": user_row[0],
                    "name": user_row[1],
                    "email": user_row[2],
                    "password_hash": user_row[3]
                }
            return None
        except sqlite3.Error as e:
            print(f"Database error fetching user by email: {e}")
            return None

    def verify_password(self, stored_hash, provided_password):
        """Verifies a provided password against a stored hash."""
        return stored_hash == self._hash_password(provided_password)

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

# Example usage (for testing this module directly)
if __name__ == '__main__':
    db_manager = DatabaseManager()

    # Test adding a user
    # success, message = db_manager.add_user("Test User", "test@example.com", "password123")
    # print(f"Add user 1: {success}, {message}")

    # success, message = db_manager.add_user("Another User", "another@example.com", "securepass")
    # print(f"Add user 2: {success}, {message}")

    # Test adding a duplicate email
    # success, message = db_manager.add_user("Test User Again", "test@example.com", "newpassword")
    # print(f"Add duplicate user: {success}, {message}")

    # Test retrieving a user
    # user = db_manager.get_user_by_email("test@example.com")
    # if user:
    #     print(f"Found user: {user['name']}, {user['email']}")
    #     # Test password verification
    #     is_valid = db_manager.verify_password(user['password_hash'], "password123")
    #     print(f"Password 'password123' for test@example.com is valid: {is_valid}")
    #     is_valid = db_manager.verify_password(user['password_hash'], "wrongpassword")
    #     print(f"Password 'wrongpassword' for test@example.com is valid: {is_valid}")
    # else:
    #     print("User test@example.com not found.")

    # user_none = db_manager.get_user_by_email("nonexistent@example.com")
    # print(f"User nonexistent@example.com found: {user_none}")

    db_manager.close_connection()