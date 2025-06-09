# controller/user_controller.py
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer 
import sys # <-- Import sys to allow exiting the app

from view.welcome_window import WelcomePage
from view.login_window import LoginPage
from view.signup_window import SignupPage
from view.dashboard_window import DashboardWindow

from model.database_manager import DatabaseManager
from processing.user_processing import UserProcessor

class UserController:
    def __init__(self, app_shell):
        self.app_shell = app_shell
        
        try:
            self.db_manager = DatabaseManager()
            self.user_processor = UserProcessor(self.db_manager)
        except ConnectionError as e:
            QMessageBox.critical(
                None, 
                "Fatal Error", 
                f"A critical error occurred while initializing the database:\n\n{e}\n\nThe application cannot continue and will now close."
            )
            sys.exit(1)

        self.stacked_widget = app_shell.stacked_widget
        self.dashboard_win = None
        self.current_user_data = None

        if QApplication.instance():
             QApplication.instance().user_controller = self

        self.welcome_page = WelcomePage()
        self.login_page = LoginPage()
        self.signup_page = SignupPage()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        if hasattr(self.welcome_page, 'content_card'):
            self.original_welcome_login_btn_style = self.welcome_page.content_card.login_button.styleSheet()
            self.original_welcome_signup_btn_style = self.welcome_page.content_card.signup_button.styleSheet()

        self._connect_signals()

    def _connect_signals(self):
        self.welcome_page.login_requested.connect(lambda: self.show_login_page())
        self.welcome_page.signup_requested.connect(self.show_signup_page)
        self.login_page.process_login_request.connect(self.handle_login_attempt)
        self.login_page.signup_requested.connect(self.show_signup_page)
        if hasattr(self.login_page, 'project_info_signup_requested'):
            self.login_page.project_info_signup_requested.connect(self.show_signup_page)
        self.signup_page.process_signup_request.connect(self.handle_signup_attempt)
        self.signup_page.login_requested.connect(self.show_login_page)

    def start_app(self):
        self.show_welcome_page()
        self.app_shell.show()

    def _animate_button_click(self, button, original_style, temp_bg_color_hex):
        temp_style = (original_style or "") + f" background-color: {temp_bg_color_hex};"
        button.setStyleSheet(temp_style)
        QTimer.singleShot(200, lambda: button.setStyleSheet(original_style or ""))

    def show_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.app_shell.setWindowTitle("Track App - Welcome")

    def show_login_page(self, email_to_prefill=None):
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card'):
             self._animate_button_click(self.welcome_page.content_card.login_button, self.original_welcome_login_btn_style, "#0052A3")
        elif self.stacked_widget.currentWidget() == self.signup_page:
            if hasattr(self.login_page, 'login_form_box'): self.login_page.login_form_box.clear_fields()
        if email_to_prefill and hasattr(self.login_page, 'login_form_box'):
            self.login_page.login_form_box.email_input.setText(email_to_prefill)
            if hasattr(self.login_page.login_form_box, 'password_input'): self.login_page.login_form_box.password_input.setFocus()
        elif hasattr(self.login_page, 'login_form_box'): self.login_page.login_form_box.email_input.setFocus()
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        self.app_shell.setWindowTitle("Track App - Login")

    def show_signup_page(self):
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card'):
            self._animate_button_click(self.welcome_page.content_card.signup_button, self.original_welcome_signup_btn_style, "#e0e0e0")
        if hasattr(self.signup_page, 'signup_form_box'): self.signup_page.signup_form_box.clear_fields()
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.signup_page))
        self.app_shell.setWindowTitle("Track App - Sign Up")
    
    def handle_signup_attempt(self, name, email, password):
        success, message = self.user_processor.register_new_user(name, email, password)
        self.signup_page.show_signup_feedback(success, message)

    def handle_login_attempt(self, email, password):
        success, message, user_data = self.user_processor.authenticate_user(email, password)
        if success:
            self.current_user_data = user_data
            self.show_dashboard_window()
        else:
            self.login_page.show_login_feedback(False, message)

    def show_dashboard_window(self):
        if not self.current_user_data:
            self.show_login_page()
            return
        if not self.dashboard_win:
            self.dashboard_win = DashboardWindow(user_data=self.current_user_data, db_manager_instance=self.db_manager)
            if hasattr(self.dashboard_win, 'app_logout_requested'):
                self.dashboard_win.app_logout_requested.connect(self.handle_app_logout)
        elif hasattr(self.dashboard_win, 'set_user_info'):
            self.dashboard_win.set_user_info(self.current_user_data)
        self.dashboard_win.resize(self.app_shell.width(), self.app_shell.height())
        self.dashboard_win.move(self.app_shell.pos())
        self.dashboard_win.show()
        # --- FIX: Change close() to hide() ---
        # This keeps the AppShell (and its DB connection) alive in the background
        self.app_shell.hide() 

    def handle_app_logout(self):
        self.current_user_data = None
        if self.dashboard_win:
            self.dashboard_win.close()
            self.dashboard_win = None
        if self.app_shell:
            # This logic correctly shows the shell again
            self.app_shell.show()
            self.show_login_page()
        else:
            QApplication.quit()
            
    def close_db_connection(self):
        if self.db_manager:
            self.db_manager.close_connection()