from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from view.welcome_window import WelcomeWindow
from view.login_window import LoginWindow
from view.signup_window import SignupWindow
import sys

class MainController:
    def __init__(self):
        self.welcome_window = WelcomeWindow()
        self.login_window = LoginWindow()
        self.signup_window = SignupWindow()  
        self.welcome_window.content.login.clicked.connect(self.show_login)
        self.welcome_window.content.register.clicked.connect(self.show_register)
        
    def show_welcome(self):
        self.welcome_window.show()
        
    def show_login(self):
        self.welcome_window.content.login.setStyleSheet(
            self.welcome_window.content.login.styleSheet() + "background-color: #0052A3;"
        )
        QTimer.singleShot(200, self.reset_login_style)
        self.login_window.show()
        self.welcome_window.close()
    def reset_login_style(self):
        self.welcome_window.content.login.setStyleSheet(
            self.welcome_window.content.login.styleSheet().replace("background-color: #0052A3;", "")
        )
        
    def show_register(self):
        self.welcome_window.content.register.setStyleSheet(
            self.welcome_window.content.register.styleSheet() + "background-color: #f2f2f2;"
        )
        QTimer.singleShot(200, self.reset_register_style)
        self.signup_window.show()  
        self.welcome_window.close()
    def reset_register_style(self):
        self.welcome_window.content.register.setStyleSheet(
            self.welcome_window.content.register.styleSheet().replace("background-color: #f2f2f2;", "")
        )

def main():
    app = QApplication(sys.argv)
    controller = MainController()
    controller.show_welcome()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())