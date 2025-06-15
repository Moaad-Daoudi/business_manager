from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit,
    QDoubleSpinBox, QSpinBox, QPushButton, QHBoxLayout,
    QDialogButtonBox, QScrollArea, QWidget, QLabel, QAbstractSpinBox, QFrame,
    QFileDialog, QComboBox
)
from PySide6.QtCore import Qt, QEvent

class ScrollEventBlocker(QWidget):
    def eventFilter(self, watched, event):
        scroll_events = {
            QEvent.Type.Wheel,          
            QEvent.Type.Scroll,         
            QEvent.Type.Gesture,        
        }
        event.ignore()
        if event.type() in scroll_events:
            if isinstance(watched, (QSpinBox, QDoubleSpinBox, QComboBox)):
                if watched.hasFocus():
                    watched.clearFocus()
                return True
        
        return super().eventFilter(watched, event)
    

class AddProductDialogUI(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.is_edit_mode = product_data is not None
        title = "Edit Product Details" if self.is_edit_mode else "Add a New Product"
        self.setWindowTitle(title)
        self.setMinimumWidth(550)
        self.resize(600, 700)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-radius: 12px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        header_label = QLabel(title)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px 0;
                border-bottom: 2px solid #3498db;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(header_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #ecf0f1;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3c7;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
        """)

        scroll_content_widget = QWidget()
        scroll_content_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        form_layout = QFormLayout(scroll_content_widget)
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        input_style = """
            QLineEdit, QTextEdit {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                padding: 12px 15px;
                background-color: #ffffff;
                font-size: 14px;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
                outline: none;
            }
            QLineEdit:hover, QTextEdit:hover {
                border-color: #bdc3c7;
            }
            QLineEdit:hover:focus, QTextEdit:hover:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
                outline: none;
            }
        """
        
        spinbox_style = """
            #spinBox {
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                padding: 12px 15px;
                background-color: #ffffff;
                font-size: 14px;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
            #spinBox:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
                outline: none;
            }
            #spinBox:hover {
                border-color: #bdc3c7;
            }
            #spinBox:hover:focus {
                border-color: #3498db;
                background-color: #fbfcfd;
                outline: none;
            }
        """
        
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #34495e;
                padding: 5px 0;
            }
        """
        
        self.product_name_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setMinimumHeight(100)
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setObjectName("spinBox")
        self.purchase_price_input.setPrefix("$ "); self.purchase_price_input.setDecimals(2); self.purchase_price_input.setRange(0, 999999.99)
        self.purchase_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.selling_price_input = QDoubleSpinBox()
        self.selling_price_input.setObjectName("spinBox")
        self.selling_price_input.setPrefix("$ "); self.selling_price_input.setDecimals(2); self.selling_price_input.setRange(0, 999999.99)
        self.selling_price_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.stock_quantity_input = QSpinBox()
        self.stock_quantity_input.setObjectName("spinBox")
        self.stock_quantity_input.setRange(0, 99999); 
        self.stock_quantity_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.low_stock_threshold_input = QSpinBox()
        self.low_stock_threshold_input.setObjectName("spinBox")
        self.low_stock_threshold_input.setRange(0, 9999); 
        self.low_stock_threshold_input.setValue(5)
        self.low_stock_threshold_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.notes_input = QTextEdit()
        self.notes_input.setMinimumHeight(80)

        self.image_url_input = QLineEdit()
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #74b9ff, stop:1 #0984e3);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #81c784, stop:1 #66bb6a);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5c7cfa, stop:1 #495057);
            }
        """)
        self.browse_button.clicked.connect(self._browse_for_image)
        
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_url_input, 1)
        image_layout.addWidget(self.browse_button)
        image_layout.setSpacing(10)
        
        self.scroll_blocker = ScrollEventBlocker(self)
        
        widgets_to_modify = [self.purchase_price_input, self.selling_price_input,
                       self.stock_quantity_input, self.low_stock_threshold_input]
        
        
        line_edit_widgets = [
            self.product_name_input, self.sku_input, self.category_input,
            self.brand_input, self.image_url_input
        ]
        
        text_edit_widgets = [self.description_input, self.notes_input]
        
        for widget in widgets_to_modify:
            widget.installEventFilter(self.scroll_blocker)
                        
        for widget in line_edit_widgets:
            widget.setStyleSheet(input_style)
            
        for widget in text_edit_widgets:
            widget.setStyleSheet(input_style)

        for widget in widgets_to_modify:
            widget.setStyleSheet(spinbox_style)
            

        def create_label(text, required=False):
            label = QLabel(text)
            if required:
                label.setText(f"{text} <span style='color: #e74c3c; font-weight: bold;'>*</span>")
            label.setStyleSheet(label_style)
            return label

        form_layout.addRow(create_label("Product Name", True), self.product_name_input)
        form_layout.addRow(create_label("SKU"), self.sku_input)
        form_layout.addRow(create_label("Category"), self.category_input)
        form_layout.addRow(create_label("Brand"), self.brand_input)
        form_layout.addRow(create_label("Description"), self.description_input)
        form_layout.addRow(create_label("Purchase Price"), self.purchase_price_input)
        form_layout.addRow(create_label("Selling Price", True), self.selling_price_input)
        form_layout.addRow(create_label("Stock Quantity"), self.stock_quantity_input)
        form_layout.addRow(create_label("Low Stock Alert"), self.low_stock_threshold_input)
        form_layout.addRow(create_label("Image Path"), image_layout)
        form_layout.addRow(create_label("Notes"), self.notes_input)

        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        save_button_text = "Update Product" if self.is_edit_mode else "Save Product"
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setText(save_button_text)
        
        self.button_box.button(QDialogButtonBox.StandardButton.Save).setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ecc71, stop:1 #27ae60);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
                transform: translateY(0px);
            }
        """)
        
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bdc3c7, stop:1 #95a5a6);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
                transform: translateY(0px);
            }
        """)

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