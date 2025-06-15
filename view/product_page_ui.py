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
        
        self.setMinimumSize(220, 300)
        self.setMaximumSize(320, 350)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setObjectName("productCard")
        
        self.setStyleSheet("""
            #productCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #FAFAFA);
                border: 1px solid #E8E8E8;
                border-radius: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            #productCard:hover {
                border: 1px solid #4A90E2;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8FBFF);
                box-shadow: 0 4px 16px rgba(74,144,226,0.15);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(0)

        image_container = QFrame()
        image_container.setObjectName("imageContainer")
        image_container.setStyleSheet("""
            #imageContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom: 1px solid #F0F0F0;
            }
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(140)
        self.image_label.setMaximumHeight(160)
        self.set_product_image(product_data.get('image_url'))
        image_layout.addWidget(self.image_label)
        layout.addWidget(image_container)

        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(16, 12, 16, 8)
        content_layout.setSpacing(8)

        name_label = QLabel(self.product_name)
        name_label.setStyleSheet("""
            font-size: 15px; 
            font-weight: 600; 
            color: #2C3E50;
            line-height: 1.3;
        """)
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(40)
        content_layout.addWidget(name_label)

        desc = product_data.get('description', 'No description available.')
        metrics = self.fontMetrics()
        elided_desc = metrics.elidedText(desc, Qt.TextElideMode.ElideRight, 200)
        description_label = QLabel(elided_desc)
        description_label.setStyleSheet("""
            font-size: 12px; 
            color: #7F8C8D;
            line-height: 1.4;
        """)
        description_label.setMaximumHeight(32)
        content_layout.addWidget(description_label)
        
        content_layout.addStretch()

        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(46,204,113,0.1), stop:1 rgba(52,152,219,0.1));
            border-radius: 8px;
            padding: 8px;
        """)
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 6, 8, 6)
        
        price = product_data.get('selling_price', 0.0)
        price_label = QLabel(f"${price:.2f}")
        price_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #27AE60;
            background: transparent;
        """)
        
        stock = product_data.get('stock_quantity', 0)
        stock_color = "#E74C3C" if stock < 10 else "#F39C12" if stock < 50 else "#27AE60"
        stock_label = QLabel(f"Stock: {stock}")
        stock_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        stock_label.setStyleSheet(f"""
            font-size: 11px; 
            color: {stock_color}; 
            font-weight: 600;
            background: transparent;
            padding: 2px 6px;
            border-radius: 10px;
            background-color: rgba(255,255,255,0.7);
        """)

        info_layout.addWidget(price_label)
        info_layout.addStretch()
        info_layout.addWidget(stock_label)
        content_layout.addWidget(info_frame)
        
        layout.addWidget(content_frame)

        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(16, 0, 16, 0)
        button_layout.setSpacing(8)
        
        details_button = QPushButton("View Details")
        details_button.setCursor(Qt.CursorShape.PointingHandCursor)
        details_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A90E2, stop:1 #357ABD);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5BA0F2, stop:1 #4A90E2);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #357ABD, stop:1 #2E6DA4);
            }
        """)
        details_button.clicked.connect(lambda: self.edit_requested.emit(self.product_id))

        delete_button = QPushButton()
        delete_button.setIcon(QIcon("assets/icons/delete.png"))
        delete_button.setIconSize(QSize(36, 36))
        delete_button.setFixedSize(36, 36)
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setToolTip("Delete Product")
        delete_button.setStyleSheet("""
            QPushButton {
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 16px;
                padding: 0px;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete_requested.emit(self.product_id, self.product_name))

        button_layout.addWidget(details_button, 1)
        button_layout.addWidget(delete_button)
        layout.addWidget(button_frame)

    def set_product_image(self, image_path):
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap("assets/placeholder.png")

        if pixmap.isNull():
            pixmap = QPixmap("assets/placeholder.png")

        target_width = self.width()
        scaled_pixmap = pixmap.scaled(target_width, 140, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        
        target_height = 160 
        
        py = max(0, (scaled_pixmap.height() - target_height) / 2)
        
        cropped_pixmap = scaled_pixmap.copy(0, int(py), target_width, target_height)
        
        self.image_label.setPixmap(cropped_pixmap)

class ProductPageUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.min_card_width = 240
        self.grid_columns = 3
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(20)

        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            #headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(74,144,226,0.05), stop:1 rgba(46,204,113,0.05));
                border-radius: 12px;
                padding: 10px;
            }
        """)
        
        top_bar_layout = QHBoxLayout(header_frame)
        top_bar_layout.setSpacing(15)
        top_bar_layout.setContentsMargins(15, 10, 15, 10)

        self.add_product_button = QPushButton("Add New Product")
        self.add_product_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_product_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2ECC71, stop:1 #27AE60);
                color: white;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3EDD81, stop:1 #2ECC71);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27AE60, stop:1 #229954);
            }
        """)
        top_bar_layout.addWidget(self.add_product_button)
        top_bar_layout.addStretch(1)

        controls_container = QHBoxLayout()
        controls_container.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, SKU, brand...")
        self.search_input.setMinimumWidth(220)
        self.search_input.setFixedHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E8E8E8;
                border-radius: 20px;
                padding: 0 15px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #4A90E2;
                background: #F8FBFF;
            }
            QLineEdit:hover {
                border-color: #B0BEC5;
            }
        """)
        controls_container.addWidget(self.search_input)

        
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_frame.setStyleSheet("""
            #filterFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(74,144,226,0.05), stop:1 rgba(46,204,113,0.05));
                border-radius: 16px;
                padding: 16px;
                border: 1px solid #E8F4FD;
            }
        """)
        top_bar_layout = QHBoxLayout(filter_frame)
        top_bar_layout.setSpacing(15)
        
        self.sort_combo = QComboBox()
        self.sort_combo.setFixedHeight(40)
        self.sort_combo.setMinimumWidth(180)
        self.sort_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E8E8E8;
                border-radius: 20px;
                padding-left: 15px;
                font-size: 13px;
                background: white;
                color: #2C3E50;
            }
            QComboBox:hover {
                border-color: #B0BEC5;
            }
            QComboBox:focus {
                border-color: #4A90E2;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #E8E8E8; border-radius: 8px;
                background: white; selection-background-color: #F0F8FF;
            }
        """)
        self.sort_combo.addItem("Sort by: Name (A-Z)", ('product_name', 'ASC'))
        self.sort_combo.addItem("Sort by: Name (Z-A)", ('product_name', 'DESC'))
        self.sort_combo.addItem("Sort by: Price (Low-High)", ('selling_price', 'ASC'))
        self.sort_combo.addItem("Sort by: Price (High-Low)", ('selling_price', 'DESC'))
        self.sort_combo.addItem("Sort by: Stock (Low-High)", ('stock_quantity', 'ASC'))
        self.sort_combo.addItem("Sort by: Stock (High-Low)", ('stock_quantity', 'DESC'))
        self.sort_combo.addItem("Sort by: Newest", ('created_at', 'DESC'))
        controls_container.addWidget(self.sort_combo)
        
        top_bar_layout.addLayout(controls_container)
        main_layout.addWidget(header_frame)
        
        main_layout.addWidget(filter_frame)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #F5F5F5;
                width: 8px;
                border-radius: 4px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999999;
            }
        """)

        scroll_content = QWidget()
        self.cards_layout = QGridLayout(scroll_content)
        self.cards_layout.setSpacing(20)
        self.cards_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(self.scroll_area, 1)
        
        self.no_products_label = QLabel()
        self.no_products_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_products_label.setStyleSheet("""
            font-size: 16px;
            color: #95A5A6;
            font-style: italic;
            padding: 40px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 rgba(149,165,166,0.1), stop:1 rgba(189,195,199,0.1));
            border-radius: 12px;
            border: 2px dashed #BDC3C7;
        """)
        self.no_products_label.setVisible(False)
        main_layout.addWidget(self.no_products_label, 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        available_width = self.width() - 60 
        self.grid_columns = max(1, available_width // (self.min_card_width + 20))

    def populate_card_grid(self, products, controller):
        row, col = 0, 0
        for product in products:
            card = ProductCardWidget(product)
            card.edit_requested.connect(controller.open_edit_product_dialog)
            card.delete_requested.connect(controller.handle_delete_product_confirmation)
            
            self.cards_layout.addWidget(card, row, col)
            col += 1
            if col >= self.grid_columns:
                col = 0
                row += 1
        
        for remaining_col in range(col, self.grid_columns):
            self.cards_layout.setColumnStretch(remaining_col, 1)
        
        self.cards_layout.setRowStretch(row + 1, 1)

    def clear_card_layout(self):
        while self.cards_layout.count():
            child = self.cards_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        for col in range(self.grid_columns):
            self.cards_layout.setColumnStretch(col, 0)
            
        self.no_products_label.setVisible(False)
        self.scroll_area.setVisible(True)

    def show_no_products_message(self, search_term):
        if search_term:
            self.no_products_label.setText(f"No products match your search for '{search_term}'.\nTry adjusting your search terms.")
        else:
            self.no_products_label.setText("You haven't added any products yet.\n\n Click 'Add New Product' to start building your inventory!")
        self.scroll_area.setVisible(False)
        self.no_products_label.setVisible(True)