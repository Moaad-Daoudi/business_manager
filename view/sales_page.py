from PySide6.QtWidgets import (QTableWidget, QHeaderView, QTableWidgetItem, 
                               QComboBox, QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QSizePolicy)
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

        self.data_changed_signal = data_changed_signal
        self.data_changed_signal.connect(self.handle_global_data_change)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded) 
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
            QScrollBar:vertical {
                background: #F0F0F0;
                width: 15px;
                border-radius: 7px;
                margin: 0;
                border: 1px solid #E0E0E0;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                border-radius: 6px;
                min-height: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9E9E9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        page_content_layout = QVBoxLayout(scroll_content_widget)
        page_content_layout.setContentsMargins(0, 0, 0, 0) 
        page_content_layout.setSpacing(20)

        self._create_filter_bar(page_content_layout)
        self._create_summary_bar(page_content_layout)
        
        table_container = QFrame()
        table_container.setObjectName("tableContainer")
        table_container.setStyleSheet("""
            #tableContainer {
                background: white;
                border-radius: 16px;
                border: 1px solid #E8E8E8;
                padding: 20px;
                margin: 10px 0;
            }
        """)
        table_layout = QVBoxLayout(table_container)
        table_layout.setContentsMargins(0, 0, 0, 0)

        table_header = QLabel("Sales Transactions")
        table_header.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #2C3E50;
            margin-bottom: 15px;
            padding: 0;
        """)
        table_layout.addWidget(table_header)
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(5)
        self.sales_table.setHorizontalHeaderLabels(["Date", "Product Name", "Quantity", "Price", "Revenue"])
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch) 
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents) 
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.verticalHeader().setVisible(True)
        self.sales_table.setMinimumHeight(300)
        self.sales_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
        self.sales_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #F0F0F0;
                background-color: white;
                alternate-background-color: #FAFBFC;
                selection-background-color: rgba(74, 144, 226, 0.2);
                border: none;
                border-radius: 8px;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #F5F5F5;
            }
            QTableWidget::item:selected {
                background-color: rgba(74, 144, 226, 0.15);
                color: #2C3E50;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F8F9FA, stop:1 #E9ECEF);
                color: #495057;
                padding: 12px 8px;
                border: none;
                border-bottom: 2px solid #4A90E2;
                font-weight: 600;
                font-size: 13px;
            }
            QHeaderView::section:first {
                border-top-left-radius: 8px;
            }
            QHeaderView::section:last {
                border-top-right-radius: 8px;
            }
            QScrollBar:vertical {
                background: #F0F0F0;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9E9E9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                background: #F0F0F0;
                height: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:horizontal {
                background: #BDBDBD;
                border-radius: 6px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #9E9E9E;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        
        table_layout.addWidget(self.sales_table)
        page_content_layout.addWidget(table_container)
        page_content_layout.addStretch()

        self.content_layout.addWidget(scroll_area)

    def load_page_data(self):
        super().load_page_data()
        self.handle_global_data_change() 

    def handle_global_data_change(self):
        print("SalesPage detected a data change, refreshing...")
        current_prod_id = self.product_filter_combo.currentData()
        current_date_index = self.date_filter_combo.currentIndex()

        self._populate_product_filter()

        prod_index = self.product_filter_combo.findData(current_prod_id)
        if prod_index != -1:
            self.product_filter_combo.setCurrentIndex(prod_index)
        
        if current_date_index != -1:
            self.date_filter_combo.setCurrentIndex(current_date_index)
        else:
             self.date_filter_combo.setCurrentIndex(2)

        self._update_sales_display()

    def _create_filter_bar(self, parent_layout):
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_frame.setStyleSheet("""
            #filterFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(74,144,226,0.05), stop:1 rgba(46,204,113,0.05));
                border-radius: 16px;
                padding: 20px;
                margin: 10px 0;
                border: 1px solid #E8F4FD;
            }
        """)
        
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(20)
        filter_layout.setContentsMargins(0, 0, 0, 0)

        product_section = QVBoxLayout()
        product_label = QLabel("Filter by Product")
        product_label.setStyleSheet("""
            font-weight: 600;
            color: #2C3E50;
            font-size: 13px;
            margin-bottom: 5px;
        """)
        product_section.addWidget(product_label)
        
        self.product_filter_combo = QComboBox()
        self.product_filter_combo.setMinimumWidth(250)
        self.product_filter_combo.setFixedHeight(40)
        self.product_filter_combo.setStyleSheet("""
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
                background: #F8FBFF;
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
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                background: white;
                selection-background-color: #F0F8FF;
            }
        """)
        product_section.addWidget(self.product_filter_combo)
        filter_layout.addLayout(product_section)

        date_section = QVBoxLayout()
        date_label = QLabel("Filter by Date")
        date_label.setStyleSheet("""
            font-weight: 600;
            color: #2C3E50;
            font-size: 13px;
            margin-bottom: 5px;
        """)
        date_section.addWidget(date_label)
        
        self.date_filter_combo = QComboBox()
        self.date_filter_combo.setFixedHeight(40)
        self.date_filter_combo.setMinimumWidth(150)
        self.date_filter_combo.setStyleSheet("""
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
                background: #F8FBFF;
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
                border: 2px solid #E8E8E8;
                border-radius: 8px;
                background: white;
                selection-background-color: #F0F8FF;
            }
        """)
        self.date_filter_combo.addItem("All Time", "all")
        self.date_filter_combo.addItem("This Week", "week")
        self.date_filter_combo.addItem("This Month", "month")
        date_section.addWidget(self.date_filter_combo)
        filter_layout.addLayout(date_section)

        filter_layout.addStretch()

        apply_btn = QPushButton("Apply Filters")
        apply_btn.setFixedHeight(40)
        apply_btn.clicked.connect(self._update_sales_display)
        apply_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4A90E2, stop:1 #357ABD);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 0 25px;
                font-weight: 600;
                font-size: 13px;
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
        filter_layout.addWidget(apply_btn)
        
        parent_layout.addWidget(filter_frame)

    def _create_summary_bar(self, parent_layout):
        summary_frame = QFrame()
        summary_frame.setObjectName("summaryFrame")
        summary_frame.setStyleSheet("""
            #summaryFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(46,204,113,0.1), stop:0.5 rgba(52,152,219,0.1), stop:1 rgba(155,89,182,0.1));
                border-radius: 16px;
                border: 1px solid rgba(46,204,113,0.2);
                padding: 25px;
                margin: 10px 0;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setSpacing(40)
        
        revenue_card = QFrame()
        revenue_card.setStyleSheet("""
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(46,204,113,0.3);
        """)
        revenue_layout = QVBoxLayout(revenue_card)
        revenue_layout.setSpacing(5)
        
        self.total_revenue_label = QLabel("Total Revenue: $0.00")
        self.total_revenue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_revenue_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #27AE60;
            margin-top: 5px;
        """)
        revenue_layout.addWidget(self.total_revenue_label)
        
        items_card = QFrame()
        items_card.setStyleSheet("""
            background: white;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(52,152,219,0.3);
        """)
        items_layout = QVBoxLayout(items_card)
        items_layout.setSpacing(5)
        
        self.items_sold_label = QLabel("Items Sold: 0")
        self.items_sold_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.items_sold_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #3498DB;
            margin-top: 5px;
        """)
        items_layout.addWidget(self.items_sold_label)
        
        summary_layout.addWidget(revenue_card, 1)
        summary_layout.addWidget(items_card, 1)
        
        parent_layout.addWidget(summary_frame)

    def _populate_product_filter(self):
        self.product_filter_combo.clear()
        self.product_filter_combo.addItem("All Products", 0)
        products = self.product_processor.get_products_for_display(self.user_id)
        for p in products:
            self.product_filter_combo.addItem(f"{p['product_name']}", p['id'])

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
            
            date_item = QTableWidgetItem(sale_date)
            date_item.setToolTip(f"Transaction on {sale_date}")
            
            product_item = QTableWidgetItem(sale['product_name'])
            product_item.setToolTip(f"Product: {sale['product_name']}")
            
            quantity_item = QTableWidgetItem(str(sale['quantity_sold']))
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            quantity_item.setToolTip(f"Quantity sold: {sale['quantity_sold']} units")
            
            price_item = QTableWidgetItem(f"${sale['price_at_sale']:.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            price_item.setToolTip(f"Price per unit: ${sale['price_at_sale']:.2f}")
            
            revenue_item = QTableWidgetItem(f"${sale['total_revenue']:.2f}")
            revenue_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            revenue_item.setToolTip(f"Total revenue: ${sale['total_revenue']:.2f}")
            
            if sale['total_revenue'] > 100:
                revenue_item.setForeground(Qt.GlobalColor.darkGreen)
            elif sale['total_revenue'] > 50:
                revenue_item.setForeground(Qt.GlobalColor.darkBlue)
            
            self.sales_table.setItem(row, 0, date_item)
            self.sales_table.setItem(row, 1, product_item)
            self.sales_table.setItem(row, 2, quantity_item)
            self.sales_table.setItem(row, 3, price_item)
            self.sales_table.setItem(row, 4, revenue_item)

            total_revenue += sale['total_revenue']
            total_items_sold += sale['quantity_sold']
        
        self.sales_table.resizeRowsToContents()
        self.sales_table.resizeColumnsToContents()
        
        row_count = self.sales_table.rowCount()
        if row_count > 0:
            header_height = self.sales_table.horizontalHeader().height()
            row_height = self.sales_table.rowHeight(0)  
            ideal_height = header_height + (row_height * row_count) + 4  
            
            min_height = 300
            max_height = 600
            
            if ideal_height < min_height:
                self.sales_table.setFixedHeight(min_height)
            elif ideal_height > max_height:
                self.sales_table.setFixedHeight(max_height)
            else:
                self.sales_table.setFixedHeight(ideal_height)
        
        self.total_revenue_label.setText(f"Total Revenue\n${total_revenue:,.2f}")
        self.items_sold_label.setText(f"Items Sold\n{total_items_sold:,} units")