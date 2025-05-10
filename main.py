# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import QTimer, Signal, QSize
from PySide6.QtGui import QFont, QGuiApplication
import sys

# Import page widgets
from view.welcome_window import WelcomePage
from view.login_window import LoginPage
from view.signup_window import SignupPage
from view.dashboard_window import DashboardWindow

APP_WIDTH = 1200
APP_HEIGHT = 800

class AppShell(QMainWindow): # Main application window for auth flow
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track App")
        # Set fixed size for the authentication flow for consistency
        self.resize(APP_WIDTH, APP_HEIGHT)
        self.setMinimumSize(960, 700)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.center_on_screen()

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

class MainController:
    def __init__(self, app_shell):
        self.app_shell = app_shell
        self.stacked_widget = app_shell.stacked_widget
        self.dashboard_win = None # To hold the dashboard window instance

        self.welcome_page = WelcomePage()
        self.login_page = LoginPage()
        self.signup_page = SignupPage()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        # Store original styles for welcome page buttons (if needed for complex animations)
        # For simple color change, direct manipulation in show_xxx_page is fine.
        self.original_welcome_login_btn_style = self.welcome_page.content_card.login_button.styleSheet()
        self.original_welcome_signup_btn_style = self.welcome_page.content_card.signup_button.styleSheet()


        # --- Connect signals from pages ---
        self.welcome_page.login_requested.connect(self.show_login_page)
        self.welcome_page.signup_requested.connect(self.show_signup_page)

        self.login_page.signup_requested.connect(self.show_signup_page)
        self.login_page.login_successful.connect(self.show_dashboard_window)
        self.login_page.project_info_signup_requested.connect(self.show_signup_page) # From dialog on login page

        self.signup_page.login_requested.connect(self.show_login_page)
        self.signup_page.signup_successful.connect(self.show_login_page) # e.g., go to login after signup
        # self.signup_page.project_info_signup_requested.connect(self.show_signup_page) # Dialog on signup page likely leads to signup itself


    def start(self):
        self.show_welcome_page()
        self.app_shell.show()

    def _animate_button_click(self, button, original_style, temp_bg_color_hex):
        """Simple button click visual feedback."""
        current_style = button.styleSheet() # Get current complete stylesheet
        # Find the base background-color to replace or append
        if "background-color:" in original_style:
             # Attempt to replace existing, might be complex if multiple bg-colors are used
             # For robust solution, parse stylesheet or use specific properties if available
             temp_style = original_style.replace(
                 original_style.split("background-color:")[1].split(";")[0],
                 f" {temp_bg_color_hex}"
             )
        else:
            temp_style = original_style + f" background-color: {temp_bg_color_hex};"

        button.setStyleSheet(temp_style)
        QTimer.singleShot(200, lambda: button.setStyleSheet(original_style))


    def show_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.app_shell.setWindowTitle("Track App - Welcome")

    def show_login_page(self):
        # Animate the button on welcome_page if it was the source
        if self.stacked_widget.currentWidget() == self.welcome_page:
             self._animate_button_click(
                 self.welcome_page.content_card.login_button,
                 self.original_welcome_login_btn_style,
                 "#0052A3" # Click color for primary button
            )
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.login_page)) # Slight delay for animation
        self.app_shell.setWindowTitle("Track App - Login")


    def show_signup_page(self):
        if self.stacked_widget.currentWidget() == self.welcome_page:
            self._animate_button_click(
                self.welcome_page.content_card.signup_button,
                self.original_welcome_signup_btn_style,
                "#e0e0e0" # Click color for secondary button
            )
        elif self.stacked_widget.currentWidget() == self.login_page:
            # Potentially animate the "Sign up" link on the login page if needed
            pass
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.signup_page))
        self.app_shell.setWindowTitle("Track App - Sign Up")

    def show_dashboard_window(self):
        print("Authentication successful, showing DashboardWindow...")
        if not self.dashboard_win: # Create only if it doesn't exist
            self.dashboard_win = DashboardWindow()

        # Match the size of the auth shell or use a default dashboard size
        self.dashboard_win.resize(self.app_shell.width(), self.app_shell.height())
        self.dashboard_win.move(self.app_shell.pos()) # Move to the same position
        
        self.dashboard_win.show()
        self.app_shell.close() # Close the authentication shell


def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10) # Global font
    app.setFont(font)
    app.setStyle("Fusion") # Global style

    shell = AppShell()
    controller = MainController(shell)
    controller.start()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())