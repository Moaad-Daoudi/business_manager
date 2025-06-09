# view/sales_page.py
from PySide6.QtWidgets import (QTableWidget, QHeaderView, QTableWidgetItem, 
                               QComboBox, QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QWidget)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from datetime import datetime, timedelta

from .base_dashboard_page import BaseDashboardPage
from processing.sales_processor import SalesProcessor
from processing.product_processing import ProductProcessor

class SalesPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, data_changed_signal, parent=None):
        super().__init__("Sales History & Revenue", parent=parent)
        self.user_id = user_id
        self.product_processor = product_processor
        self.sales_processor = SalesProcessor(product_processor.db_manager)

        # Store the signal passed from the parent and connect it to a handler
        self.data_changed_signal = data_changed_signal
        self.data_changed_signal.connect(self.handle_global_data_change)

        self._create_filter_bar(self.content_layout)
        self._create_summary_bar(self.content_layout)

        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(["Date", "Product Name", "Quantity Sold", "Price at Sale", "Total Revenue"])
        self.sales_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setMinimumHeight(300)
        self.content_layout.addWidget(self.sales_table)
        self.content_layout.addStretch()

    def load_page_data(self):
        super().load_page_data()
        self.handle_global_data_change() # Use the handler for initial load too

    def handle_global_data_change(self):
        """Called when data is changed elsewhere in the app or on initial page load."""
        print("SalesPage detected a data change, refreshing...")
        # Get the currently selected item before clearing
        current_prod_id = self.product_filter_combo.currentData()
        current_date_index = self.date_filter_combo.currentIndex()

        self._populate_product_filter()

        # Try to restore the previous selection
        prod_index = self.product_filter_combo.findData(current_prod_id)
        if prod_index != -1:
            self.product_filter_combo.setCurrentIndex(prod_index)
        
        if current_date_index != -1:
            self.date_filter_combo.setCurrentIndex(current_date_index)
        else:
             self.date_filter_combo.setCurrentIndex(2) # Default to 'This Month'

        self._update_sales_display()

    def _create_filter_bar(self, parent_layout):
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        filter_layout.addWidget(QLabel("<b>Filter by Product:</b>"))
        self.product_filter_combo = QComboBox()
        self.product_filter_combo.setMinimumWidth(250)
        filter_layout.addWidget(self.product_filter_combo)

        filter_layout.addWidget(QLabel("<b>Filter by Date:</b>"))
        self.date_filter_combo = QComboBox()
        self.date_filter_combo.addItem("All Time", "all")
        self.date_filter_combo.addItem("This Week", "week")
        self.date_filter_combo.addItem("This Month", "month")
        filter_layout.addWidget(self.date_filter_combo)

        apply_btn = QPushButton("Apply Filters")
        apply_btn.clicked.connect(self._update_sales_display)
        filter_layout.addWidget(apply_btn)
        
        filter_layout.addStretch()
        parent_layout.addLayout(filter_layout)

    def _create_summary_bar(self, parent_layout):
        summary_frame = QFrame()
        summary_frame.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef; padding: 15px;")
        summary_layout = QHBoxLayout(summary_frame)
        
        self.total_revenue_label = QLabel("Total Revenue: $0.00")
        self.items_sold_label = QLabel("Items Sold: 0")

        for label in [self.total_revenue_label, self.items_sold_label]:
            label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            summary_layout.addWidget(label, 0, Qt.AlignCenter)
        
        parent_layout.addWidget(summary_frame)

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
        total_revenue, total_items_sold = 0, 0

        for row, sale in enumerate(sales_data):
            self.sales_table.insertRow(row)
            try:
                sale_date = datetime.fromisoformat(sale['sale_date']).strftime('%Y-%m-%d %H:%M')
            except (ValueError, TypeError):
                sale_date = str(sale['sale_date'])
            
            self.sales_table.setItem(row, 0, QTableWidgetItem(sale_date))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            self.sales_table.setItem(row, 2, QTableWidgetItem(str(sale['quantity_sold'])))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"${sale['price_at_sale']:.2f}"))
            self.sales_table.setItem(row, 4, QTableWidgetItem(f"${sale['total_revenue']:.2f}"))

            total_revenue += sale['total_revenue']
            total_items_sold += sale['quantity_sold']
            
        self.total_revenue_label.setText(f"Total Revenue: ${total_revenue:.2f}")
        self.items_sold_label.setText(f"Items Sold: {total_items_sold}")