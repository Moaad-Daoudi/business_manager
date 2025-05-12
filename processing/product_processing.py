# processing/product_processing.py
# from model.product_database_manager import ProductDatabaseManager # Injected

class ProductProcessor:
    def __init__(self, product_db_manager): # Now takes ProductDatabaseManager
        self.product_db_manager = product_db_manager

    def add_new_product(self, owner_username, product_data_dict):
        # Basic validation (can be more extensive)
        if not owner_username:
            return False, "Owner username missing.", None
        if not product_data_dict.get('product_name') or product_data_dict.get('selling_price') is None:
            return False, "Product name and selling price are required.", None
        
        try: # Ensure numeric types
            product_data_dict['selling_price'] = float(product_data_dict.get('selling_price', 0.0))
            # Handle optional numeric fields
            for field, default, type_func in [
                ('purchase_price', 0.0, float),
                ('stock_quantity', 0, int),
                ('low_stock_threshold', 5, int)
            ]:
                value = product_data_dict.get(field)
                if value is None or str(value).strip() == "": product_data_dict[field] = default
                else: product_data_dict[field] = type_func(value)
        except ValueError:
            return False, "Invalid numeric value for price or quantity.", None

        product_id, message = self.product_db_manager.add_product(owner_username, product_data_dict)
        return product_id is not None, message, product_id

    def get_products_for_display(self, owner_username, **kwargs): # search, category, sort etc.
        if not owner_username:
            return []
        products = self.product_db_manager.get_products_by_username(owner_username, **kwargs)
        # Here you could enrich product data, e.g., calculate "sold quantity" if you had a sales table
        # For now, just return them.
        for prod in products:
            prod['sold_quantity'] = 0 # Placeholder
            prod['revenue_generated'] = 0.0 # Placeholder
        return products

    def get_single_product_details(self, owner_username, product_id):
        if not owner_username or not product_id:
            return None
        product = self.product_db_manager.get_product_by_id_and_username(product_id, owner_username)
        if product:
            product['sold_quantity'] = 0 # Placeholder
        return product

    def update_product_details(self, owner_username, product_id, product_data_dict):
        if not owner_username or not product_id:
            return False, "User or Product ID missing for update."
        # ... (type conversions as in add_new_product) ...
        try:
            if 'selling_price' in product_data_dict and (product_data_dict['selling_price'] is not None and str(product_data_dict['selling_price']).strip() != ""):
                product_data_dict['selling_price'] = float(product_data_dict['selling_price'])
            # ... (other numeric field conversions)
        except ValueError:
            return False, "Invalid numeric value during update."

        return self.product_db_manager.update_product(product_id, owner_username, product_data_dict)

    def remove_product(self, owner_username, product_id):
        if not owner_username or not product_id:
            return False, "User or Product ID missing for delete."
        return self.product_db_manager.delete_product(product_id, owner_username)