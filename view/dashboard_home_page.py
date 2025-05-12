# view/dashboard_home_page.py
from PySide6.QtWidgets import QLabel
from .base_dashboard_page import BaseDashboardPage

class DashboardHomePage(BaseDashboardPage):
    def __init__(self, parent=None):
        super().__init__("Dashboard", parent=parent) # Title for this page

        # Add specific content for the Dashboard Home Page
        welcome_message = QLabel("Welcome to your Track App Dashboard!")
        welcome_message.setStyleSheet("font-size: 18px; color: #34495e;")
        self.content_layout.addWidget(welcome_message)

        overview_text = QLabel(
            "This is the central hub for your application. "
            "From here, you can navigate to manage products, track sales, set goals, and more. "
            "Use the sidebar to access different sections."
        )
        overview_text.setWordWrap(True)
        overview_text.setStyleSheet("font-size: 14px; color: #7f8c8d; line-height: 150%;")
        self.content_layout.addWidget(overview_text)

        # Add a spacer to push content up if needed, or let BaseDashboardPage's AlignTop handle it
        self.content_layout.addStretch(1)

    def load_page_data(self):
        super().load_page_data()
        # TODO: Load summary data, charts, etc. for the dashboard home