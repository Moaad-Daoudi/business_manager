# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import QTimer, Signal, QSize
from PySide6.QtGui import QFont, QGuiApplication
import sys

# Import page widgets
from view.welcome_window import WelcomePage
from view.login_window import LoginPage
from view.signup_window import SignupPage
from view.dashboard_window import DashboardWindow

# Import Database Manager
from model.database_manager import DatabaseManager

APP_WIDTH = 1200
APP_HEIGHT = 800

class AppShell(QMainWindow): # Main application window for auth flow
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track App")
        self.resize(APP_WIDTH, APP_HEIGHT)
        self.setMinimumSize(int(APP_WIDTH * 0.8), int(APP_HEIGHT * 0.75))

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

    def closeEvent(self, event): # Ensure DB connection is closed
        if hasattr(QApplication.instance(), 'controller') and \
           hasattr(QApplication.instance().controller, 'db_manager'):
            QApplication.instance().controller.db_manager.close_connection()
        super().closeEvent(event)


class MainController:
    def __init__(self, app_shell):
        self.app_shell = app_shell
        self.stacked_widget = app_shell.stacked_widget
        self.dashboard_win = None

        self.db_manager = DatabaseManager()
        QApplication.instance().controller = self

        self.welcome_page = WelcomePage()
        self.login_page = LoginPage()
        self.signup_page = SignupPage()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        if hasattr(self.welcome_page, 'content_card'): # Check if content_card exists
            self.original_welcome_login_btn_style = self.welcome_page.content_card.login_button.styleSheet()
            self.original_welcome_signup_btn_style = self.welcome_page.content_card.signup_button.styleSheet()
        else: # Fallback if structure is different or not yet fully initialized
            self.original_welcome_login_btn_style = ""
            self.original_welcome_signup_btn_style = ""


        # --- Connect signals from pages ---
        self.welcome_page.login_requested.connect(self.show_login_page)
        self.welcome_page.signup_requested.connect(self.show_signup_page)

        # Login Page Connections
        self.login_page.signup_requested.connect(self.show_signup_page)
        # REMOVED: self.login_page.login_successful.connect(self.show_dashboard_window)
        self.login_page.process_login_request.connect(self.handle_login_processing) # Correct connection for login data
        self.login_page.project_info_signup_requested.connect(self.show_signup_page)

        # Signup Page Connections
        self.signup_page.login_requested.connect(self.show_login_page)
        self.signup_page.process_signup_request.connect(self.handle_signup_processing)


    def start(self):
        self.show_welcome_page()
        self.app_shell.show()

    def _animate_button_click(self, button, original_style, temp_bg_color_hex):
        # Ensure original_style is not empty before trying to concatenate
        if not original_style:
            temp_style = f"background-color: {temp_bg_color_hex};"
        else:
            temp_style = original_style + f" background-color: {temp_bg_color_hex};"
        button.setStyleSheet(temp_style)
        QTimer.singleShot(200, lambda: button.setStyleSheet(original_style if original_style else ""))


    def show_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.app_shell.setWindowTitle("Track App - Welcome")

    def show_login_page(self):
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card'):
             self._animate_button_click(
                 self.welcome_page.content_card.login_button,
                 self.original_welcome_login_btn_style, "#0052A3"
            )
        elif self.stacked_widget.currentWidget() == self.signup_page:
            if hasattr(self.login_page, 'login_form_box') and hasattr(self.login_page.login_form_box, 'clear_fields'):
                self.login_page.login_form_box.clear_fields()
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        self.app_shell.setWindowTitle("Track App - Login")

    def show_signup_page(self):
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card'):
            self._animate_button_click(
                self.welcome_page.content_card.signup_button,
                self.original_welcome_signup_btn_style, "#e0e0e0"
            )
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.signup_page))
        self.app_shell.setWindowTitle("Track App - Sign Up")

    def handle_signup_processing(self, name, email, password):
        print(f"Controller received signup request: {name}, {email}")
        success, message = self.db_manager.add_user(name, email, password)
        self.signup_page.show_signup_feedback(success, message)

    def handle_login_processing(self, email, password): # This method processes login
        print(f"Controller received login request for email: {email}")
        user = self.db_manager.get_user_by_email(email)

        if user:
            if self.db_manager.verify_password(user["password_hash"], password):
                print(f"Login successful for user: {user['name']}")
                # Call show_dashboard_window directly upon successful authentication
                self.show_dashboard_window(user) # Pass user data
            else:
                print("Login failed: Invalid password.")
                self.login_page.show_login_feedback(False, "Invalid email or password.")
        else:
            print("Login failed: User not found.")
            self.login_page.show_login_feedback(False, "Invalid email or password.") # Generic message

    def show_dashboard_window(self, user_data=None): # Renamed from original, now accepts user_data
        print(f"Authentication successful, preparing to show DashboardWindow for user: {user_data.get('name') if user_data else 'Unknown'}")
        if not self.dashboard_win:
            self.dashboard_win = DashboardWindow()

        if user_data:
            self.dashboard_win.setWindowTitle(f"Track App - Dashboard ({user_data.get('name')})")
            # You could also pass user_data to a method within DashboardWindow if it needs more info
            # e.g., if hasattr(self.dashboard_win, 'load_user_data'): self.dashboard_win.load_user_data(user_data)

        self.dashboard_win.resize(self.app_shell.width(), self.app_shell.height())
        self.dashboard_win.move(self.app_shell.pos())
        self.dashboard_win.show()
        self.app_shell.close() # This will trigger AppShell's closeEvent

def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyle("Fusion")

    shell = AppShell()
    controller = MainController(shell)
    controller.start()
    exit_code = app.exec()
    if hasattr(controller, 'db_manager') and controller.db_manager:
        print("Closing DB connection from main exit.")
        controller.db_manager.close_connection()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())