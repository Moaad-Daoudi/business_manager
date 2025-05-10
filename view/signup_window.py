# view/signup_window.py
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QLineEdit, QFrame, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox
)
from .shared_ui import ModernGradientWidget, StyledGroupBox, FeaturesGroupBox, ProjectInfoDialog

class SignupGroupBox(StyledGroupBox):
    signup_attempt = Signal(str, str, str) # name, email, password
    login_link_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()

    def setupUI(self):
        self.setStyleSheet("QGroupBox { background-color: white; border-radius: 16px; border: none; }")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40); layout.setSpacing(20)

        header = QLabel("Sign up for free to track your product")
        header.setStyleSheet("font-weight: 700; font-size: 24px; color: #0D47A1;")
        layout.addWidget(header)
        subtitle = QLabel("Access all features for free")
        subtitle.setStyleSheet("font-weight: 400; font-size: 16px; color: #1976D2; margin-bottom: 10px;")
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

        name_layout, self.name_input = create_input_field("What should we call you?", "Enter your name")
        layout.addLayout(name_layout)
        email_layout, self.email_input = create_input_field("What's your email?", "Enter your email")
        layout.addLayout(email_layout)
        password_layout, self.password_input = create_input_field("Create a password", "Enter your password", password=True)
        layout.addLayout(password_layout)

        password_hint = QLabel("Use 8 or more characters with a mix of letters, numbers & symbols")
        password_hint.setStyleSheet("font-weight: 400; font-size: 13px; color: #1976D2;")
        layout.addWidget(password_hint)

        terms_layout = QHBoxLayout()
        self.terms_checkbox = QCheckBox() # Make accessible if needed for validation
        self.terms_checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 18px; height: 18px; border-radius: 4px; border: 1px solid #BBDEFB; }
            QCheckBox::indicator:checked { background-color: #2196F3; border: 1px solid #2196F3; image: url('assets/check.png'); }
        """) # Make sure 'assets/check.png' exists
        terms_text = QLabel("By creating an account, you agree to the Terms of use and Privacy Policy.")
        terms_text.setStyleSheet("font-weight: 400; font-size: 14px; color: #1976D2;"); terms_text.setWordWrap(True)
        terms_layout.addWidget(self.terms_checkbox); terms_layout.addWidget(terms_text, 1)
        layout.addLayout(terms_layout)
        layout.addSpacing(10)

        self.signup_button = QPushButton("Create an account")
        self.signup_button.setStyleSheet("""
            QPushButton { background-color: #1565C0; color: white; border-radius: 10px;
                          font-size: 16px; font-weight: 600; padding: 14px; }
            QPushButton:hover { background-color: #0D47A1; }
            QPushButton:pressed { background-color: #0A3D91; }
        """); self.signup_button.setMinimumHeight(50)
        layout.addWidget(self.signup_button)
        self.signup_button.clicked.connect(lambda: self.signup_attempt.emit(
            self.name_input.text(), self.email_input.text(), self.password_input.text()
        ))


        login_layout = QHBoxLayout(); login_layout.setAlignment(Qt.AlignCenter)
        login_text = QLabel("Already have an account?"); login_text.setStyleSheet("color: #1976D2; font-size: 14px;")
        self.login_link_button = QPushButton("Login") # Renamed
        font = QFont(); font.setUnderline(True)
        self.login_link_button.setStyleSheet("""
            QPushButton { background: transparent; color: #2196F3; font-size: 14px; font-weight: 600; border: none; }
            QPushButton:hover { color: #1565C0; }
        """); self.login_link_button.setCursor(Qt.PointingHandCursor); self.login_link_button.setFont(font)
        self.login_link_button.clicked.connect(self.login_link_clicked.emit)

        login_layout.addWidget(login_text); login_layout.addWidget(self.login_link_button)
        layout.addLayout(login_layout)
        layout.addStretch()


class SignupPage(QWidget):
    signup_successful = Signal() # Or pass user data
    login_requested = Signal()
    project_info_signup_requested = Signal() # From dialog (though unlikely to be used here)

    def __init__(self):
        super().__init__()

        self.gradient_widget = ModernGradientWidget() # Page background
        page_layout = QHBoxLayout(self)
        page_layout.setContentsMargins(0,0,0,0)
        page_layout.addWidget(self.gradient_widget)

        content_layout = QHBoxLayout(self.gradient_widget)
        content_layout.setContentsMargins(40, 40, 40, 40); content_layout.setSpacing(30)

        self.features_box = FeaturesGroupBox(self.gradient_widget)
        content_layout.addWidget(self.features_box, 1)
        self.features_box.learn_more_clicked.connect(self.show_project_info)

        self.signup_form_box = SignupGroupBox(self.gradient_widget) # Renamed from signup_box
        content_layout.addWidget(self.signup_form_box, 1)

        # Connect signals from SignupGroupBox
        self.signup_form_box.signup_attempt.connect(self._handle_signup_attempt)
        self.signup_form_box.login_link_clicked.connect(self.login_requested.emit)

    def _handle_signup_attempt(self, name, email, password):
        # --- Placeholder for actual signup logic ---
        print(f"Attempting signup with Name: {name}, Email: {email}, Password: {password}")
        if name and email and password and self.signup_form_box.terms_checkbox.isChecked(): # Basic validation
            print("Signup successful (placeholder).")
            self.signup_successful.emit()
        else:
            if not self.signup_form_box.terms_checkbox.isChecked():
                 print("Signup failed: Terms not accepted.")
            else:
                 print("Signup failed: Missing information (example).")
            # Optionally show an error message

    def show_project_info(self):
        info_dialog = ProjectInfoDialog(self)
        # This signal connection is here for completeness but might not be strictly
        # necessary on the signup page if the dialog's signup button leads to the same action.
        info_dialog.signup_action_requested.connect(self.project_info_signup_requested.emit)
        info_dialog.exec()