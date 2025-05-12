# view/base_dashboard_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class BaseDashboardPage(QWidget):
    def __init__(self, title="Page Title", parent=None):
        super().__init__(parent)
        self.setObjectName(f"{title.replace(' ', '')}Page") # For styling or identification

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20) # Consistent padding
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Content starts at the top

        # Title Label for the page
        self.title_label = QLabel(title)
        self.title_label.setObjectName("dashboardPageTitle") # For specific styling
        self.title_label.setStyleSheet("""
            QLabel#dashboardPageTitle {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50; /* Dark blue-grey */
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e0e0e0; /* Light grey separator */
            }
        """)
        layout.addWidget(self.title_label)

        # Placeholder for page-specific content - subclasses will add to this layout
        self.content_layout = layout # Expose layout for subclasses

    def load_page_data(self):
        """
        Placeholder method for subclasses to override.
        Called when the page becomes active.
        """
        print(f"Loading data for {self.title_label.text()}")
        pass

    def unload_page_data(self):
        """
        Placeholder method for subclasses to override.
        Called when the page becomes inactive.
        """
        print(f"Unloading data for {self.title_label.text()}")
        pass