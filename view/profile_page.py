from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QLineEdit, QFrame, QFormLayout, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .base_dashboard_page import BaseDashboardPage
from .shared_ui import StyledAlertDialog, ThemeToggleSwitch 

class ProfilePageStyles:
    
    @staticmethod
    def get_card_style(theme="light"):
        if theme == "dark":
            return """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1F2937, stop:1 #111827);
                    border: 1px solid #374151;
                    border-radius: 16px;
                }
            """
        else:
            return """
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #FFFFFF, stop:1 #F8FAFC);
                    border: 1px solid #E2E8F0;
                    border-radius: 16px;
                }
            """
    
    @staticmethod
    def get_title_style(theme="light", size=24):
        color = "#F9FAFB" if theme == "dark" else "#1F2937"
        return f"""
            QLabel {{
                color: {color};
                font-size: {size}px;
                font-weight: 700;
                margin-bottom: 8px;
                padding: 0;
                border: none;
                background: transparent;
            }}
        """
    
    @staticmethod
    def get_description_style(theme="light"):
        color = "#9CA3AF" if theme == "dark" else "#6B7280"
        return f"""
            QLabel {{
                color: {color};
                font-size: 14px;
                font-weight: 400;
                margin-bottom: 20px;
                padding: 0;
                border: none;
                background: transparent;
            }}
        """
    
    @staticmethod
    def get_label_style(theme="light"):
        color = "#D1D5DB" if theme == "dark" else "#374151"
        return f"""
            QLabel {{
                color: {color};
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 8px;
                padding: 0;
                border: none;
                background: transparent;
            }}
        """
    
    @staticmethod
    def get_input_style(theme="light"):
        if theme == "dark":
            bg_color = "#374151"
            border_color = "#4B5563"
            text_color = "#F9FAFB"
            focus_border = "#60A5FA"
        else:
            bg_color = "#FFFFFF"
            border_color = "#E5E7EB"
            text_color = "#1F2937"
            focus_border = "#3B82F6"
            
        return f"""
            QLineEdit {{
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: {text_color};
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border-color: {focus_border};
            }}
        """
    
    @staticmethod
    def get_button_style(button_type="primary", theme="light"):
        styles = {
            "primary": {
                "light": { "bg": "#10B981", "hover": "#059669", "pressed": "#047857" },
                "dark": { "bg": "#059669", "hover": "#047857", "pressed": "#065F46" }
            },
            "warning": {
                "light": { "bg": "#F59E0B", "hover": "#D97706", "pressed": "#B45309" },
                "dark": { "bg": "#D97706", "hover": "#B45309", "pressed": "#92400E" }
            }
        }
        style_config = styles.get(button_type, styles["primary"])[theme]
        
        return f"""
            QPushButton {{
                background-color: {style_config['bg']};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {style_config['hover']}; }}
            QPushButton:pressed {{ background-color: {style_config['pressed']}; }}
        """
    
    @staticmethod
    def get_separator_style(theme="light"):
        color = "#4B5563" if theme == "dark" else "#E2E8F0"
        return f"""
            QFrame {{
                background-color: {color};
                border: none;
                height: 1px;
            }}
        """

