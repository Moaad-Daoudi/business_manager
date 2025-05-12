# view/settings_page.py
from PySide6.QtWidgets import QLabel
from .base_dashboard_page import BaseDashboardPage

class SettingsPage(BaseDashboardPage):
    def __init__(self, parent=None):
        super().__init__("Application Settings", parent=parent)

        description = QLabel("Configure application preferences, themes, and other settings here.")
        description.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        self.content_layout.addWidget(description)
        self.content_layout.addStretch(1)

    def load_page_data(self):
        super().load_page_data()
        # TODO: Load current settings