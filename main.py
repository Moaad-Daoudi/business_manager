# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtGui import QFont, QGuiApplication # QGuiApplication for screen info
import sys

from controller.user_controller import UserController

APP_WIDTH = 1200
APP_HEIGHT = 800

class AppShell(QMainWindow): # This is the main window for the auth pages
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

    def closeEvent(self, event):
        # Try to access UserController and close its DB (UserDatabaseManager)
        # DashboardWindow handles its own ProductDatabaseManager closure
        controller_instance = getattr(QApplication.instance(), 'user_controller', None)
        if controller_instance and hasattr(controller_instance, 'close_db_connection'):
            print("[AppShell closeEvent] Closing User DB connection via UserController.")
            controller_instance.close_db_connection()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyle("Fusion")

    shell = AppShell()
    user_controller = UserController(shell) # UserController now manages the auth flow
    # Store user_controller on app instance if AppShell's closeEvent needs it
    # This was already done inside UserController.__init__

    user_controller.start_app()

    exit_code = app.exec()

    # Fallback DB close for user_database.db if AppShell's closeEvent didn't trigger
    if hasattr(user_controller, 'close_db_connection'):
         print("[main exit] Closing User DB connection via UserController as fallback.")
         user_controller.close_db_connection()
    return exit_code

if __name__ == "__main__":
    sys.exit(main())