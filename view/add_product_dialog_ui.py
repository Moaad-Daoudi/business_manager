# view/add_product_dialog_ui.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDoubleSpinBox, QSpinBox, QCheckBox, QPushButton, QHBoxLayout,
    QDialogButtonBox, QGroupBox, QScrollArea, QWidget, QSizePolicy, QLabel, QAbstractSpinBox # Added QAbstractSpinBox
)
from PySide6.QtCore import Qt

class AddProductDialogUI(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.is_edit_mode = product_data is not None
        title = "Edit Product" if self.is_edit_mode else "Add New Product"
        self.setWindowTitle(title)
        self.setMinimumWidth(500) # Slightly smaller minimum
        self.resize(600, 650)     # Set a default sensible size
        # self.setMaximumHeight(750) # Let height be more flexible with scroll
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.scroll_content_widget = QWidget()
        scroll_content_layout = QVBoxLayout(self.scroll_content_widget)
        scroll_content_layout.setContentsMargins(10,10,10,10)
        scroll_content_layout.setSpacing(15)

        self.form_groupbox = QGroupBox(title)
        self.form_groupbox.setStyleSheet("QGroupBox { font-size: 15px; font-weight: bold; border: 1px solid #ccc; border-radius: 5px; margin-top: 1ex;} QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px;} ")
        form_v_layout = QVBoxLayout(self.form_groupbox)

        self.product_form_layout = QFormLayout()
        self.product_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.product_form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.product_form_layout.setSpacing(10)
        self.product_form_layout.setContentsMargins(10,10,10,10)
        # --- Crucial for better field distribution ---
        self.product_form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)


        self.product_name_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.description_input = QTextEdit()
        # For QTextEdit, explicitly set a reasonable size policy if needed
        self.description_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.description_input.setMinimumHeight(60) # Ensure it has some initial height
        self.description_input.setMaximumHeight(100) # Prevent it from getting too tall

        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setPrefix("$ "); self.purchase_price_input.setDecimals(2); self.purchase_price_input.setRange(0, 999999.99)
        self.purchase_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setPrefix("$ "); self.selling_price_input.setDecimals(2); self.selling_price_input.setRange(0, 999999.99)
        self.selling_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.stock_quantity_input = QSpinBox()
        self.stock_quantity_input.setRange(0, 99999); self.stock_quantity_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.low_stock_threshold_input = QSpinBox()
        self.low_stock_threshold_input.setRange(0, 9999); self.low_stock_threshold_input.setValue(5)
        self.low_stock_threshold_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        self.image_url_input = QLineEdit() # For image path/URL
        self.notes_input = QTextEdit()
        self.notes_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.notes_input.setMinimumHeight(50)
        self.notes_input.setMaximumHeight(80)


        # Add rows to form
        self.product_form_layout.addRow(QLabel("Name*:"), self.product_name_input)
        self.product_form_layout.addRow(QLabel("SKU:"), self.sku_input)
        self.product_form_layout.addRow(QLabel("Category:"), self.category_input)
        self.product_form_layout.addRow(QLabel("Brand:"), self.brand_input)
        self.product_form_layout.addRow(QLabel("Description:"), self.description_input)
        self.product_form_layout.addRow(QLabel("Purchase Price:"), self.purchase_price_input)
        self.product_form_layout.addRow(QLabel("Selling Price*:"), self.selling_price_input)
        self.product_form_layout.addRow(QLabel("Stock Quantity:"), self.stock_quantity_input)
        self.product_form_layout.addRow(QLabel("Low Stock Threshold:"), self.low_stock_threshold_input)
        self.product_form_layout.addRow(QLabel("Image URL:"), self.image_url_input)
        self.product_form_layout.addRow(QLabel("Notes:"), self.notes_input)

        form_v_layout.addLayout(self.product_form_layout)
        scroll_content_layout.addWidget(self.form_groupbox)
        # Removed addStretch here to let form determine its natural size better within scroll area

        self.scroll_area.setWidget(self.scroll_content_widget)
        main_layout.addWidget(self.scroll_area)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        save_button_text = "Update Product" if self.is_edit_mode else "Save Product"
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText(save_button_text)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setStyleSheet("background-color: #27ae60; color:white; padding: 8px 15px; border-radius:4px; font-weight:bold;")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("background-color: #95a5a6; color:white; padding: 8px 15px; border-radius:4px;")

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.button_box)

        if product_data:
            self.populate_form(product_data)
        else: # Set focus for new product
            self.product_name_input.setFocus()


    def populate_form(self, data):
        self.product_name_input.setText(data.get('product_name', ''))
        self.sku_input.setText(data.get('sku', ''))
        self.category_input.setText(data.get('category', ''))
        self.brand_input.setText(data.get('brand', ''))
        self.description_input.setPlainText(data.get('description', ''))
        self.purchase_price_input.setValue(data.get('purchase_price', 0.0) or 0.0)
        self.selling_price_input.setValue(data.get('selling_price', 0.0) or 0.0)
        self.stock_quantity_input.setValue(data.get('stock_quantity', 0) or 0)
        self.low_stock_threshold_input.setValue(data.get('low_stock_threshold', 5) or 5)
        self.image_url_input.setText(data.get('image_url', ''))
        self.notes_input.setPlainText(data.get('notes', ''))

    def get_form_data(self):
        return {
            'product_name': self.product_name_input.text().strip(),
            'sku': self.sku_input.text().strip() or None,
            'category': self.category_input.text().strip() or None,
            'brand': self.brand_input.text().strip() or None,
            'description': self.description_input.toPlainText().strip() or None,
            'purchase_price': self.purchase_price_input.value(),
            'selling_price': self.selling_price_input.value(),
            'stock_quantity': self.stock_quantity_input.value(),
            'low_stock_threshold': self.low_stock_threshold_input.value(),
            'image_url': self.image_url_input.text().strip() or None,
            'notes': self.notes_input.toPlainText().strip() or None,
        }

# ... (if __name__ == "__main__": block for testing as before)