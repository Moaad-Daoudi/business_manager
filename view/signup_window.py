# view/signup_window.py
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QLineEdit, QFrame, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox # Added QMessageBox
)

from .shared_ui import ModernGradientWidget, StyledGroupBox, FeaturesGroupBox, ProjectInfoDialog, StyledAlertDialog, BASE_LINE_EDIT_STYLE # Import new alert

class SignupGroupBox(StyledGroupBox):
    signup_form_submitted = Signal(str, str, str)
    login_link_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.name_input = None
        self.email_input = None
        self.password_input = None
        self.terms_checkbox = None
        self.setupUI()

    def _set_field_error_state(self, field, has_error):
        if field:
            field.setProperty("error", has_error)
            field.style().unpolish(field)
            field.style().polish(field)

    def setupUI(self):
        self.setStyleSheet("QGroupBox { background-color: white; border-radius: 16px; border: none; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(15)

        header = QLabel("Sign up for free to track your product") # ... (style same) ...
        header.setStyleSheet("font-weight: 700; font-size: 24px; color: #0D47A1;")
        layout.addWidget(header)
        subtitle = QLabel("Access all features for free") # ... (style same) ...
        subtitle.setStyleSheet("font-weight: 400; font-size: 16px; color: #1976D2; margin-bottom: 10px;")
        layout.addWidget(subtitle)


        def create_input_field(label_text, placeholder, password=False):
            field_layout = QVBoxLayout(); field_layout.setSpacing(5)
            label = QLabel(label_text); label.setStyleSheet("font-weight: 500; font-size: 14px; color: #1976D2;")
            input_field = QLineEdit(); input_field.setPlaceholderText(placeholder)
            if password: input_field.setEchoMode(QLineEdit.Password)
            input_field.setStyleSheet(BASE_LINE_EDIT_STYLE) # Use shared base style
            input_field.setMinimumHeight(45)
            field_layout.addWidget(label); field_layout.addWidget(input_field)
            return field_layout, input_field

        name_layout, self.name_input = create_input_field("What should we call you?", "Enter your name")
        layout.addLayout(name_layout)
        email_layout, self.email_input = create_input_field("What's your email?", "Enter your email (e.g., user@example.com)")
        layout.addLayout(email_layout)
        password_layout, self.password_input = create_input_field("Create a password", "Min. 8 characters") # Placeholder updated
        layout.addLayout(password_layout)

        self.password_strength_label = QLabel("Use 8+ characters with a mix of letters, numbers & symbols.")
        self.password_strength_label.setStyleSheet("font-weight: 400; font-size: 12px; color: #757575; padding-left: 2px;") # Added padding
        layout.addWidget(self.password_strength_label)

        # --- Connect textChanged signals to reset error state ---
        self.name_input.textChanged.connect(lambda: self._set_field_error_state(self.name_input, False))
        self.email_input.textChanged.connect(lambda: self._set_field_error_state(self.email_input, False))
        self.password_input.textChanged.connect(self._update_password_feedback) # For strength and error reset


        terms_layout = QHBoxLayout() # ... (terms_layout is the same) ...
        self.terms_checkbox = QCheckBox()
        self.terms_checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px; border: 1px solid #BBDEFB; }
            QCheckBox::indicator:checked { background-color: #2196F3; border: 1px solid #2196F3; image: url('assets/check.png'); }
        """)
        terms_text = QLabel("I agree to the <a href='#terms'>Terms of use</a> and <a href='#privacy'>Privacy Policy</a>.")
        terms_text.setOpenExternalLinks(False)
        terms_text.linkActivated.connect(self._handle_text_link)
        terms_text.setStyleSheet("font-weight: 400; font-size: 13px; color: #1976D2;"); terms_text.setWordWrap(True)
        terms_layout.addWidget(self.terms_checkbox); terms_layout.addWidget(terms_text, 1)
        layout.addLayout(terms_layout)
        layout.addSpacing(10)


        self.signup_button = QPushButton("Create an account") # ... (style same) ...
        self.signup_button.setStyleSheet("""
            QPushButton { background-color: #1565C0; color: white; border-radius: 10px;
                          font-size: 16px; font-weight: 600; padding: 14px; }
            QPushButton:hover { background-color: #0D47A1; }
            QPushButton:pressed { background-color: #0A3D91; }
        """); self.signup_button.setMinimumHeight(50)
        layout.addWidget(self.signup_button)
        self.signup_button.clicked.connect(self._validate_and_submit_form)

        login_layout = QHBoxLayout() # ... (rest of login_layout is the same) ...
        login_layout.setAlignment(Qt.AlignCenter)
        login_text = QLabel("Already have an account?"); login_text.setStyleSheet("color: #1976D2; font-size: 14px;")
        self.login_link_button = QPushButton("Login")
        font = QFont(); font.setUnderline(True)
        self.login_link_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 14px; font-weight: 600; border: none; }
            QPushButton:hover { color: #1565C0; }
        """); self.login_link_button.setCursor(Qt.PointingHandCursor); self.login_link_button.setFont(font)
        self.login_link_button.clicked.connect(self.login_link_clicked.emit)

        login_layout.addWidget(login_text); login_layout.addWidget(self.login_link_button)
        layout.addLayout(login_layout)
        layout.addStretch()

    def _update_password_feedback(self, text):
        self._set_field_error_state(self.password_input, False) # Reset error on type
        length = len(text)
        has_letter = any(c.isalpha() for c in text)
        has_digit = any(c.isdigit() for c in text)
        has_symbol = any(not c.isalnum() for c in text) # Basic symbol check

        if length == 0:
            self.password_strength_label.setText("Use 8+ characters with a mix of letters, numbers & symbols.")
            self.password_strength_label.setStyleSheet("font-weight: 400; font-size: 12px; color: #757575; padding-left: 2px;")
        elif length < 8:
            self.password_strength_label.setText("<font color='#D32F2F'>Too short (min 8 characters)</font>")
        elif not (has_letter and has_digit and has_symbol):
            missing = []
            if not has_letter: missing.append("letter")
            if not has_digit: missing.append("number")
            if not has_symbol: missing.append("symbol")
            self.password_strength_label.setText(f"<font color='#F57F17'>Weak (needs {', '.join(missing)})</font>") # Orange for weak
        else: # Strong enough by basic criteria
            self.password_strength_label.setText("<font color='#388E3C'>Strong password</font>") # Green for strong

    def _handle_text_link(self, link_text):
        if link_text == "#terms":
            StyledAlertDialog.show_alert("Terms of Use", "This is where the terms of use would be displayed.", alert_type="info", parent=self)
        elif link_text == "#privacy":
            StyledAlertDialog.show_alert("Privacy Policy", "This is where the privacy policy would be displayed.", alert_type="info", parent=self)

    def _validate_and_submit_form(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()

        # Reset all error states first
        self._set_field_error_state(self.name_input, False)
        self._set_field_error_state(self.email_input, False)
        self._set_field_error_state(self.password_input, False) # Password error might be set by strength check too

        errors = []
        if not name:
            errors.append("Name field is required.")
            self._set_field_error_state(self.name_input, True)

        if not email:
            errors.append("Email field is required.")
            self._set_field_error_state(self.email_input, True)
        elif "@" not in email or "." not in email.split("@")[-1]:
            errors.append("Please enter a valid email address.")
            self._set_field_error_state(self.email_input, True)

        if not password:
            errors.append("Password field is required.")
            self._set_field_error_state(self.password_input, True)
            self.password_strength_label.setText("<font color='#D32F2F'>Password is required.</font>")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long.")
            self._set_field_error_state(self.password_input, True)
            self.password_strength_label.setText("<font color='#D32F2F'>Too short (min 8 characters)</font>")
        # Add more password complexity checks if needed and append to errors

        if not self.terms_checkbox.isChecked():
            errors.append("You must agree to the Terms and Privacy Policy.")
            # Optionally, you could highlight the checkbox or its label, but it's less common for checkboxes.

        if errors:
            StyledAlertDialog.show_alert("Signup Input Error", "\n".join(errors), alert_type="error", parent=self)
            return

        self.signup_form_submitted.emit(name, email, password)

    def clear_fields(self): # For SignupPage to call
        if self.name_input: self.name_input.clear()
        if self.email_input: self.email_input.clear()
        if self.password_input: self.password_input.clear()
        if self.terms_checkbox: self.terms_checkbox.setChecked(False)
        self._set_field_error_state(self.name_input, False)
        self._set_field_error_state(self.email_input, False)
        self._set_field_error_state(self.password_input, False)
        self.password_strength_label.setText("Use 8+ characters with a mix of letters, numbers & symbols.")
        self.password_strength_label.setStyleSheet("font-weight: 400; font-size: 12px; color: #757575; padding-left: 2px;")


class SignupPage(QWidget): # ... (SignupPage remains largely the same, ensure it calls the new alert for general signup failures) ...
    process_signup_request = Signal(str, str, str)
    login_requested = Signal()
    def __init__(self):
        super().__init__()
        # ... (setup of gradient_widget, content_layout, features_box, signup_form_box as before) ...
        self.gradient_widget = ModernGradientWidget()
        page_layout = QHBoxLayout(self); page_layout.setContentsMargins(0,0,0,0)
        page_layout.addWidget(self.gradient_widget)

        content_layout = QHBoxLayout(self.gradient_widget)
        content_layout.setContentsMargins(40, 40, 40, 40); content_layout.setSpacing(30)

        self.features_box = FeaturesGroupBox(self.gradient_widget)
        content_layout.addWidget(self.features_box, 1)
        if hasattr(self.features_box, 'learn_more_clicked'):
            self.features_box.learn_more_clicked.connect(self.show_project_info)

        self.signup_form_box = SignupGroupBox(self.gradient_widget)
        content_layout.addWidget(self.signup_form_box, 1)

        self.signup_form_box.signup_form_submitted.connect(self.process_signup_request.emit)
        self.signup_form_box.login_link_clicked.connect(self.login_requested.emit)

    def show_signup_feedback(self, success, message):
        if success:
            StyledAlertDialog.show_alert("Signup Successful", message, alert_type="info", parent=self)
            if hasattr(self.signup_form_box, 'clear_fields'): self.signup_form_box.clear_fields()
            QTimer.singleShot(1000, self.login_requested.emit) # Auto-navigate to login after 1 sec
        else:
            StyledAlertDialog.show_alert("Signup Failed", message, alert_type="error", parent=self)
            # If it's an "email already exists" error, highlight the email field
            if "email" in message.lower() and hasattr(self.signup_form_box, '_set_field_error_state'):
                self.signup_form_box._set_field_error_state(self.signup_form_box.email_input, True)


    def show_project_info(self): # ... (same as before) ...
        info_dialog = ProjectInfoDialog(self)
        # if hasattr(info_dialog, 'signup_action_requested'):
        #     info_dialog.signup_action_requested.connect(self.project_info_signup_requested.emit)
        info_dialog.exec()

# ... (if __name__ == "__main__": block for SignupPage is the same) ...