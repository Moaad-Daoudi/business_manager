from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox
)
from .shared_ui import ModernGradientWidget, StyledGroupBox, FeaturesGroupBox, ProjectInfoDialog, StyledAlertDialog, BASE_LINE_EDIT_STYLE 

class LoginGroupBox(StyledGroupBox):
    login_form_submitted = Signal(str, str)
    forgot_password_requested = Signal()
    signup_link_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.email_input = None 
        self.password_input = None
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

        header = QLabel("Welcome back"); header.setStyleSheet("font-weight: 700; font-size: 24px; color: #0D47A1;")
        layout.addWidget(header)
        subtitle = QLabel("Sign in to continue"); subtitle.setStyleSheet("font-weight: 400; font-size: 16px; color: #1976D2; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        def create_input_field(label_text, placeholder, password=False):
            field_layout = QVBoxLayout(); field_layout.setSpacing(5)
            label = QLabel(label_text); label.setStyleSheet("font-weight: 500; font-size: 14px; color: #1976D2;")
            input_field = QLineEdit(); input_field.setPlaceholderText(placeholder)
            if password: input_field.setEchoMode(QLineEdit.Password)
            input_field.setStyleSheet(BASE_LINE_EDIT_STYLE) 
            input_field.setMinimumHeight(45)
            field_layout.addWidget(label); field_layout.addWidget(input_field)
            return field_layout, input_field

        email_layout, self.email_input = create_input_field("Email", "Enter your email")
        layout.addLayout(email_layout)
        password_layout, self.password_input = create_input_field("Password", "Enter your password", password=True)
        layout.addLayout(password_layout)
        
        self.email_input.textChanged.connect(lambda: self._set_field_error_state(self.email_input, False))
        self.password_input.textChanged.connect(lambda: self._set_field_error_state(self.password_input, False))


        options_layout = QHBoxLayout()
        self.remember_checkbox = QCheckBox()
        self.remember_checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 16px; height: 16px; border-radius: 4px; border: 1px solid #BBDEFB; }
            QCheckBox::indicator:checked { background-color: #2196F3; border: 1px solid #2196F3; image: url('assets/check.png'); }
        """)
        remember_text = QLabel("Remember me"); remember_text.setStyleSheet("font-weight: 400; font-size: 13px; color: #1976D2;")
        remember_layout = QHBoxLayout()
        remember_layout.addWidget(self.remember_checkbox); remember_layout.addWidget(remember_text)

        self.forgot_password_button = QPushButton("Forgot password?")
        self.forgot_password_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 13px; font-weight: 600; border: none; text-align: right; }
            QPushButton:hover { color: #1565C0; }
        """); self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.forgot_password_requested.emit)

        options_layout.addLayout(remember_layout); options_layout.addStretch(); options_layout.addWidget(self.forgot_password_button)
        layout.addLayout(options_layout)
        layout.addSpacing(15)


        self.login_button = QPushButton("Sign in")
        self.login_button.setStyleSheet("""
            QPushButton { background-color: #1565C0; color: white; border-radius: 10px;
                          font-size: 16px; font-weight: 600; padding: 14px; }
            QPushButton:hover { background-color: #0D47A1; }
            QPushButton:pressed { background-color: #0A3D91; }
        """); self.login_button.setMinimumHeight(50)
        layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self._validate_and_submit_form)

        signup_layout = QHBoxLayout()
        signup_layout.setAlignment(Qt.AlignCenter)
        signup_text = QLabel("Don't have an account?"); signup_text.setStyleSheet("color: #1976D2; font-size: 14px;")
        self.signup_link_button = QPushButton("Sign up")
        font = QFont(); font.setUnderline(True)
        self.signup_link_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 14px; font-weight: 600; border: none; }
            QPushButton:hover { color: #1565C0; }
        """); self.signup_link_button.setCursor(Qt.PointingHandCursor); self.signup_link_button.setFont(font)
        self.signup_link_button.clicked.connect(self.signup_link_clicked.emit)

        signup_layout.addWidget(signup_text); signup_layout.addWidget(self.signup_link_button)
        layout.addLayout(signup_layout)
        layout.addStretch()


    def _validate_and_submit_form(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()

        self._set_field_error_state(self.email_input, False)
        self._set_field_error_state(self.password_input, False)
        
        errors = []
        if not email:
            errors.append("Email field is required.")
            self._set_field_error_state(self.email_input, True)
        elif "@" not in email or "." not in email.split("@")[-1]:
            errors.append("Please enter a valid email address.")
            self._set_field_error_state(self.email_input, True)

        if not password:
            errors.append("Password field is required.")
            self._set_field_error_state(self.password_input, True)

        if errors:
            StyledAlertDialog.show_alert("Login Input Error", "\n".join(errors), alert_type="error", parent=self)
            return
        
        self.login_form_submitted.emit(email, password)

    def clear_fields(self):
        if self.email_input: self.email_input.clear()
        if self.password_input: self.password_input.clear()
        self._set_field_error_state(self.email_input, False) 
        self._set_field_error_state(self.password_input, False)
        if hasattr(self, 'remember_checkbox'): self.remember_checkbox.setChecked(False)


class LoginPage(QWidget):
    process_login_request = Signal(str, str)
    signup_requested = Signal()
    project_info_signup_requested = Signal()

    def __init__(self):
        super().__init__()
        self.gradient_widget = ModernGradientWidget()
        page_layout = QHBoxLayout(self); page_layout.setContentsMargins(0,0,0,0)
        page_layout.addWidget(self.gradient_widget)

        content_layout = QHBoxLayout(self.gradient_widget)
        content_layout.setContentsMargins(40, 40, 40, 40); content_layout.setSpacing(30)

        self.features_box = FeaturesGroupBox(self.gradient_widget)
        content_layout.addWidget(self.features_box, 1)
        if hasattr(self.features_box, 'learn_more_clicked'):
            self.features_box.learn_more_clicked.connect(self.show_project_info)

        self.login_form_box = LoginGroupBox(self.gradient_widget)
        content_layout.addWidget(self.login_form_box, 1)

        self.login_form_box.login_form_submitted.connect(self.process_login_request.emit)
        self.login_form_box.signup_link_clicked.connect(self.signup_requested.emit)
        self.login_form_box.forgot_password_requested.connect(self._handle_forgot_password)

    def _handle_forgot_password(self):
        StyledAlertDialog.show_alert("Forgot Password", "Password recovery is not yet implemented.", alert_type="info", parent=self)

    def show_login_feedback(self, success, message):
        if success:
            self.login_form_box.clear_fields()
        else:
            StyledAlertDialog.show_alert("Login Failed", message, alert_type="error", parent=self)
            if self.login_form_box.password_input:
                self.login_form_box.password_input.clear()
                self.login_form_box.password_input.setFocus()
            self._set_field_error_state(self.login_form_box.email_input, True)
            self._set_field_error_state(self.login_form_box.password_input, True)


    def _set_field_error_state(self, field, has_error):
        if field:
            field.setProperty("error", has_error)
            field.style().unpolish(field)
            field.style().polish(field)

    def show_project_info(self): 
        info_dialog = ProjectInfoDialog(self)
        if hasattr(info_dialog, 'signup_action_requested'):
            info_dialog.signup_action_requested.connect(self.project_info_signup_requested.emit)
        info_dialog.exec()