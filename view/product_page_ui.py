# view/product_page_ui.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QScrollArea, QGridLayout, QFrame, QComboBox, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QPainter, QIcon
import os

class ProductCardWidget(QFrame):
    edit_requested = Signal(int)
    delete_requested = Signal(int, str)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_id = product_data.get('id')
        self.product_name = product_data.get('product_name', 'N/A')
        
        self.setMinimumSize(250, 320)
        self.setMaximumSize(300, 320)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setObjectName("productCard")
        self.setStyleSheet("""
            #productCard {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
            }
            #productCard:hover {
                border: 1px solid #0078D7;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(8)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(150)
        self.image_label.setStyleSheet("background-color: #F5F5F5; border-top-left-radius: 11px; border-top-right-radius: 11px;")
        self.set_product_image(product_data.get('image_url'))
        layout.addWidget(self.image_label)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(15, 5, 15, 5)
        content_layout.setSpacing(5)

        name_label = QLabel(self.product_name)
        name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #333;")
        name_label.setWordWrap(True)
        content_layout.addWidget(name_label)

        desc = product_data.get('description', 'No description available.')
        metrics = self.fontMetrics()
        elided_desc = metrics.elidedText(desc, Qt.TextElideMode.ElideRight, 220)
        description_label = QLabel(elided_desc)
        description_label.setStyleSheet("font-size: 13px; color: #666;")
        content_layout.addWidget(description_label)
        
        content_layout.addStretch()

        info_layout = QHBoxLayout()
        price = product_data.get('selling_price', 0.0)
        price_label = QLabel(f"${price:.2f}")
        price_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
        
        stock = product_data.get('stock_quantity', 0)
        stock_label = QLabel(f"Stock: {stock}")
        stock_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        stock_label.setStyleSheet("font-size: 13px; color: #777; font-weight: 500;")

        info_layout.addWidget(price_label)
        info_layout.addStretch()
        info_layout.addWidget(stock_label)
        content_layout.addLayout(info_layout)
        
        layout.addLayout(content_layout)
        layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(15, 0, 15, 0)
        
        details_button = QPushButton("View Details")
        details_button.setCursor(Qt.CursorShape.PointingHandCursor)
        details_button.setStyleSheet("""
            QPushButton { background-color: #E3F2FD; color: #1976D2; border:none; border-radius: 5px; padding: 8px; font-weight: bold; }
            QPushButton:hover { background-color: #BBDEFB; }
        """)
        details_button.clicked.connect(lambda: self.edit_requested.emit(self.product_id))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon("assets/icons/delete.png"))
        delete_button.setIconSize(QSize(25, 25))
        delete_button.setFixedSize(32, 32)
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setToolTip("Delete Product")
        delete_button.setStyleSheet("""
            QPushButton { background-color: #FFEBEE; color: #D32F2F; border:none; border-radius: 16px; }
            QPushButton:hover { background-color: #FFCDD2; }
        """)
        delete_button.clicked.connect(lambda: self.delete_requested.emit(self.product_id, self.product_name))

        button_layout.addWidget(details_button, 1)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

    def set_product_image(self, image_path):
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap("assets/placeholder.png")

        if pixmap.isNull():
            pixmap = QPixmap("assets/placeholder.png")

        scaled_pixmap = pixmap.scaled(280, 150, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        w, h = 280, 150
        px, py = (scaled_pixmap.width() - w) / 2, (scaled_pixmap.height() - h) / 2
        cropped_pixmap = scaled_pixmap.copy(int(px), int(py), w, h)
        
        self.image_label.setPixmap(cropped_pixmap)


class ProductPageUI(QWidget):
    GRID_COLUMNS = 4 

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 0, 0)
        main_layout.setSpacing(20)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(15)

        self.add_product_button = QPushButton(QIcon("assets/icons/add.png"), "  Add New Product")
        self.add_product_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_product_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white; padding: 10px 20px;
                border: none; border-radius: 5px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #2ecc71; }
        """)
        top_bar_layout.addWidget(self.add_product_button)
        top_bar_layout.addStretch(1)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, SKU, brand...")
        self.search_input.setMinimumWidth(250)
        self.search_input.setFixedHeight(38)
        self.search_input.setStyleSheet("QLineEdit { border: 1px solid #ccc; border-radius: 5px; padding: 0 10px; } QLineEdit:focus { border-color: #0078D7; }")
        top_bar_layout.addWidget(self.search_input)

        self.sort_combo = QComboBox()
        self.sort_combo.setFixedHeight(38)
        self.sort_combo.setMinimumWidth(180)
        self.sort_combo.setStyleSheet("QComboBox { border: 1px solid #ccc; border-radius: 5px; padding-left: 10px; }")
        self.sort_combo.addItem("Sort by: Name (A-Z)", ('product_name', 'ASC'))
        self.sort_combo.addItem("Sort by: Name (Z-A)", ('product_name', 'DESC'))
        self.sort_combo.addItem("Sort by: Price (Low-High)", ('selling_price', 'ASC'))
        self.sort_combo.addItem("Sort by: Price (High-Low)", ('selling_price', 'DESC'))
        self.sort_combo.addItem("Sort by: Stock (Low-High)", ('stock_quantity', 'ASC'))
        self.sort_combo.addItem("Sort by: Stock (High-Low)", ('stock_quantity', 'DESC'))
        self.sort_combo.addItem("Sort by: Newest", ('created_at', 'DESC'))
        top_bar_layout.addWidget(self.sort_combo)
        
        main_layout.addLayout(top_bar_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")

        scroll_content = QWidget()
        self.cards_layout = QGridLayout(scroll_content)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(self.scroll_area, 1)
        
        self.no_products_label = QLabel()
        self.no_products_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_products_label.setStyleSheet("font-size: 18px; color: #999; font-style: italic;")
        self.no_products_label.setVisible(False)
        main_layout.addWidget(self.no_products_label, 1)

    def populate_card_grid(self, products, controller):
        row, col = 0, 0
        for product in products:
            card = ProductCardWidget(product)
            card.edit_requested.connect(controller.open_edit_product_dialog)
            card.delete_requested.connect(controller.handle_delete_product_confirmation)
            
            self.cards_layout.addWidget(card, row, col)
            col += 1
            if col >= self.GRID_COLUMNS:
                col = 0
                row += 1
        self.cards_layout.setRowStretch(row + 1, 1)

    def clear_card_layout(self):
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.no_products_label.setVisible(False)
        self.scroll_area.setVisible(True)

    def show_no_products_message(self, search_term):
        if search_term:
            self.no_products_label.setText(f"No products match your search for '{search_term}'.")
        else:
            self.no_products_label.setText("You haven't added any products yet. Click 'Add New Product' to start!")
        self.scroll_area.setVisible(False)
        self.no_products_label.setVisible(True)