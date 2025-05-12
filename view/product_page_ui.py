# view/product_page_ui.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QDoubleSpinBox, QSpinBox, QCheckBox, QPushButton, QFormLayout, QAbstractSpinBox,
    QTableWidget, QAbstractItemView, QHeaderView, QGroupBox, QSizePolicy
)
from PySide6.QtCore import Qt

class ProductPageUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ProductPageUI")

        # Main vertical layout for the entire product page content (form + list)
        main_page_layout = QVBoxLayout(self)
        main_page_layout.setContentsMargins(0, 0, 0, 0) # Margins handled by BaseDashboardPage
        main_page_layout.setSpacing(15)

        # --- Form Section ---
        self.form_groupbox = QGroupBox("Add / Edit Product")
        self.form_groupbox.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; margin-bottom: 10px;} ")
        form_v_layout = QVBoxLayout(self.form_groupbox) # Layout inside the groupbox

        self.product_form_layout = QFormLayout()
        self.product_form_layout.setContentsMargins(10, 15, 10, 15) # Padding inside form
        self.product_form_layout.setSpacing(10)
        self.product_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.product_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)


        self.name_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setFixedHeight(80)
        self.category_input = QLineEdit()
        self.brand_input = QLineEdit()

        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setPrefix("$ ")
        self.purchase_price_input.setDecimals(2)
        self.purchase_price_input.setRange(0, 999999.99)
        self.purchase_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setPrefix("$ ")
        self.selling_price_input.setDecimals(2)
        self.selling_price_input.setRange(0, 999999.99)
        self.selling_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


        self.stock_quantity_input = QSpinBox()
        self.stock_quantity_input.setRange(-99999, 99999) # Allow negative for adjustments? Or keep >=0
        self.stock_quantity_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


        self.low_stock_threshold_input = QSpinBox()
        self.low_stock_threshold_input.setRange(0,9999)
        self.low_stock_threshold_input.setValue(5) # Default
        self.low_stock_threshold_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)


        self.supplier_name_input = QLineEdit()
        self.image_url_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setFixedHeight(60)
        self.is_active_checkbox = QCheckBox("Product is Active")
        self.is_active_checkbox.setChecked(True)

        # Add rows to form
        self.product_form_layout.addRow("Name*:", self.name_input)
        self.product_form_layout.addRow("SKU:", self.sku_input)
        self.product_form_layout.addRow("Category:", self.category_input)
        self.product_form_layout.addRow("Brand:", self.brand_input)
        self.product_form_layout.addRow("Description:", self.description_input)
        self.product_form_layout.addRow("Purchase Price:", self.purchase_price_input)
        self.product_form_layout.addRow("Selling Price*:", self.selling_price_input)
        self.product_form_layout.addRow("Stock Quantity:", self.stock_quantity_input)
        self.product_form_layout.addRow("Low Stock Threshold:", self.low_stock_threshold_input)
        self.product_form_layout.addRow("Supplier:", self.supplier_name_input)
        self.product_form_layout.addRow("Image URL:", self.image_url_input)
        self.product_form_layout.addRow("Notes:", self.notes_input)
        self.product_form_layout.addRow("", self.is_active_checkbox)

        form_v_layout.addLayout(self.product_form_layout) # Add QFormLayout to groupbox's QVBoxLayout

        self.form_buttons_layout = QHBoxLayout()
        self.add_update_button = QPushButton("Add Product")
        self.add_update_button.setObjectName("addProductButton")
        self.add_update_button.setStyleSheet("""
            QPushButton#addProductButton {
                background-color: #27ae60; color: white; padding: 10px 20px;
                border-radius: 5px; font-weight: bold; font-size: 14px;
            }
            QPushButton#addProductButton:hover { background-color: #2ecc71; }
        """)
        self.clear_form_button = QPushButton("Clear Form")
        self.clear_form_button.setObjectName("clearProductFormButton")
        self.clear_form_button.setStyleSheet("""
            QPushButton#clearProductFormButton {
                background-color: #95a5a6; color: white; padding: 10px 15px;
                border-radius: 5px; font-size: 14px;
            }
            QPushButton#clearProductFormButton:hover { background-color: #bdc3c7; }
        """)
        self.form_buttons_layout.addStretch()
        self.form_buttons_layout.addWidget(self.clear_form_button)
        self.form_buttons_layout.addWidget(self.add_update_button)
        form_v_layout.addLayout(self.form_buttons_layout)

        main_page_layout.addWidget(self.form_groupbox)
        # self.form_groupbox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum) # Prevent form from taking too much vertical space

        # --- Product List Section ---
        self.product_list_label = QLabel("Your Products")
        self.product_list_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 5px; color: #34495e;")
        main_page_layout.addWidget(self.product_list_label)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(7)
        self.product_table.setHorizontalHeaderLabels(["ID", "Name", "SKU", "Category", "Sell Price", "Stock", "Active"])
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.product_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.product_table.verticalHeader().setVisible(False)
        self.product_table.horizontalHeader().setStretchLastSection(True)
        self.product_table.setAlternatingRowColors(True)
        self.product_table.setShowGrid(False)
        self.product_table.setStyleSheet("""
            QTableWidget { border: 1px solid #ddd; border-radius: 5px; }
            QHeaderView::section { background-color: #ecf0f1; padding: 5px; border: none; font-weight: bold; }
            QTableWidget::item { padding: 5px; }
        """)

        header = self.product_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive) # ID
        self.product_table.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)    # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive) # SKU
        self.product_table.setColumnWidth(2, 120)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive) # Category
        self.product_table.setColumnWidth(3, 120)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive) # Price
        self.product_table.setColumnWidth(4, 100)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive) # Stock
        self.product_table.setColumnWidth(5, 70)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Interactive) # Active
        self.product_table.setColumnWidth(6, 70)

        main_page_layout.addWidget(self.product_table)

        self.list_actions_layout = QHBoxLayout()
        self.edit_selected_button = QPushButton("Edit Selected")
        self.edit_selected_button.setObjectName("editProductButton")
        self.delete_selected_button = QPushButton("Delete Selected")
        self.delete_selected_button.setObjectName("deleteProductButton")

        common_action_button_style = """
            QPushButton { padding: 8px 15px; border-radius: 4px; font-size: 13px; margin-top: 5px;}
            QPushButton:hover { background-color: #ecf0f1; }
        """
        self.edit_selected_button.setStyleSheet(common_action_button_style + "QPushButton { background-color: #e0e0e0; }")
        self.delete_selected_button.setStyleSheet(common_action_button_style + "QPushButton { background-color: #e74c3c; color: white; } QPushButton:hover { background-color: #c0392b; }")

        self.list_actions_layout.addStretch()
        self.list_actions_layout.addWidget(self.edit_selected_button)
        self.list_actions_layout.addWidget(self.delete_selected_button)
        main_page_layout.addLayout(self.list_actions_layout)