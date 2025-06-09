# view/profile_page.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFrame, QFormLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .base_dashboard_page import BaseDashboardPage
from .shared_ui import StyledAlertDialog
# The 'utils/theme_manager' import has been removed.

class ProfilePage(BaseDashboardPage):
    # The constructor no longer needs the product_processor, so it's simplified.
    def __init__(self, user_id, user_processor, data_changed_signal, parent=None):
        super().__init__("Profile & Settings", parent=parent)
        self.user_id = user_id
        self.user_processor = user_processor
        self.data_changed_signal = data_changed_signal

        # --- Create and add the settings cards ---
        self.content_layout.addWidget(self._create_info_card())
        self.content_layout.addWidget(self._create_security_card())
        
        # The "Appearance" card is no longer created.
        
        self.content_layout.addStretch()

    def load_page_data(self):
        """Called when the page becomes visible."""
        super().load_page_data()
        # Load the current user's data into the form fields
        user = self.user_processor.db_manager.get_user_by_id(self.user_id)
        if user:
            self.name_input.setText(user.get('name', ''))
            self.email_input.setText(user.get('email', ''))
        
        # The logic to set the theme toggle's state has been removed.

    def _create_styled_card(self, title):
        """Helper function to create a consistent card widget."""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        card_layout.addWidget(title_label)
        
        return card, card_layout

    def _create_info_card(self):
        """Creates the card for updating personal information."""
        card, layout = self._create_styled_card("Personal Information")
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        form_layout.addRow("<b>Name:</b>", self.name_input)
        form_layout.addRow("<b>Email:</b>", self.email_input)
        
        layout.addLayout(form_layout)

        save_info_btn = QPushButton("Save Changes")
        save_info_btn.setCursor(Qt.PointingHandCursor)
        save_info_btn.clicked.connect(self._save_personal_info)
        layout.addWidget(save_info_btn, 0, Qt.AlignRight)
        
        return card

    def _create_security_card(self):
        """Creates the card for changing the password."""
        card, layout = self._create_styled_card("Security")
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        self.old_pass_input = QLineEdit()
        self.old_pass_input.setEchoMode(QLineEdit.Password)
        self.new_pass_input = QLineEdit()
        self.new_pass_input.setEchoMode(QLineEdit.Password)
        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("<b>Current Password:</b>", self.old_pass_input)
        form_layout.addRow("<b>New Password:</b>", self.new_pass_input)
        form_layout.addRow("<b>Confirm New Password:</b>", self.confirm_pass_input)
        
        layout.addLayout(form_layout)
        
        change_pass_btn = QPushButton("Change Password")
        change_pass_btn.setCursor(Qt.PointingHandCursor)
        change_pass_btn.clicked.connect(self._change_password)
        layout.addWidget(change_pass_btn, 0, Qt.AlignRight)
        
        return card

    # The _create_appearance_card and _toggle_theme methods have been completely removed.

    def _save_personal_info(self):
        new_data = {
            'name': self.name_input.text().strip(),
            'email': self.email_input.text().strip()
        }
        success, message = self.user_processor.update_user_details(self.user_id, new_data)
        StyledAlertDialog.show_alert("Update Profile", message, "info" if success else "error")
        if success:
            self.data_changed_signal.emit("user_info")

    def _change_password(self):
        old_pass = self.old_pass_input.text()
        new_pass = self.new_pass_input.text()
        confirm_pass = self.confirm_pass_input.text()

        if not new_pass or not old_pass:
            StyledAlertDialog.show_alert("Error", "All password fields are required.", "error")
            return

        if new_pass != confirm_pass:
            StyledAlertDialog.show_alert("Error", "New passwords do not match.", "error")
            return
            
        success, message = self.user_processor.change_password(self.user_id, old_pass, new_pass)
        StyledAlertDialog.show_alert("Change Password", message, "info" if success else "error")
        if success:
            self.old_pass_input.clear()
            self.new_pass_input.clear()
            self.confirm_pass_input.clear()