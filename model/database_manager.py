# model/database_manager.py
import sqlite3
import hashlib
import os
import sys
from datetime import datetime

DATABASE_NAME = "app_database.db"

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, db_name)
        
        print(f"--- [DatabaseManager] Using database in project folder at: {self.db_path} ---")
        
        self.conn = None
        self.cursor = None
        
        try:
            self._connect()
            self._create_users_table()
            self._create_user_products_table()
            # --- NEW: Call the method to create sales tables on startup ---
            self._create_sales_tables()
        except ConnectionError as e:
            raise ConnectionError(e)

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            print("[DatabaseManager] Database connection successful.")
        except sqlite3.Error as e:
            print(f"[DatabaseManager] FATAL: Failed to connect to database at '{self.db_path}'. Error: {e}")
            raise ConnectionError(f"Failed to connect to database. Please check file permissions for the path:\n{self.db_path}")

    # --- NEW: Method to create the two new tables for sales ---
    def _create_sales_tables(self):
        if not self.cursor: return
        try:
            # Table for the overall sale event
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount REAL NOT NULL,
                    notes TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            # Junction table for items within a sale
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity_sold INTEGER NOT NULL,
                    price_at_sale REAL NOT NULL, -- Store price in case product price changes later
                    FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                    FOREIGN KEY(product_id) REFERENCES user_products(id) ON DELETE SET NULL
                )
            """)
            self.conn.commit()
            print("[DatabaseManager] Sales tables verified/created successfully.")
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error creating sales tables: {e}")

    # --- THE REST OF THE FILE REMAINS UNCHANGED ---
    # (All methods like _create_users_table, add_user, add_product, etc., stay the same)

    def _create_users_table(self):
        if not self.cursor: return
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
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error creating 'users' table: {e}")

    def _hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def add_user(self, name, email, password):
        if not all([name, email, password]): return False, "Name, email, and password cannot be empty."
        hashed_password = self._hash_password(password)
        try:
            self.cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                                (name, email.lower(), hashed_password))
            self.conn.commit()
            return True, "User registered successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already registered."
        except sqlite3.Error as e:
            return False, f"An error occurred: {e}"

    def get_user_by_email(self, email):
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email.lower(),))
            user_row = self.cursor.fetchone()
            if user_row:
                return {"id": user_row[0], "name": user_row[1], "email": user_row[2], "password_hash": user_row[3]}
            return None
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting user by email: {e}")
            return None

    def verify_password(self, stored_hash, provided_password):
        return stored_hash == self._hash_password(provided_password)

    def _create_user_products_table(self):
        if not self.cursor: return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_name TEXT NOT NULL,
                    sku TEXT UNIQUE,
                    description TEXT,
                    category TEXT,
                    brand TEXT,
                    purchase_price REAL DEFAULT 0.0,
                    selling_price REAL NOT NULL,
                    stock_quantity INTEGER DEFAULT 0,
                    low_stock_threshold INTEGER DEFAULT 5,
                    image_url TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error creating 'user_products' table: {e}")

    def add_product(self, user_id, product_data):
        if not self.cursor or not self.conn: return None, "Database not connected."
        if not user_id: return None, "User ID is required."
        
        columns = ['user_id', 'product_name', 'sku', 'description', 'category', 'brand',
                   'purchase_price', 'selling_price', 'stock_quantity', 'low_stock_threshold',
                   'image_url', 'notes']
        
        values_tuple = (
            user_id,
            product_data.get('product_name'),
            product_data.get('sku'),
            product_data.get('description'),
            product_data.get('category'),
            product_data.get('brand'),
            float(product_data.get('purchase_price', 0.0) or 0.0),
            float(product_data.get('selling_price')),
            int(product_data.get('stock_quantity', 0) or 0),
            int(product_data.get('low_stock_threshold', 5) or 5),
            product_data.get('image_url'),
            product_data.get('notes')
        )
        
        try:
            query = f"INSERT INTO user_products ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            self.cursor.execute(query, values_tuple)
            self.conn.commit()
            product_id = self.cursor.lastrowid
            return product_id, "Product added successfully."
        except sqlite3.IntegrityError:
            return None, f"Error: SKU '{product_data.get('sku')}' might already exist."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"

    def get_products_by_user_id(self, user_id, search_term=None, sort_by="product_name", sort_order="ASC", **kwargs):
        if not self.cursor or not user_id: return []
        query = "SELECT * FROM user_products WHERE user_id = ?"
        params = [user_id]
        if search_term:
            query += " AND (product_name LIKE ? OR sku LIKE ? OR description LIKE ? OR brand LIKE ?)"
            like_term = f"%{search_term}%"
            params.extend([like_term] * 4)
        allowed_sort = ["product_name", "selling_price", "stock_quantity", "created_at"]
        if sort_by not in allowed_sort: sort_by = "product_name"
        sort_order = "DESC" if sort_order.upper() == "DESC" else "ASC"
        query += f" ORDER BY {sort_by} {sort_order}"
        try:
            self.cursor.execute(query, tuple(params))
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting products for user ID {user_id}: {e}")
            return []

    def get_product_by_id_and_user_id(self, product_id, user_id):
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT * FROM user_products WHERE id = ? AND user_id = ?", (product_id, user_id))
            row = self.cursor.fetchone()
            if row:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, row))
            return None
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting product ID {product_id} for user ID {user_id}: {e}")
            return None

    def update_product(self, product_id, user_id, product_data):
        if not self.cursor or not self.conn: return False, "Database not connected."
        product_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_clauses, values = [], []
        allowed = ['product_name', 'sku', 'description', 'category', 'brand', 'purchase_price', 'selling_price', 'stock_quantity', 'low_stock_threshold', 'image_url', 'notes', 'updated_at']
        for key, value in product_data.items():
            if key in allowed:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        if not set_clauses: return False, "No valid fields to update."
        values.extend([product_id, user_id])
        try:
            query = f"UPDATE user_products SET {', '.join(set_clauses)} WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product updated successfully." if self.cursor.rowcount > 0 else "Product not found or no changes."
        except sqlite3.IntegrityError:
            return False, f"Error updating: SKU might already exist."
        except sqlite3.Error as e:
            return False, f"Database error updating product: {e}"

    def delete_product(self, product_id, user_id):
        if not self.cursor or not self.conn: return False, "Database not connected."
        try:
            self.cursor.execute("DELETE FROM user_products WHERE id = ? AND user_id = ?", (product_id, user_id))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product deleted." if self.cursor.rowcount > 0 else "Product not found."
        except sqlite3.Error as e:
            return False, f"Database error deleting: {e}"
        
        
    def get_sales_records(self, user_id, start_date=None, end_date=None, product_id=None):
        """
        Fetches sales records with product details, filterable by date and product.
        """
        if not self.cursor or not user_id:
            return []
        
        query = """
            SELECT
                s.sale_date,
                p.product_name,
                si.quantity_sold,
                si.price_at_sale,
                (si.quantity_sold * si.price_at_sale) as total_revenue
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            JOIN user_products p ON si.product_id = p.id
            WHERE s.user_id = ?
        """
        params = [user_id]

        if product_id:
            query += " AND si.product_id = ?"
            params.append(product_id)
        
        if start_date:
            query += " AND s.sale_date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND s.sale_date <= ?"
            params.append(end_date)
            
        query += " ORDER BY s.sale_date DESC"
        
        try:
            self.cursor.execute(query, tuple(params))
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting sales records: {e}")
            return []

    def close_connection(self):
        if self.conn:
            print(f"[DatabaseManager] Closing connection to {self.db_path}")
            self.conn.close()
            self.conn = self.cursor = None