# view/sales_page.py
from PySide6.QtWidgets import QLabel, QPushButton
from .base_dashboard_page import BaseDashboardPage

class ProfilePage(BaseDashboardPage):
    def __init__(self, parent=None):
        super().__init__("Sales Management", parent=parent)

        description = QLabel("Record new sales, view sales history, and analyze sales performance.")
        description.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        self.content_layout.addWidget(description)

        record_sale_button = QPushButton("Record New Sale")
        record_sale_button.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db; color: white;
                        border: none; border-radius: 5px;
                        padding: 10px 15px; font-size: 14px; font-weight: bold;
                    }
                    QPushButton:hover { background-color: #5dade2; }
                """)
        record_sale_button.setFixedWidth(180)
        self.content_layout.addWidget(record_sale_button)
        self.content_layout.addStretch(1)

    def load_page_data(self):
        super().load_page_data()
        # TODO: Load sales data