class ProfilePage(BaseDashboardPage):
    def __init__(self, user_id, user_processor, data_changed_signal, parent=None, theme="light"):
        super().__init__("Profile & Settings", parent=parent)
        self.user_id = user_id
        self.user_processor = user_processor
        self.data_changed_signal = data_changed_signal
        self.theme = theme # You can connect this to a theme manager later
        self.styles = ProfilePageStyles()

        # --- Main Layout with Scroll Area for Flexibility ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                color: black;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)


        scroll_content_widget = QWidget()
        scroll_area.setWidget(scroll_content_widget)

        cards_layout = QVBoxLayout(scroll_content_widget)
        cards_layout.setContentsMargins(20, 10, 20, 20)
        cards_layout.setSpacing(25)
        cards_layout.setAlignment(Qt.AlignTop)

        cards_layout.addWidget(self._create_info_card())
        cards_layout.addWidget(self._create_security_card())
        
        self.content_layout.addWidget(scroll_area)

    def load_page_data(self):
        super().load_page_data()
        user = self.user_processor.db_manager.get_user_by_id(self.user_id)
        if user:
            self.name_input.setText(user.get('name', ''))
            self.email_input.setText(user.get('email', ''))

    def _create_styled_card(self, title, title_size=24):
        card = QFrame()
        card.setStyleSheet(self.styles.get_card_style(self.theme))
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(32, 24, 32, 24)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(self.styles.get_title_style(self.theme, title_size))
        card_layout.addWidget(title_label)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet(self.styles.get_separator_style(self.theme))
        card_layout.addWidget(separator)
        
        return card, card_layout

    def _create_info_card(self):
        card, layout = self._create_styled_card("Personal Information")
        
        desc_label = QLabel("Update your personal details and contact information.")
        desc_label.setStyleSheet(self.styles.get_description_style(self.theme))
        layout.addWidget(desc_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        name_label = QLabel("Full Name")
        name_label.setStyleSheet(self.styles.get_label_style(self.theme))
        
        email_label = QLabel("Email Address")
        email_label.setStyleSheet(self.styles.get_label_style(self.theme))
        
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(self.styles.get_input_style(self.theme))
        self.name_input.setPlaceholderText("Enter your full name")
        
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(self.styles.get_input_style(self.theme))
        self.email_input.setPlaceholderText("Enter your email address")
        
        form_layout.addRow(name_label)
        form_layout.addRow(self.name_input)
        form_layout.addRow(email_label)
        form_layout.addRow(self.email_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()

        save_info_btn = QPushButton("Save Changes")
        save_info_btn.setCursor(Qt.PointingHandCursor)
        save_info_btn.setStyleSheet(self.styles.get_button_style("primary", self.theme))
        save_info_btn.clicked.connect(self._save_personal_info)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(save_info_btn)
        layout.addLayout(button_layout)
        
        return card

    def _create_security_card(self):
        card, layout = self._create_styled_card("Security", title_size=22)
        
        desc_label = QLabel("Change your account password to keep your data secure.")
        desc_label.setStyleSheet(self.styles.get_description_style(self.theme))
        layout.addWidget(desc_label)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)
        
        current_pass_label = QLabel("Current Password")
        current_pass_label.setStyleSheet(self.styles.get_label_style(self.theme))
        new_pass_label = QLabel("New Password")
        new_pass_label.setStyleSheet(self.styles.get_label_style(self.theme))
        confirm_pass_label = QLabel("Confirm New Password")
        confirm_pass_label.setStyleSheet(self.styles.get_label_style(self.theme))

        self.old_pass_input = QLineEdit()
        self.old_pass_input.setEchoMode(QLineEdit.Password)
        self.old_pass_input.setStyleSheet(self.styles.get_input_style(self.theme))
        self.old_pass_input.setPlaceholderText("Enter your current password")

        self.new_pass_input = QLineEdit()
        self.new_pass_input.setEchoMode(QLineEdit.Password)
        self.new_pass_input.setStyleSheet(self.styles.get_input_style(self.theme))
        self.new_pass_input.setPlaceholderText("Enter your new password (min. 8 characters)")
        
        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setEchoMode(QLineEdit.Password)
        self.confirm_pass_input.setStyleSheet(self.styles.get_input_style(self.theme))
        self.confirm_pass_input.setPlaceholderText("Confirm your new password")
        
        form_layout.addRow(current_pass_label)
        form_layout.addRow(self.old_pass_input)
        form_layout.addRow(new_pass_label)
        form_layout.addRow(self.new_pass_input)
        form_layout.addRow(confirm_pass_label)
        form_layout.addRow(self.confirm_pass_input)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        change_pass_btn = QPushButton("Change Password")
        change_pass_btn.setCursor(Qt.PointingHandCursor)
        change_pass_btn.setStyleSheet(self.styles.get_button_style("warning", self.theme))
        change_pass_btn.clicked.connect(self._change_password)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(change_pass_btn)
        layout.addLayout(button_layout)
        
        return card

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