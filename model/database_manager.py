import sqlite3
import hashlib
import os
import sys
from datetime import datetime, timedelta

DATABASE_NAME = "app_database.db"

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(project_root, db_name)
        
        print(f"--- [DatabaseManager] Using database at: {self.db_path} ---")
        
        self.conn = None
        self.cursor = None
        
        try:
            self._connect()
            self._create_users_table()
            self._create_user_products_table()
            self._create_sales_tables()
            self._create_goals_table()
            self._create_activity_log_table()
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

    def get_user_by_id(self, user_id):
        if not self.cursor: return None
        try:
            self.cursor.execute("SELECT id, name, email, password_hash FROM users WHERE id = ?", (user_id,))
            user_row = self.cursor.fetchone()
            if user_row:
                return {"id": user_row[0], "name": user_row[1], "email": user_row[2], "password_hash": user_row[3]}
            return None
        except sqlite3.Error as e:
            print(f"[DatabaseManager] Error getting user by ID: {e}")
            return None

    def update_user(self, user_id, data_to_update):
        if not self.cursor or not user_id: return False, "Database not connected."
        set_clauses = []
        values = []
        if 'name' in data_to_update:
            set_clauses.append("name = ?")
            values.append(data_to_update['name'])
        if 'email' in data_to_update:
            set_clauses.append("email = ?")
            values.append(data_to_update['email'].lower())
        if 'password' in data_to_update:
            set_clauses.append("password_hash = ?")
            values.append(self._hash_password(data_to_update['password']))
        if not set_clauses: return False, "No valid fields provided for update."
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = ?"
        try:
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return True, "Profile updated successfully."
        except sqlite3.IntegrityError:
            return False, "This email address is already in use by another account."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def verify_password(self, stored_hash, provided_password):
        return stored_hash == self._hash_password(provided_password)

    def _create_user_products_table(self):
        if not self.cursor: return
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                sku TEXT,
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
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(user_id, sku)
            )
        """)
        self.conn.commit()

    def add_product(self, user_id, product_data):
        columns = ['user_id', 'product_name', 'sku', 'description', 'category', 'brand',
                   'purchase_price', 'selling_price', 'stock_quantity', 'low_stock_threshold',
                   'image_url', 'notes']
        values_tuple = (user_id, product_data.get('product_name'), product_data.get('sku'),
                        product_data.get('description'), product_data.get('category'),
                        product_data.get('brand'), float(product_data.get('purchase_price', 0.0) or 0.0),
                        float(product_data.get('selling_price')), int(product_data.get('stock_quantity', 0) or 0),
                        int(product_data.get('low_stock_threshold', 5) or 5), product_data.get('image_url'),
                        product_data.get('notes'))
        try:
            query = f"INSERT INTO user_products ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            self.cursor.execute(query, values_tuple)
            self.conn.commit()
            return self.cursor.lastrowid, "Product added successfully."
        except sqlite3.IntegrityError:
            return None, f"Error: SKU '{product_data.get('sku')}' might already exist for this user."
        except sqlite3.Error as e:
            return None, f"Database error: {e}"

    def get_products_by_user_id(self, user_id, search_term=None, sort_by="product_name", sort_order="ASC"):
        if not self.cursor or not user_id: return []
        query = "SELECT * FROM user_products WHERE user_id = ?"
        params = [user_id]
        if search_term:
            query += " AND (product_name LIKE ? OR sku LIKE ? OR description LIKE ? OR brand LIKE ?)"
            like_term = f"%{search_term}%"; params.extend([like_term] * 4)
        if sort_by not in ["product_name", "selling_price", "stock_quantity", "created_at"]: sort_by = "product_name"
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
            if row: columns = [desc[0] for desc in self.cursor.description]; return dict(zip(columns, row))
            return None
        except sqlite3.Error as e:
            print(f"[DB] Error getting product ID {product_id} for user ID {user_id}: {e}")
            return None

    def update_product(self, product_id, user_id, product_data):
        if not self.cursor: return False, "DB not connected."
        product_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        set_clauses, values = [], []
        allowed = ['product_name', 'sku', 'description', 'category', 'brand', 'purchase_price', 'selling_price', 'stock_quantity', 'low_stock_threshold', 'image_url', 'notes', 'updated_at']
        for key, value in product_data.items():
            if key in allowed: set_clauses.append(f"{key} = ?"); values.append(value)
        if not set_clauses: return False, "No valid fields to update."
        values.extend([product_id, user_id])
        try:
            query = f"UPDATE user_products SET {', '.join(set_clauses)} WHERE id = ? AND user_id = ?"
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product updated successfully."
        except sqlite3.IntegrityError: return False, f"Error updating: SKU might already exist."
        except sqlite3.Error as e: return False, f"Database error updating product: {e}"

    def delete_product(self, product_id, user_id):
        if not self.cursor: return False, "DB not connected."
        try:
            self.cursor.execute("DELETE FROM user_products WHERE id = ? AND user_id = ?", (product_id, user_id))
            self.conn.commit()
            return self.cursor.rowcount > 0, "Product deleted."
        except sqlite3.Error as e: return False, f"Database error deleting: {e}"

    def _create_sales_tables(self):
        if not self.cursor: return
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, total_amount REAL NOT NULL, notes TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                sale_id INTEGER NOT NULL, 
                product_id INTEGER NOT NULL,
                quantity_sold INTEGER NOT NULL, 
                price_at_sale REAL NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES user_products(id) ON DELETE CASCADE
            )
            """)
        self.conn.commit()
        

    def record_sale_transaction(self, user_id, items, total_amount, notes=''):
        """
        Records a sale and updates stock levels in a single, safe transaction.
        'items' should be a list of dicts: [{'id': product_id, 'quantity': qty, 'price': price}, ...]
        """
        if not self.conn or not self.cursor:
            return False, "Database not connected."
        
        try:
            self.cursor.execute("BEGIN TRANSACTION")

            self.cursor.execute(
                "INSERT INTO sales (user_id, total_amount, notes) VALUES (?, ?, ?)",
                (user_id, total_amount, notes)
            )
            sale_id = self.cursor.lastrowid

            for item in items:
                product_id = item['id']
                quantity_sold = item['quantity']
                
                self.cursor.execute(
                    "INSERT INTO sale_items (sale_id, product_id, quantity_sold, price_at_sale) VALUES (?, ?, ?, ?)",
                    (sale_id, product_id, quantity_sold, item['price'])
                )
                
                self.cursor.execute(
                    "UPDATE user_products SET stock_quantity = stock_quantity - ? WHERE id = ? AND user_id = ?",
                    (quantity_sold, product_id, user_id)
                )
            
            self.add_activity_log(user_id, "SALE", f"New sale recorded for ${total_amount:,.2f} with {len(items)} item(s).")
            self.conn.commit()
            return True, "Sale recorded successfully."

        except sqlite3.Error as e:
            self.conn.rollback()
            return False, f"Transaction failed: {e}"
    

    def get_sales_records(self, user_id, start_date=None, end_date=None, product_id=None):
        if not self.cursor: return []
        query = """SELECT s.sale_date, p.product_name, p.sku, p.category, si.quantity_sold, 
                   si.price_at_sale, (si.quantity_sold * si.price_at_sale) as total_revenue
                   FROM sales s JOIN sale_items si ON s.id = si.sale_id JOIN user_products p ON si.product_id = p.id
                   WHERE s.user_id = ?"""
        params = [user_id]
        if product_id: query += " AND si.product_id = ?"; params.append(product_id)
        if start_date: query += " AND s.sale_date >= ?"; params.append(start_date)
        if end_date: query += " AND s.sale_date <= ?"; params.append(end_date)
        query += " ORDER BY s.sale_date DESC"
        try:
            self.cursor.execute(query, tuple(params))
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"[DB] Error getting sales records: {e}"); return []

    def _create_goals_table(self):
        if not self.cursor: return
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_name TEXT NOT NULL,
                product_id INTEGER, target_revenue REAL, 
                target_quantity INTEGER,
                start_date TIMESTAMP NOT NULL, 
                deadline TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES user_products(id) ON DELETE CASCADE
            )
        """)
        self.conn.commit()

    def add_goal(self, user_id, goal_data):
        try:
            query = """INSERT INTO goals (user_id, goal_name, product_id, target_revenue, 
                       target_quantity, start_date, deadline) VALUES (?, ?, ?, ?, ?, ?, ?)"""
            values = (user_id, goal_data['goal_name'], goal_data.get('product_id'), goal_data.get('target_revenue'),
                      goal_data.get('target_quantity'), goal_data['start_date'], goal_data['deadline'])
            self.cursor.execute(query, values); self.conn.commit(); return True, "Goal created."
        except sqlite3.Error as e: return False, f"DB error: {e}"

    def get_user_goals(self, user_id):
        if not self.cursor: return []
        try:
            self.cursor.execute("SELECT * FROM goals WHERE user_id = ? ORDER BY deadline ASC", (user_id,))
            rows = self.cursor.fetchall(); columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e: print(f"Error getting goals: {e}"); return []

    def get_sales_progress_for_goal(self, user_id, start_date, end_date, product_id=None):
        if not self.cursor: return {'total_revenue': 0, 'total_quantity': 0}
        query = "SELECT SUM(si.quantity_sold * si.price_at_sale), SUM(si.quantity_sold) FROM sales s JOIN sale_items si ON s.id = si.sale_id WHERE s.user_id = ? AND s.sale_date BETWEEN ? AND ?"
        params = [user_id, start_date, end_date]
        if product_id: query += " AND si.product_id = ?"; params.append(product_id)
        try:
            self.cursor.execute(query, params); result = self.cursor.fetchone()
            return {'total_revenue': result[0] or 0.0, 'total_quantity': result[1] or 0}
        except sqlite3.Error as e: print(f"Error calculating progress: {e}"); return {'total_revenue': 0, 'total_quantity': 0}

    def delete_goal(self, goal_id, user_id):
        if not self.cursor: return False, "DB not connected."
        try:
            self.cursor.execute("DELETE FROM goals WHERE id = ? AND user_id = ?", (goal_id, user_id))
            self.conn.commit(); return self.cursor.rowcount > 0, "Goal deleted."
        except sqlite3.Error as e: return False, f"DB error deleting goal: {e}"

    def _create_activity_log_table(self):
        if not self.cursor: return
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL, description TEXT NOT NULL, activity_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE)""")
        self.conn.commit()

    def add_activity_log(self, user_id, activity_type, description):
        if not self.cursor: return
        self.cursor.execute("INSERT INTO activity_log (user_id, activity_type, description) VALUES (?, ?, ?)",
                            (user_id, activity_type, description))
        self.conn.commit()

    def get_recent_activity(self, user_id, limit=5):
        if not self.cursor: return []
        self.cursor.execute("SELECT activity_type, description, activity_date FROM activity_log WHERE user_id = ? ORDER BY activity_date DESC LIMIT ?",
                            (user_id, limit))
        return self.cursor.fetchall()

    def get_kpi_data(self, user_id, start_date=None, end_date=None):
        if not self.cursor: return {}
        if start_date is None: start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        revenue_query = "SELECT SUM(si.quantity_sold * si.price_at_sale) FROM sales s JOIN sale_items si ON s.id = si.sale_id WHERE s.user_id = ? AND s.sale_date >= ?"
        items_sold_query = "SELECT SUM(si.quantity_sold) FROM sales s JOIN sale_items si ON s.id = si.sale_id WHERE s.user_id = ? AND s.sale_date >= ?"
        params = [user_id, start_date]
        if end_date:
            revenue_query += " AND s.sale_date <= ?"; items_sold_query += " AND s.sale_date <= ?"; params.append(end_date)
        try:
            self.cursor.execute(revenue_query, tuple(params)); revenue = self.cursor.fetchone()[0] or 0.0
            self.cursor.execute(items_sold_query, tuple(params)); items_sold = self.cursor.fetchone()[0] or 0
            self.cursor.execute("SELECT SUM(stock_quantity) FROM user_products WHERE user_id = ?", (user_id,)); total_stock = self.cursor.fetchone()[0] or 0
            return {"revenue": revenue, "items_sold": items_sold, "total_stock": total_stock}
        except sqlite3.Error as e: print(f"Error fetching KPI data: {e}"); return {}

    def get_attention_items(self, user_id):
        if not self.cursor: return {'low_stock': []}
        self.cursor.execute("SELECT id, product_name, stock_quantity FROM user_products WHERE user_id = ? AND stock_quantity <= low_stock_threshold AND stock_quantity > 0 ORDER BY stock_quantity ASC LIMIT 5", (user_id,))
        return {'low_stock': self.cursor.fetchall()}

    def get_daily_sales_for_chart(self, user_id, days=30):
        if not self.cursor: return {}
        date_sales = {(datetime.now().date() - timedelta(days=i)): 0.0 for i in range(days)}
        start_date_for_query = datetime.now().date() - timedelta(days=days - 1)
        try:
            self.cursor.execute("SELECT DATE(s.sale_date), SUM(si.quantity_sold * si.price_at_sale) FROM sales s JOIN sale_items si ON s.id = si.sale_id WHERE s.user_id = ? AND DATE(s.sale_date) >= ? GROUP BY DATE(s.sale_date)", (user_id, start_date_for_query))
            for row in self.cursor.fetchall(): date_sales[datetime.strptime(row[0], '%Y-%m-%d').date()] = row[1]
            return dict(sorted(date_sales.items()))
        except sqlite3.Error as e: print(f"Error fetching chart data: {e}"); return {}

    def get_top_products(self, user_id, start_date=None, end_date=None, limit=5):
        if not self.cursor: return []
        if start_date is None: start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        query = "SELECT p.product_name, SUM(si.quantity_sold * si.price_at_sale) as total_revenue FROM sales s JOIN sale_items si ON s.id = si.sale_id JOIN user_products p ON si.product_id = p.id WHERE s.user_id = ? AND s.sale_date >= ?"
        params = [user_id, start_date]
        if end_date: query += " AND s.sale_date <= ?"; params.append(end_date)
        query += " GROUP BY p.product_name ORDER BY total_revenue DESC LIMIT ?"
        params.append(limit)
        try:
            self.cursor.execute(query, tuple(params))
            return self.cursor.fetchall()
        except sqlite3.Error as e: print(f"Error getting top products: {e}"); return []

    def close_connection(self):
        if self.conn:
            print(f"[DatabaseManager] Closing connection to {self.db_path}")
            self.conn.close()
            self.conn = self.cursor = None

    def close_and_reopen_connection(self):
        db_path = self.db_path
        self.close_connection()
        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            print("[DatabaseManager] Database reconnected.")
            return True
        except sqlite3.Error as e:
            print(f"[DB] FATAL: Failed to reconnect. Error: {e}"); return False