import sqlite3
import random
from datetime import datetime, timedelta
import os

DATABASE_PATH = 'app_database.db'
USER_ID_TO_POPULATE = 1 

def get_products(cursor, user_id):
    cursor.execute("SELECT id, selling_price, stock_quantity FROM user_products WHERE user_id = ?", (user_id,))
    return cursor.fetchall()

def create_random_sales():
    if not os.path.exists(DATABASE_PATH):
        print(f"Database not found at '{DATABASE_PATH}'. Please check the path.")
        return

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    products = get_products(cursor, USER_ID_TO_POPULATE)
    if not products:
        print(f"No products found for user_id {USER_ID_TO_POPULATE}. Add some products first.")
        conn.close()
        return

    print(f"Found {len(products)} products for user {USER_ID_TO_POPULATE}. Generating random sales...")
    sales_created = 0

    for product_id, price, stock in products:
        if stock <= 0:
            continue 

        num_sales = random.randint(1, 5)
        
        for _ in range(num_sales):
            if stock <= 0: break 

            quantity_sold = random.randint(1, min(2, stock))
            
            sale_date = datetime.now() - timedelta(days=random.randint(0, 30))
            total_amount = quantity_sold * price
            
            try:
                cursor.execute("BEGIN TRANSACTION")

                cursor.execute(
                    "INSERT INTO sales (user_id, sale_date, total_amount) VALUES (?, ?, ?)",
                    (USER_ID_TO_POPULATE, sale_date, total_amount)
                )
                sale_id = cursor.lastrowid

                cursor.execute(
                    "INSERT INTO sale_items (sale_id, product_id, quantity_sold, price_at_sale) VALUES (?, ?, ?, ?)",
                    (sale_id, product_id, quantity_sold, price)
                )

                cursor.execute(
                    "UPDATE user_products SET stock_quantity = stock_quantity - ? WHERE id = ?",
                    (quantity_sold, product_id)
                )
                
                conn.commit()
                stock -= quantity_sold
                sales_created += 1

            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                conn.rollback()

    print(f"Done. Created {sales_created} random sale records.")
    conn.close()

if __name__ == "__main__":
    create_random_sales()