# view/dashboard_window.py
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSpacerItem, QSizePolicy, QApplication, QLabel # Added QApplication, QLabel
)
import sys
import os

# Attempt to import shared_ui. This will be retried in __main__ if it fails here due to path issues.
try:
    from .shared_ui import ModernGradientWidget, LogoWidget
except ImportError:
    # Define placeholder classes if the import fails initially.
    # This allows the rest of the class definitions to be parsed without error.
    # The actual import for standalone execution is handled in the __main__ block.
    print("Initial import of shared_ui failed. Will retry if run as __main__.")
    class ModernGradientWidget(QWidget):
        def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)
    class LogoWidget(QWidget):
        def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)


class DashboardLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Re-attempt import here for when DashboardLayoutWidget is instantiated
        # This is more direct than relying on global scope if __main__ modified sys.path
        global ModernGradientWidget, LogoWidget # Make sure we're using the potentially re-imported versions
        try:
            # If running as __main__ and sys.path was fixed, this should now work
            from view.shared_ui import ModernGradientWidget as ActualModernGradientWidget
            from view.shared_ui import LogoWidget as ActualLogoWidget
            ModernGradientWidget = ActualModernGradientWidget
            LogoWidget = ActualLogoWidget
        except ImportError:
            # If still failing, the placeholders will be used, or an error will occur
            # This indicates a more fundamental path issue if not running as __main__
            # or if the __main__ path fix didn't work.
            print("Warning: Failed to import actual shared_ui components in DashboardLayoutWidget init.")
            # Fallback to placeholder if absolutely necessary, though ideally the path fix works
            if 'ActualModernGradientWidget' not in globals():
                class ModernGradientWidget(QWidget): pass
                class LogoWidget(QWidget): pass


        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sidebar
        self.sidebar_widget = ModernGradientWidget()
        self.sidebar_widget.setFixedWidth(220)

        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(15)

        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.logo_widget_sidebar = LogoWidget()
        self.sidebar_layout.addWidget(self.logo_widget_sidebar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        sidebar_buttons_data = [
            ("Dashbord", "Dashboard"),
            ("Product", "Product"),
            ("Sales", "Sales"),
            ("Goals", "Goals"),
            ("History", "History"),
            ("Notifications", "Notifications"),
            ("Profile", "Profile"),
            ("Setting", "Settings"),
            ("Log out", "Log Out")
        ]

        for i, (icon_name, button_text) in enumerate(sidebar_buttons_data):
            button = QPushButton(f"  {button_text}")
            button.setIconSize(QSize(20, 20))
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 10px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    border-radius: 5px;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.25);
                }
            """)

            # Determine asset base path
            asset_base_path = "assets" # Default for when imported by main.py
            if __name__ == "__main__" or not hasattr(sys, 'frozen'): # If run standalone or not frozen by PyInstaller
                # Construct path relative to this file's location for standalone
                try:
                    # This assumes 'assets' is in the parent directory of 'view'
                    current_file_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root_dir = os.path.dirname(current_file_dir)
                    asset_base_path = os.path.join(project_root_dir, "assets")
                except NameError: # __file__ might not be defined in some contexts
                    pass # Fallback to "assets"

            icon_path = os.path.join(asset_base_path, f"{icon_name}.png")

            if os.path.exists(icon_path):
                button.setIcon(QIcon(icon_path))
            else:
                print(f"Warning: Icon not found at {icon_path}")

            self.sidebar_layout.addWidget(button)

            if button_text == "Notifications":
                self.sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.sidebar_layout.addStretch(1)

        # Content Area
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #f4f6f8;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget, 1)


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track App - Dashboard")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_window_layout = QVBoxLayout(self.central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.setSpacing(0)

        self.layout_content = DashboardLayoutWidget()
        main_window_layout.addWidget(self.layout_content)


if __name__ == "__main__":
    # Modify sys.path to allow finding the 'view' package and its modules
    # when this script is run directly.
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_dir = os.path.dirname(current_file_dir) # This should be your_project_root

    if project_root_dir not in sys.path:
        sys.path.insert(0, project_root_dir)

    # Now, attempt to re-import shared_ui components with the corrected path.
    # This is necessary because the class-level imports might have failed.
    try:
        from view.shared_ui import ModernGradientWidget as ActualModernGradientWidget
        from view.shared_ui import LogoWidget as ActualLogoWidget
        # Make these available globally within this script for the classes to use
        ModernGradientWidget = ActualModernGradientWidget
        LogoWidget = ActualLogoWidget
        print("Successfully re-imported shared_ui components for standalone execution.")
    except ImportError as e:
        print(f"Critical Error: Could not import shared_ui components even after path modification: {e}")
        print("Please ensure 'shared_ui.py' exists in the 'view' directory and the project structure is correct.")
        # Define very basic fallbacks so the QApplication can at least try to start
        class ModernGradientWidget(QWidget): pass
        class LogoWidget(QWidget): pass
        # sys.exit(1) # Optionally exit if shared_ui is absolutely critical

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    default_font = QFont("Segoe UI", 10) # Renamed to avoid conflict with QFont class
    app.setFont(default_font)

    window = DashboardWindow() # This will now use the (potentially) re-imported shared components

    # Example: Add content to dashboard for testing
    test_label = QLabel("Dashboard Content Placeholder")
    test_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    test_label.setStyleSheet("font-size: 24px; color: #333;")
    window.layout_content.content_layout.addWidget(test_label)

    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())