# view/product_page.py
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, Slot, QTimer

from .base_dashboard_page import BaseDashboardPage
from .product_page_ui import ProductPageUI
from .add_product_dialog_ui import AddProductDialogUI
from .shared_ui import StyledAlertDialog

class ProductPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, parent=None):
        super().__init__("Manage Your Products", parent=parent)
        self.user_id = user_id
        self.product_processor = product_processor
        self.current_products = [] 

        self.ui = ProductPageUI()
        self.content_layout.addWidget(self.ui)

        self.ui.add_product_button.clicked.connect(self.open_add_product_dialog)
        self.ui.search_input.textChanged.connect(self._debounce_refresh)
        self.ui.sort_combo.currentIndexChanged.connect(self.refresh_product_list)

        self.refresh_timer = QTimer()
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self.refresh_product_list)

    def load_page_data(self):
        super().load_page_data()
        if not self.user_id:
            StyledAlertDialog.show_alert("Error", "User not identified. Cannot load products.", "error", self)
            self.ui.clear_card_layout()
            return
        
        self.ui.search_input.clear()
        self.ui.sort_combo.setCurrentIndex(0)
        self.refresh_product_list()

    def unload_page_data(self):
        super().unload_page_data()
        self.ui.clear_card_layout()

    def _debounce_refresh(self):
        self.refresh_timer.start(300)

    @Slot()
    def refresh_product_list(self):
        if not self.user_id or not self.product_processor:
            return

        search_term = self.ui.search_input.text().strip()
        sort_option = self.ui.sort_combo.currentData()
        sort_by, sort_order = sort_option if sort_option else ('product_name', 'ASC')

        self.current_products = self.product_processor.get_products_for_display(
            user_id=self.user_id,
            search_term=search_term,
            sort_by=sort_by,
            sort_order=sort_order
        )

        self.ui.clear_card_layout()

        if not self.current_products:
            self.ui.show_no_products_message(search_term)
        else:
            self.ui.populate_card_grid(self.current_products, self)

    def open_add_product_dialog(self):
        if not self.user_id:
            StyledAlertDialog.show_alert("Authentication Error", "User not identified.", "error", self)
            return

        dialog = AddProductDialogUI(parent=self)

        if dialog.exec():
            product_data = dialog.get_form_data()
            if not product_data.get('product_name') or product_data.get('selling_price') is None:
                StyledAlertDialog.show_alert("Input Error", "Product Name and Selling Price are required.", "error", self)
                return

            success, message, _ = self.product_processor.add_new_product(self.user_id, product_data)
            StyledAlertDialog.show_alert("Add Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()

    @Slot(int)
    def open_edit_product_dialog(self, product_id):
        product_to_edit = self.product_processor.get_single_product_details(self.user_id, product_id)
        if not product_to_edit:
            StyledAlertDialog.show_alert("Error", f"Product with ID {product_id} not found.", "error", self)
            return

        dialog = AddProductDialogUI(parent=self, product_data=product_to_edit)
        
        if dialog.exec():
            updated_data = dialog.get_form_data()
            if not updated_data.get('product_name') or updated_data.get('selling_price') is None:
                StyledAlertDialog.show_alert("Input Error", "Product Name and Selling Price are required.", "error", self)
                return

            success, message = self.product_processor.update_product_details(self.user_id, product_id, updated_data)
            StyledAlertDialog.show_alert("Update Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()

    @Slot(int, str)
    def handle_delete_product_confirmation(self, product_id, product_name):
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete the product:\n'{product_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.product_processor.remove_product(self.user_id, product_id)
            StyledAlertDialog.show_alert("Delete Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()