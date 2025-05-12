# view/product_page.py
from PySide6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QHBoxLayout, QMessageBox, QWidget # Added QWidget
)
from PySide6.QtCore import Qt, Slot, Signal # Added Signal if needed later, Slot for clarity
from PySide6.QtGui import QIcon # For button icons

# Assuming these are in the same 'view' package or paths are correctly set up
from .base_dashboard_page import BaseDashboardPage
from .product_page_ui import ProductPageUI # The UI layout class
from .shared_ui import StyledAlertDialog   # For user feedback

# ProductProcessor is expected to be passed in the constructor

class ProductPage(BaseDashboardPage):
    # Optional signals if this page needed to communicate upwards beyond direct calls
    # product_operation_completed_signal = Signal() # Example

    def __init__(self, owner_username, product_processor, parent=None):
        super().__init__("Manage Your Products", parent=parent) # Title for the BaseDashboardPage
        self.owner_username = owner_username
        self.product_processor = product_processor
        self.current_edit_product_id = None # Tracks the ID of the product being edited

        # --- Main Layout ---
        # self.content_layout is inherited from BaseDashboardPage (it's a QVBoxLayout)

        # --- Add New Product Button ---
        self.add_new_product_button = QPushButton(QIcon.fromTheme("list-add", QIcon("assets/icons/add.png")), " Add New Product") # Fallback icon path
        self.add_new_product_button.setObjectName("addNewProductBtn")
        self.add_new_product_button.setStyleSheet("""
            QPushButton#addNewProductBtn {
                background-color: #27ae60; /* Green */
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                text-align: left; /* Icon on left, text next to it */
            }
            QPushButton#addNewProductBtn:hover { background-color: #2ecc71; }
        """)
        self.add_new_product_button.setFixedHeight(40)
        self.add_new_product_button.clicked.connect(self.open_add_product_dialog)
        self.content_layout.addWidget(self.add_new_product_button)


        # --- Product List Table (using ProductPageUI's table) ---
        # The ProductPageUI itself will be the main content holder below the title
        self.ui = ProductPageUI() # Instantiate the UI part that contains table and form (form is hidden by default here)
        
        # We will hide the form from ProductPageUI by default and only use its table and list action buttons initially
        # The Add/Edit dialog will handle the form.
        self.ui.form_groupbox.setVisible(False) # Hide the inline form from ProductPageUI

        # Connect signals from the UI elements within ProductPageUI (if they were used directly)
        # For now, we are using the new AddProductDialogUI for forms.
        # The table actions (Edit/Delete buttons per row) will be added dynamically.
        
        # Connect list action buttons if they exist from ProductPageUI (these are below the table)
        if hasattr(self.ui, 'edit_selected_button'):
            self.ui.edit_selected_button.clicked.connect(self._trigger_edit_for_selected_row)
        if hasattr(self.ui, 'delete_selected_button'):
            self.ui.delete_selected_button.clicked.connect(self._trigger_delete_for_selected_row)

        # Add the ProductPageUI widget (which now mainly shows the table and its action buttons)
        # to the content_layout of BaseDashboardPage
        self.content_layout.addWidget(self.ui)
        # self.content_layout.addStretch(1) # BaseDashboardPage's AlignTop handles this

    def load_page_data(self):
        """Called when the page becomes active."""
        super().load_page_data() # Calls print statement from BaseDashboardPage
        if not self.owner_username:
            StyledAlertDialog.show_alert("Error", "User not identified. Cannot load products.", "error", self)
            if hasattr(self.ui, 'product_table'): self.ui.product_table.setRowCount(0)
            return
        self.refresh_product_list()

    def refresh_product_list(self):
        """Fetches products for the current user and populates the table."""
        if not self.owner_username:
            print("[ProductPage] Cannot refresh list: owner_username is not set.")
            return
        if not self.product_processor:
            print("[ProductPage] Cannot refresh list: product_processor is not set.")
            return
        if not hasattr(self.ui, 'product_table'):
            print("[ProductPage] Cannot refresh list: UI table not found.")
            return

        products = self.product_processor.get_products_for_display(self.owner_username)
        self.ui.product_table.setRowCount(0) # Clear existing rows

        if not products:
            print(f"[ProductPage] No products found for user: {self.owner_username}")
            # Optionally, display a "No products found" message in the UI
            return

        self.ui.product_table.setRowCount(len(products))
        for row_idx, prod in enumerate(products):
            # ID
            id_item = QTableWidgetItem(str(prod.get('id', '')))
            id_item.setData(Qt.ItemDataRole.UserRole, prod.get('id')) # Store actual ID
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.product_table.setItem(row_idx, 0, id_item)
            # Name
            self.ui.product_table.setItem(row_idx, 1, QTableWidgetItem(str(prod.get('product_name', ''))))
            # SKU
            self.ui.product_table.setItem(row_idx, 2, QTableWidgetItem(str(prod.get('sku', ''))))
            # Category
            self.ui.product_table.setItem(row_idx, 3, QTableWidgetItem(str(prod.get('category', ''))))
            # Selling Price
            price_item = QTableWidgetItem(f"${float(prod.get('selling_price', 0.0)):.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.ui.product_table.setItem(row_idx, 4, price_item)
            # Stock
            stock_item = QTableWidgetItem(str(prod.get('stock_quantity', 0)))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.product_table.setItem(row_idx, 5, stock_item)
            # Sold Quantity (Placeholder)
            sold_item = QTableWidgetItem(str(prod.get('sold_quantity', 0))) # Placeholder
            sold_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.product_table.setItem(row_idx, 6, sold_item)

            # --- Action Buttons in Table Cell ---
            btn_edit = QPushButton(QIcon.fromTheme("document-edit", QIcon("assets/icons/edit.png")), " Edit")
            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_edit.setStyleSheet("background-color: #3498db; color:white; padding: 5px 8px; border-radius:3px; font-size:11px; margin-right: 2px;")
            btn_edit.clicked.connect(lambda checked=False, pid=prod.get('id'): self.open_edit_product_dialog(pid))

            btn_delete = QPushButton(QIcon.fromTheme("edit-delete", QIcon("assets/icons/delete.png")), " Del")
            btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_delete.setStyleSheet("background-color: #e74c3c; color:white; padding: 5px 8px; border-radius:3px; font-size:11px;")
            btn_delete.clicked.connect(lambda checked=False, pid=prod.get('id'), pname=prod.get('product_name'): self.handle_delete_product_confirmation(pid, pname))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.addWidget(btn_edit)
            actions_layout.addWidget(btn_delete)
            actions_layout.setContentsMargins(2,2,2,2)
            actions_layout.setSpacing(5)
            actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center buttons in cell
            self.ui.product_table.setCellWidget(row_idx, 7, actions_widget) # Actions in the 8th column (index 7)

    def open_add_product_dialog(self):
        if not self.owner_username:
            StyledAlertDialog.show_alert("Authentication Error", "User not identified. Please log in again.", "error", self)
            return

        # Import AddProductDialogUI here to avoid circular dependency if it also imports ProductPage or BaseDashboardPage
        # Or ensure it's imported at the top of the file if there's no circularity concern.
        try:
            from .add_product_dialog_ui import AddProductDialogUI
        except ImportError:
            StyledAlertDialog.show_alert("Error", "Add Product Dialog UI could not be loaded.", "error", self)
            return

        dialog = AddProductDialogUI(parent=self) # Pass self as parent
        if dialog.exec(): # True if "Save" was clicked (dialog.accept() was called)
            product_data = dialog.get_form_data()

            # Basic validation in the page before sending to processor
            if not product_data.get('product_name') or product_data.get('selling_price') is None or float(product_data.get('selling_price', -1)) < 0:
                StyledAlertDialog.show_alert("Input Error", "Product Name and a valid non-negative Selling Price are required.", "error", self)
                # self.open_add_product_dialog() # Optionally reopen dialog, but can be annoying
                return

            success, message, new_product_id = self.product_processor.add_new_product(self.owner_username, product_data)
            StyledAlertDialog.show_alert("Add Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()
        else:
            print("[ProductPage] Add product dialog was cancelled.")


    def open_edit_product_dialog(self, product_id):
        if not self.owner_username or not product_id:
            StyledAlertDialog.show_alert("Error", "Cannot edit product: Missing user or product identifier.", "error", self)
            return

        product_to_edit = self.product_processor.get_single_product_details(self.owner_username, product_id)
        if not product_to_edit:
            StyledAlertDialog.show_alert("Error", f"Product with ID {product_id} not found or does not belong to you.", "error", self)
            return

        try:
            from .add_product_dialog_ui import AddProductDialogUI
        except ImportError:
            StyledAlertDialog.show_alert("Error", "Edit Product Dialog UI could not be loaded.", "error", self)
            return

        dialog = AddProductDialogUI(parent=self, product_data=product_to_edit) # Pass existing data
        if dialog.exec():
            updated_data = dialog.get_form_data()
            if not updated_data.get('product_name') or updated_data.get('selling_price') is None or float(updated_data.get('selling_price', -1)) < 0:
                StyledAlertDialog.show_alert("Input Error", "Product Name and a valid non-negative Selling Price are required for update.", "error", self)
                return

            success, message = self.product_processor.update_product_details(self.owner_username, product_id, updated_data)
            StyledAlertDialog.show_alert("Update Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()
        else:
            print(f"[ProductPage] Edit product dialog for ID {product_id} was cancelled.")


    def handle_delete_product_confirmation(self, product_id, product_name):
        if not self.owner_username or not product_id:
            StyledAlertDialog.show_alert("Error", "Cannot delete product: Missing user or product identifier.", "error", self)
            return

        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete product:\n'{product_name}' (ID: {product_id})?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.product_processor.remove_product(self.owner_username, product_id)
            StyledAlertDialog.show_alert("Delete Product", message, "info" if success else "error", self)
            if success:
                self.refresh_product_list()

    # --- Handlers for buttons below the table (if kept from ProductPageUI) ---
    def _get_selected_product_id_from_table(self):
        """Helper to get product ID from the selected row in the table."""
        if not hasattr(self.ui, 'product_table'): return None
        selected_items = self.ui.product_table.selectedItems()
        if not selected_items:
            return None # No selection
        
        selected_rows = sorted(list(set(item.row() for item in selected_items)))
        if len(selected_rows) != 1: # Ensure only one row is effectively selected
            return None 
            
        row = selected_rows[0]
        id_item = self.ui.product_table.item(row, 0) # ID is in column 0
        if id_item:
            return id_item.data(Qt.ItemDataRole.UserRole) or int(id_item.text())
        return None

    def _trigger_edit_for_selected_row(self):
        product_id = self._get_selected_product_id_from_table()
        if product_id:
            self.open_edit_product_dialog(product_id)
        else:
            StyledAlertDialog.show_alert("Selection Error", "Please select a single product from the list to edit.", "warning", self)

    def _trigger_delete_for_selected_row(self):
        product_id = self._get_selected_product_id_from_table()
        if product_id:
            # Need product name for confirmation, fetch it or pass it differently
            # For simplicity, we'll just use ID in confirmation here
            # Better: Store name along with ID or fetch name before confirmation
            name_item = self.ui.product_table.item(self.ui.product_table.currentRow(), 1) # Assuming name is in col 1
            product_name = name_item.text() if name_item else f"ID: {product_id}"
            self.handle_delete_product_confirmation(product_id, product_name)
        else:
            StyledAlertDialog.show_alert("Selection Error", "Please select a single product from the list to delete.", "warning", self)

    def unload_page_data(self):
        super().unload_page_data()
        # Clear the table when navigating away to ensure fresh data on next load
        if hasattr(self.ui, 'product_table'): self.ui.product_table.setRowCount(0)