# model/product_database_manager.py
import sqlite3
import os
from datetime import datetime

PRODUCT_DATABASE_NAME = "database_product.db"

class ProductDatabaseManager:
    def __init__(self, db_name=PRODUCT_DATABASE_NAME):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, db_name)
        print(f"[ProductDBManager __init__] Path: {self.db_path}")
        self.conn = None
        self.cursor = None
        self._connect()
        if self.conn and self.cursor:
            self._create_user_products_table()

    def _connect(self):
        print(f"[ProductDBManager _connect] Connecting to: {self.db_path}")
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"[ProductDBManager _connect] Successfully connected to: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[ProductDBManager _connect] FATAL Error connecting: {e}")
            self.conn = self.cursor = None

    def _create_user_products_table(self):
        if not self.cursor: return
        print("[ProductDBManager] Creating 'user_products' table...")
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_username TEXT NOT NULL,
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
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_user_product_updated_at
                AFTER UPDATE ON user_products
                FOR EACH ROW
                BEGIN
                    UPDATE user_products SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
                END;
            """)
            self.conn.commit()
            print("[ProductDBManager] 'user_products' table checked/created.")
        except sqlite3.Error as e:
            print(f"[ProductDBManager] Error creating 'user_products' table or trigger: {e}")

    def add_product(self, owner_username, product_data):
        if not self.cursor or not self.conn: return None, "Product DB not connected."
        if not owner_username: return None, "Owner username is required."

        required = ['product_name', 'selling_price']
        for field in required:
            if field not in product_data or not product_data[field]:
                return None, f"Missing required field: {field}"

        # Prepare data, ensuring all columns are accounted for
        columns = ['owner_username', 'product_name', 'sku', 'description', 'category', 'brand',
                   'purchase_price', 'selling_price', 'stock_quantity', 'low_stock_threshold',
                   'image_url', 'notes', 'created_at', 'updated_at']
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values_tuple = (
            owner_username,
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
            product_data.get('notes'),
            current_time,
            current_time
        )

        try:
            query = f"INSERT INTO user_products ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            self.cursor.execute(query, values_tuple)
            self.conn.commit()
            product_id = self.cursor.lastrowid
            print(f"[ProductDBManager] Product '{product_data['product_name']}' added for '{owner_username}', ID: {product_id}")
            return product_id, "Product added successfully."
        except sqlite3.IntegrityError as e:
            return None, f"Error (SKU '{product_data.get('sku')}' might exist): {e}"
        except sqlite3.Error as e:
            return None, f"Database error: {e}"

    def get_products_by_username(self, owner_username, search_term=None, category_filter=None, sort_by="product_name", sort_order="ASC"):
        if not self.cursor: return []
        if not owner_username: return []

        query = "SELECT * FROM user_products WHERE owner_username = ?"
        params = [owner_username]

        if search_term:
            query += " AND (product_name LIKE ? OR sku LIKE ? OR description LIKE ? OR brand LIKE ?)"
            like_term = f"%{search_term}%"
            params.extend([like_term] * 4)
        if category_filter:
            query += " AND category = ?"
            params.append(category_filter)
        
        allowed_sort = ["id", "product_name", "category", "selling_price", "stock_quantity", "created_at", "updated_at"]
        if sort_by not in allowed_sort: sort_by = "product_name"
        sort_order = "DESC" if sort_order.upper() == "DESC" else "ASC"
        query += f" ORDER BY {sort_by} {sort_order}"

        try:
            self.cursor.execute(query, tuple(params))
            rows = self.cursor.fetchall()
            products = []
            columns = [desc[0] for desc in self.cursor.description]
            for row in rows:
                products.append(dict(zip(columns, row)))
            return products
        except sqlite3.Error as e:
            print(f"[ProductDBManager] Error getting products for '{owner_username}': {e}")
            return []

    def get_product_by_id_and_username(self, product_id, owner_username):
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT * FROM user_products WHERE id = ? AND owner_username = ?", (product_id, owner_username))
            row = self.cursor.fetchone()
            if row:
                columns = [desc[0] for desc in self.cursor.description]
                return dict(zip(columns, row))
            return None
        except sqlite3.Error as e:
            print(f"[ProductDBManager] Error getting product ID {product_id} for '{owner_username}': {e}")
            return None
            
    def update_product(self, product_id, owner_username, product_data):
        if not self.cursor or not self.conn: return False, "Product DB not connected."
        if not product_data: return False, "No data for update."

        product_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_clauses = []
        values = []

        allowed_to_update = ['product_name', 'sku', 'description', 'category', 'brand',
                             'purchase_price', 'selling_price', 'stock_quantity', 
                             'low_stock_threshold', 'image_url', 'notes', 'updated_at']
                             # 'owner_username' should not be updated this way.

        for key, value in product_data.items():
            if key in allowed_to_update:
                set_clauses.append(f"{key} = ?")
                if key in ['purchase_price', 'selling_price'] and value is not None: values.append(float(value))
                elif key in ['stock_quantity', 'low_stock_threshold'] and value is not None: values.append(int(value))
                else: values.append(value)
        
        if not set_clauses: return False, "No valid fields to update."
        values.extend([product_id, owner_username])

        try:
            query = f"UPDATE user_products SET {', '.join(set_clauses)} WHERE id = ? AND owner_username = ?"
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product updated successfully." if self.cursor.rowcount > 0 else "Product not found or no changes."
        except sqlite3.IntegrityError as e: # SKU unique
            return False, f"Error updating (SKU might exist): {e}"
        except sqlite3.Error as e:
            return False, f"Database error updating product: {e}"

    def delete_product(self, product_id, owner_username):
        if not self.cursor or not self.conn: return False, "Product DB not connected."
        try:
            self.cursor.execute("DELETE FROM user_products WHERE id = ? AND owner_username = ?", (product_id, owner_username))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product deleted." if self.cursor.rowcount > 0 else "Product not found."
        except sqlite3.Error as e:
            return False, f"Database error deleting: {e}"

    def close_connection(self):
        if self.conn:
            print(f"[ProductDBManager] Closing connection to {self.db_path}")
            self.conn.close()
            self.conn = self.cursor = None