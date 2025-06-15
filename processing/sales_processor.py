class SalesProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_sales_for_display(self, user_id, start_date=None, end_date=None, product_id=None):
        """
        Retrieves sales data for the sales page.
        """
        return self.db_manager.get_sales_records(user_id, start_date, end_date, product_id)