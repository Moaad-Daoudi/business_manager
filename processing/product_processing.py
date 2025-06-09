# processing/product_processing.py
class ProductProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_new_product(self, user_id, product_data_dict):
        if not user_id:
            return False, "User ID missing.", None
        if not product_data_dict.get('product_name') or product_data_dict.get('selling_price') is None:
            return False, "Product name and selling price are required.", None
        
        try:
            # Ensure numeric types are correct before sending to DB
            product_data_dict['selling_price'] = float(product_data_dict.get('selling_price', 0.0))
            for field in ['purchase_price', 'stock_quantity', 'low_stock_threshold']:
                value = product_data_dict.get(field)
                if value is not None and str(value).strip() != "":
                    if 'price' in field:
                        product_data_dict[field] = float(value)
                    else:
                        product_data_dict[field] = int(value)
        except (ValueError, TypeError):
            return False, "Invalid numeric value for price or quantity.", None

        product_id, message = self.db_manager.add_product(user_id, product_data_dict)
        return product_id is not None, message, product_id

    def get_products_for_display(self, user_id, **kwargs):
        if not user_id: return []
        products = self.db_manager.get_products_by_user_id(user_id, **kwargs)
        return products

    def get_single_product_details(self, user_id, product_id):
        if not user_id or not product_id: return None
        return self.db_manager.get_product_by_id_and_user_id(product_id, user_id)

    def update_product_details(self, user_id, product_id, product_data_dict):
        if not user_id or not product_id:
            return False, "User or Product ID missing for update."
        
        return self.db_manager.update_product(product_id, user_id, product_data_dict)

    def remove_product(self, user_id, product_id):
        if not user_id or not product_id:
            return False, "User or Product ID missing for delete."

        return self.db_manager.delete_product(product_id, user_id)

    def adjust_product_stock(self, user_id, product_id, adjustment_value):
        """
        Adjusts the stock for a single product.
        'adjustment_value' can be positive (to add stock) or negative (to remove stock).
        """
        if not all([user_id, product_id]):
            return False, "User or Product ID missing."
        
        if adjustment_value == 0:
            return True, "No adjustment made." # Not an error, just no change

        # Get current stock to validate if we are removing too much
        product = self.db_manager.get_product_by_id_and_user_id(product_id, user_id)
        if not product:
            return False, "Product not found."
            
        current_stock = product['stock_quantity']
        new_stock = current_stock + adjustment_value

        if new_stock < 0:
            return False, f"Cannot adjust stock by {adjustment_value}. It would result in a negative quantity ({new_stock})."

        # The update_product method can be used here for simplicity
        update_data = {'stock_quantity': new_stock}
        return self.db_manager.update_product(product_id, user_id, update_data)