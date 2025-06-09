# view/sales_page.py
from PySide6.QtWidgets import (QTableWidget, QHeaderView, QTableWidgetItem, 
                               QComboBox, QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout)
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from datetime import datetime, timedelta

from .base_dashboard_page import BaseDashboardPage 
from processing.sales_processor import SalesProcessor
from processing.product_processing import ProductProcessor

class SalesPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, parent=None):
        super().__init__("Sales Overview", parent=parent) # Changed title for a more modern feel
        self.user_id = user_id
        self.product_processor = product_processor
        self.sales_processor = SalesProcessor(product_processor.db_manager)

        # --- Summary Stat Cards ---
        self._create_summary_cards(self.content_layout)

        # --- Filter Bar ---
        self._create_filter_bar(self.content_layout)
        
        # --- Sales Table ---
        self.sales_table = QTableWidget()
        self._style_sales_table()
        self.content_layout.addWidget(self.sales_table)
        self.content_layout.addStretch()

    def load_page_data(self):
        super().load_page_data()
        self._populate_product_filter()
        self.date_filter_combo.setCurrentIndex(2) # Default to "This Month"
        self._update_sales_display()

    def _create_summary_cards(self, parent_layout):
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        self.total_revenue_card = self._create_info_card("Total Revenue", "$0.00", "assets/icons/revenue.png")
        self.items_sold_card = self._create_info_card("Items Sold", "0", "assets/icons/items_sold.png")
        self.total_sales_card = self._create_info_card("Total Sales", "0", "assets/icons/total_sales.png")

        cards_layout.addWidget(self.total_revenue_card)
        cards_layout.addWidget(self.items_sold_card)
        cards_layout.addWidget(self.total_sales_card)
        cards_layout.addStretch()

        parent_layout.addLayout(cards_layout)

    def _create_info_card(self, title_text, value_text, icon_path):
        card = QFrame()
        card.setObjectName("infoCard")
        card.setMinimumHeight(120)
        card.setStyleSheet("""
            #infoCard {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                border-radius: 8px;
            }
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setPixmap(QPixmap(icon_path).scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        text_layout.setAlignment(Qt.AlignVCenter)
        
        title_label = QLabel(title_text)
        title_label.setStyleSheet("font-size: 14px; color: #6c757d;")
        
        value_label = QLabel(value_text)
        value_label.setObjectName("valueLabel")
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)

        card_layout.addWidget(icon_label)
        card_layout.addSpacing(15)
        card_layout.addLayout(text_layout)
        card_layout.addStretch()
        
        return card
        
    def _create_filter_bar(self, parent_layout):
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_frame.setStyleSheet("""
            #filterFrame { 
                background-color: #F8F9FA; 
                border-radius: 8px;
            }
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(15, 15, 15, 15)
        filter_layout.setSpacing(15)

        base_style = "border: 1px solid #ccc; border-radius: 4px; padding: 8px;"

        filter_layout.addWidget(QLabel("Product:"))
        self.product_filter_combo = QComboBox()
        self.product_filter_combo.setMinimumWidth(250)
        self.product_filter_combo.setStyleSheet(base_style)
        filter_layout.addWidget(self.product_filter_combo)

        filter_layout.addWidget(QLabel("Date Range:"))
        self.date_filter_combo = QComboBox()
        self.date_filter_combo.addItem("All Time", "all")
        self.date_filter_combo.addItem("This Week", "week")
        self.date_filter_combo.addItem("This Month", "month")
        self.date_filter_combo.setStyleSheet(base_style)
        filter_layout.addWidget(self.date_filter_combo)

        apply_btn = QPushButton("Apply Filters")
        apply_btn.setCursor(Qt.PointingHandCursor)
        apply_btn.setStyleSheet("""
            QPushButton { 
                background-color: #007bff; color: white; border: none; 
                border-radius: 4px; padding: 8px 20px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0069d9; }
        """)
        apply_btn.clicked.connect(self._update_sales_display)
        
        filter_layout.addStretch()
        filter_layout.addWidget(apply_btn)
        
        parent_layout.addWidget(filter_frame)

    def _style_sales_table(self):
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(["Date", "Product Name", "Qty", "Unit Price", "Total Revenue"])
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setSelectionMode(QTableWidget.SingleSelection)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setShowGrid(False)
        self.sales_table.verticalHeader().setVisible(False)

        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #dee2e6;
                font-size: 13px;
                font-weight: bold;
            }
        """)
        self.sales_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QTableWidget::item { padding: 10px; }
            QTableWidget::item:selected { background-color: #e9ecef; color: #000; }
        """)

    def _populate_product_filter(self):
        self.product_filter_combo.clear()
        self.product_filter_combo.addItem("All Products", 0)
        products = self.product_processor.get_products_for_display(self.user_id)
        for p in products:
            self.product_filter_combo.addItem(p['product_name'], p['id'])

    def _update_sales_display(self):
        if not self.user_id: return

        product_id = self.product_filter_combo.currentData()
        if product_id == 0: product_id = None

        date_key = self.date_filter_combo.currentData()
        today = datetime.now()
        start_date, end_date = None, None

        if date_key == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif date_key == 'month':
            start_date = today.replace(day=1)
            next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            end_date = next_month - timedelta(days=1)
        
        start_date_str = start_date.strftime('%Y-%m-%d 00:00:00') if start_date else None
        end_date_str = end_date.strftime('%Y-%m-%d 23:59:59') if end_date else None

        sales_data = self.sales_processor.get_sales_for_display(
            self.user_id,
            start_date=start_date_str,
            end_date=end_date_str,
            product_id=product_id
        )

        self.sales_table.setRowCount(0)
        total_revenue, total_items_sold = 0, len(sales_data)

        for row, sale in enumerate(sales_data):
            self.sales_table.insertRow(row)
            try:
                sale_date = datetime.fromisoformat(sale['sale_date']).strftime('%b %d, %Y')
            except (ValueError, TypeError):
                sale_date = str(sale['sale_date'])
            
            qty_item = QTableWidgetItem(str(sale['quantity_sold']))
            qty_item.setTextAlignment(Qt.AlignCenter)

            self.sales_table.setItem(row, 0, QTableWidgetItem(sale_date))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            self.sales_table.setItem(row, 2, qty_item)
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"${sale['price_at_sale']:.2f}"))
            self.sales_table.setItem(row, 4, QTableWidgetItem(f"${sale['total_revenue']:.2f}"))

            total_revenue += sale['total_revenue']
        
        # Update summary cards
        self.total_revenue_card.findChild(QLabel, "valueLabel").setText(f"${total_revenue:.2f}")
        self.items_sold_card.findChild(QLabel, "valueLabel").setText(str(sum(s['quantity_sold'] for s in sales_data)))
        self.total_sales_card.findChild(QLabel, "valueLabel").setText(str(len(sales_data)))