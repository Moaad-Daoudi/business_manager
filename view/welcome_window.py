# view/welcome_window.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from .shared_ui import RoundedButton, RoundedWidget, BackgroundWidget, LogoWidget

class ContentWidget(RoundedWidget): # The central card on the welcome page
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 600) # Fixed size for the card itself

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40); self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)

        self.logo = LogoWidget()
        logo_layout = QVBoxLayout(); logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.logo)
        self.layout.addLayout(logo_layout); self.layout.addSpacing(10)

        self.title_label = QLabel("Track App", self) # Renamed from label
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-family: 'Arial'; font-size: 38px; font-weight: bold; color: #0066CC; margin-bottom: 10px;")
        self.layout.addWidget(self.title_label)

        self.description_label = QLabel( # Renamed from label2
            "Welcome to our tracking application. Manage your tasks, track your progress and "
            "achieve your goals with our intuitive interface.", self)
        self.description_label.setAlignment(Qt.AlignCenter); self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("font-family: 'Arial'; font-size: 16px; color: #555555; margin-bottom: 20px; line-height: 150%;")
        self.layout.addWidget(self.description_label)
        self.layout.addSpacing(40)

        self.login_button = RoundedButton("Login", self, primary=True) # Renamed from login
        self.layout.addWidget(self.login_button)
        self.layout.addSpacing(15)
        self.signup_button = RoundedButton("Sign up", self) # Renamed from register
        self.layout.addWidget(self.signup_button)

        self.layout.addStretch()
        self.version_label = QLabel("Version 1.0.1", self)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet("font-family: 'Arial'; font-size: 12px; color: #777777; margin-top: 20px;")
        self.layout.addWidget(self.version_label)


class WelcomePage(QWidget):
    login_requested = Signal()
    signup_requested = Signal()

    def __init__(self):
        super().__init__()
        
        page_layout = QVBoxLayout(self) # Main layout for the WelcomePage
        page_layout.setContentsMargins(0,0,0,0)

        self.background_widget = BackgroundWidget() # The gradient background
        page_layout.addWidget(self.background_widget)
        
        # The content card (logo, text, buttons)
        self.content_card = ContentWidget()
        # Add the content card to the background_widget's layout (which centers it)
        self.background_widget.layout.addWidget(self.content_card)

        # Connect buttons from the content card to the page's signals
        self.content_card.login_button.clicked.connect(self.login_requested.emit)
        self.content_card.signup_button.clicked.connect(self.signup_requested.emit)