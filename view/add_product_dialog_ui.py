# view/add_product_dialog_ui.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDoubleSpinBox, QSpinBox, QPushButton, QHBoxLayout,
    QDialogButtonBox, QScrollArea, QWidget, QLabel, QAbstractSpinBox, QFrame,
    QFileDialog
)
from PySide6.QtCore import Qt

class AddProductDialogUI(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.is_edit_mode = product_data is not None
        title = "Edit Product Details" if self.is_edit_mode else "Add a New Product"
        self.setWindowTitle(title)
        self.setMinimumWidth(550)
        self.resize(600, 700)
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet("QDialog { background-color: #F8F9FA; }")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: transparent; }")

        scroll_content_widget = QWidget()
        form_layout = QFormLayout(scroll_content_widget)
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setSpacing(12)
        form_layout.setContentsMargins(10, 10, 10, 10)
        
        base_style = "border: 1px solid #ccc; border-radius: 4px; padding: 8px; background-color: white;"
        
        self.product_name_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setMinimumHeight(80)
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
        self.notes_input = QTextEdit()
        self.notes_input.setMinimumHeight(60)

        self.image_url_input = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._browse_for_image)
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_url_input)
        image_layout.addWidget(self.browse_button)

        for widget in [self.product_name_input, self.sku_input, self.category_input, self.brand_input,
                       self.description_input, self.purchase_price_input, self.selling_price_input,
                       self.stock_quantity_input, self.low_stock_threshold_input, self.notes_input,
                       self.image_url_input]:
            widget.setStyleSheet(base_style)

        form_layout.addRow(QLabel("<b>Name<font color='red'>*</font>:</b>"), self.product_name_input)
        form_layout.addRow(QLabel("<b>SKU:</b>"), self.sku_input)
        form_layout.addRow(QLabel("<b>Category:</b>"), self.category_input)
        form_layout.addRow(QLabel("<b>Brand:</b>"), self.brand_input)
        form_layout.addRow(QLabel("<b>Description:</b>"), self.description_input)
        form_layout.addRow(QLabel("<b>Purchase Price:</b>"), self.purchase_price_input)
        form_layout.addRow(QLabel("<b>Selling Price<font color='red'>*</font>:</b>"), self.selling_price_input)
        form_layout.addRow(QLabel("<b>Stock Quantity:</b>"), self.stock_quantity_input)
        form_layout.addRow(QLabel("<b>Low Stock Alert:</b>"), self.low_stock_threshold_input)
        form_layout.addRow(QLabel("<b>Image Path:</b>"), image_layout)
        form_layout.addRow(QLabel("<b>Notes:</b>"), self.notes_input)

        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        save_button_text = "Update Product" if self.is_edit_mode else "Save Product"
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText(save_button_text)
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setStyleSheet("background-color: #27ae60; color:white; padding: 8px 25px; border-radius:4px; font-weight:bold;")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("background-color: #95a5a6; color:white; padding: 8px 15px; border-radius:4px;")

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.button_box, 0, Qt.AlignmentFlag.AlignRight)

        if product_data:
            self.populate_form(product_data)
        else:
            self.product_name_input.setFocus()
            
    def _browse_for_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Product Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        if file_path:
            self.image_url_input.setText(file_path)

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