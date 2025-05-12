# controller/user_controller.py
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer # Slot removed as not strictly needed for these connections

# View imports
from view.welcome_window import WelcomePage
from view.login_window import LoginPage
from view.signup_window import SignupPage
from view.dashboard_window import DashboardWindow

# Model and Processing imports
from model.user_database_manager import UserDatabaseManager # <<< UPDATED IMPORT
from processing.user_processing import UserProcessor
# Product related imports are not directly used by UserController anymore

class UserController:
    def __init__(self, app_shell):
        self.app_shell = app_shell
        self.stacked_widget = app_shell.stacked_widget
        self.dashboard_win = None
        self.current_user_data = None

        # --- Initialize User Database Manager and User Processor ---
        self.user_db_manager = UserDatabaseManager() # <<< INSTANTIATE UserDatabaseManager
        self.user_processor = UserProcessor(self.user_db_manager) # Pass it here

        if QApplication.instance():
             QApplication.instance().user_controller = self

        self.welcome_page = WelcomePage()
        self.login_page = LoginPage()
        self.signup_page = SignupPage()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.signup_page)

        # Style storage (defensive coding)
        if hasattr(self.welcome_page, 'content_card') and \
           hasattr(self.welcome_page.content_card, 'login_button') and \
           hasattr(self.welcome_page.content_card, 'signup_button'):
            self.original_welcome_login_btn_style = self.welcome_page.content_card.login_button.styleSheet()
            self.original_welcome_signup_btn_style = self.welcome_page.content_card.signup_button.styleSheet()
        else:
            self.original_welcome_login_btn_style = ""
            self.original_welcome_signup_btn_style = ""

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
        # ... (same as before) ...
        if not original_style: temp_style = f"background-color: {temp_bg_color_hex};"
        else: temp_style = original_style + f" background-color: {temp_bg_color_hex};"
        button.setStyleSheet(temp_style)
        QTimer.singleShot(200, lambda: button.setStyleSheet(original_style if original_style else ""))


    def show_welcome_page(self):
        # ... (same as before) ...
        self.stacked_widget.setCurrentWidget(self.welcome_page)
        self.app_shell.setWindowTitle("Track App - Welcome")


    def show_login_page(self, email_to_prefill=None):
        # ... (same as before, with defensive checks) ...
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card') and hasattr(self.welcome_page.content_card, 'login_button'):
             self._animate_button_click(self.welcome_page.content_card.login_button, self.original_welcome_login_btn_style, "#0052A3")
        elif self.stacked_widget.currentWidget() == self.signup_page:
            if hasattr(self.login_page, 'login_form_box') and hasattr(self.login_page.login_form_box, 'clear_fields'): self.login_page.login_form_box.clear_fields()
        if email_to_prefill and hasattr(self.login_page, 'login_form_box') and hasattr(self.login_page.login_form_box, 'email_input'):
            self.login_page.login_form_box.email_input.setText(email_to_prefill)
            if hasattr(self.login_page.login_form_box, 'password_input'): self.login_page.login_form_box.password_input.setFocus()
        elif hasattr(self.login_page, 'login_form_box') and hasattr(self.login_page.login_form_box, 'email_input'): self.login_page.login_form_box.email_input.setFocus()
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        self.app_shell.setWindowTitle("Track App - Login")


    def show_signup_page(self):
        # ... (same as before, with defensive checks) ...
        if self.stacked_widget.currentWidget() == self.welcome_page and hasattr(self.welcome_page, 'content_card') and hasattr(self.welcome_page.content_card, 'signup_button'):
            self._animate_button_click(self.welcome_page.content_card.signup_button, self.original_welcome_signup_btn_style, "#e0e0e0")
        if hasattr(self.signup_page, 'signup_form_box') and hasattr(self.signup_page.signup_form_box, 'clear_fields'): self.signup_page.signup_form_box.clear_fields()
        QTimer.singleShot(100, lambda: self.stacked_widget.setCurrentWidget(self.signup_page))
        self.app_shell.setWindowTitle("Track App - Sign Up")


    def handle_signup_attempt(self, name, email, password):
        print(f"[UserController] Signup attempt: Name='{name}', Email='{email}'")
        success, message = self.user_processor.register_new_user(name, email, password)
        self.signup_page.show_signup_feedback(success, message)

    def handle_login_attempt(self, email, password):
        print(f"[UserController] Login attempt: Email='{email}'")
        success, message, user_data = self.user_processor.authenticate_user(email, password)
        if success:
            self.current_user_data = user_data
            print(f"Login successful for user: {self.current_user_data['name']} (ID: {self.current_user_data['id']})")
            self.show_dashboard_window()
        else:
            print(f"Login failed: {message}")
            self.login_page.show_login_feedback(False, message)

    def show_dashboard_window(self):
        if not self.current_user_data:
            print("Error: No user logged in. Cannot show dashboard.")
            self.show_login_page()
            return

        print(f"Transitioning to Dashboard for user: {self.current_user_data['name']}")
        if not self.dashboard_win:
            # DashboardWindow now needs the main_db_manager_instance (for user DB related things, if any,
            # or for its ProductDatabaseManager to be distinct).
            # And user_data to know who is logged in.
            self.dashboard_win = DashboardWindow(user_data=self.current_user_data,
                                                 main_db_manager_instance=self.user_db_manager) # Pass the UserDatabaseManager
            if hasattr(self.dashboard_win, 'app_logout_requested'):
                self.dashboard_win.app_logout_requested.connect(self.handle_app_logout)
        elif hasattr(self.dashboard_win, 'set_user_info'):
            self.dashboard_win.set_user_info(self.current_user_data)

        self.dashboard_win.resize(self.app_shell.width(), self.app_shell.height())
        self.dashboard_win.move(self.app_shell.pos())
        self.dashboard_win.show()
        self.app_shell.close()

    def handle_app_logout(self):
        print("[UserController] Logout requested from dashboard.")
        self.current_user_data = None
        if self.dashboard_win:
            self.dashboard_win.close() # DashboardWindow's closeEvent will handle its ProductDBManager
            self.dashboard_win = None
        if self.app_shell:
            self.app_shell.show()
            self.show_login_page()
        else: # Should not happen if app_shell is properly managed
            print("CRITICAL: AppShell not available for logout.")
            QApplication.quit()


    def close_db_connection(self): # Closes the UserDatabaseManager connection
        if self.user_db_manager:
            self.user_db_manager.close_connection()