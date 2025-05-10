# view/login_window.py
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox
)
from .shared_ui import ModernGradientWidget, StyledGroupBox, FeaturesGroupBox, ProjectInfoDialog

class LoginGroupBox(StyledGroupBox):
    # Signals for actions within this group box
    login_attempt = Signal(str, str) # email, password
    forgot_password_requested = Signal()
    signup_link_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()

    def setupUI(self):
        self.setStyleSheet("QGroupBox { background-color: white; border-radius: 16px; border: none; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(20)

        header = QLabel("Welcome back"); header.setStyleSheet("font-weight: 700; font-size: 24px; color: #0D47A1;")
        layout.addWidget(header)
        subtitle = QLabel("Sign in to continue"); subtitle.setStyleSheet("font-weight: 400; font-size: 16px; color: #1976D2; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        def create_input_field(label_text, placeholder, password=False):
            field_layout = QVBoxLayout(); field_layout.setSpacing(8)
            label = QLabel(label_text); label.setStyleSheet("font-weight: 500; font-size: 14px; color: #1976D2;")
            input_field = QLineEdit(); input_field.setPlaceholderText(placeholder)
            if password: input_field.setEchoMode(QLineEdit.Password)
            input_field.setStyleSheet("""
                QLineEdit { border: 1px solid #BBDEFB; border-radius: 10px; padding: 14px; font-size: 15px; background-color: #E3F2FD; }
                QLineEdit:focus { border: 2px solid #2196F3; background-color: white; }
            """)
            input_field.setMinimumHeight(48)
            field_layout.addWidget(label); field_layout.addWidget(input_field)
            return field_layout, input_field

        email_layout, self.email_input = create_input_field("Email", "Enter your email")
        layout.addLayout(email_layout)
        password_layout, self.password_input = create_input_field("Password", "Enter your password", password=True)
        layout.addLayout(password_layout)

        options_layout = QHBoxLayout()
        remember_layout = QHBoxLayout()
        remember_checkbox = QCheckBox()
        remember_checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #BBDEFB; }
            QCheckBox::indicator:checked { background-color: #2196F3; border: 1px solid #2196F3; image: url('assets/check.png'); }
        """) # Make sure 'assets/check.png' exists
        remember_text = QLabel("Remember me"); remember_text.setStyleSheet("font-weight: 400; font-size: 14px; color: #1976D2;")
        remember_layout.addWidget(remember_checkbox); remember_layout.addWidget(remember_text)

        self.forgot_password_button = QPushButton("Forgot password?")
        self.forgot_password_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 14px; font-weight: 600; border: none; text-align: right; }
            QPushButton:hover { color: #1565C0; }
        """); self.forgot_password_button.setCursor(Qt.PointingHandCursor)
        self.forgot_password_button.clicked.connect(self.forgot_password_requested.emit)

        options_layout.addLayout(remember_layout); options_layout.addStretch(); options_layout.addWidget(self.forgot_password_button)
        layout.addLayout(options_layout)
        layout.addSpacing(20)

        self.login_button = QPushButton("Sign in")
        self.login_button.setStyleSheet("""
            QPushButton { background-color: #1565C0; color: white; border-radius: 10px;
                          font-size: 16px; font-weight: 600; padding: 14px; }
            QPushButton:hover { background-color: #0D47A1; }
            QPushButton:pressed { background-color: #0A3D91; }
        """); self.login_button.setMinimumHeight(50)
        layout.addWidget(self.login_button)
        self.login_button.clicked.connect(lambda: self.login_attempt.emit(self.email_input.text(), self.password_input.text()))


        # Separator "OR" - can be re-added if social logins are implemented
        # ...

        signup_layout = QHBoxLayout(); signup_layout.setAlignment(Qt.AlignCenter)
        signup_text = QLabel("Don't have an account?"); signup_text.setStyleSheet("color: #1976D2; font-size: 14px;")
        self.signup_link_button = QPushButton("Sign up") # Renamed
        font = QFont(); font.setUnderline(True)
        self.signup_link_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 14px; font-weight: 600; border: none; }
            QPushButton:hover { color: #1565C0; }
        """); self.signup_link_button.setCursor(Qt.PointingHandCursor); self.signup_link_button.setFont(font)
        self.signup_link_button.clicked.connect(self.signup_link_clicked.emit)

        signup_layout.addWidget(signup_text); signup_layout.addWidget(self.signup_link_button)
        layout.addLayout(signup_layout)
        layout.addStretch()


class LoginPage(QWidget):
    login_successful = Signal() # Or pass user data
    signup_requested = Signal()
    project_info_signup_requested = Signal() # From dialog

    def __init__(self):
        super().__init__()
        
        self.gradient_widget = ModernGradientWidget() # This will be the page background
        page_layout = QHBoxLayout(self) # Main layout for the LoginPage
        page_layout.setContentsMargins(0,0,0,0)
        page_layout.addWidget(self.gradient_widget)

        # Content layout on top of the gradient
        content_layout = QHBoxLayout(self.gradient_widget) # Layout within gradient_widget
        content_layout.setContentsMargins(40, 40, 40, 40); content_layout.setSpacing(30)

        self.features_box = FeaturesGroupBox(self.gradient_widget)
        content_layout.addWidget(self.features_box, 1)
        self.features_box.learn_more_clicked.connect(self.show_project_info)

        self.login_form_box = LoginGroupBox(self.gradient_widget) # Renamed from login_box
        content_layout.addWidget(self.login_form_box, 1)

        # Connect signals from LoginGroupBox
        self.login_form_box.login_attempt.connect(self._handle_login_attempt)
        self.login_form_box.signup_link_clicked.connect(self.signup_requested.emit)
        # self.login_form_box.forgot_password_requested.connect(self._handle_forgot_password) # Placeholder

    def _handle_login_attempt(self, email, password):
        # --- Placeholder for actual login logic ---
        print(f"Attempting login with Email: {email}, Password: {password}")
        if email and password: # Replace with real validation
            self.login_successful.emit()
        else:
            print("Login failed: Email or password empty (example).")
            # Optionally show an error message to the user here

    def show_project_info(self):
        info_dialog = ProjectInfoDialog(self)
        info_dialog.signup_action_requested.connect(self.project_info_signup_requested.emit)
        info_dialog.exec()