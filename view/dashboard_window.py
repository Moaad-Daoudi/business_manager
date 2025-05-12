# view/dashboard_window.py
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSpacerItem, QSizePolicy, QStackedWidget, QApplication, QLabel # Added QLabel
)
import sys
import os

# --- Attempt to import dependencies ---
# Shared UI
try:
    from .shared_ui import ModernGradientWidget, LogoWidget
except ImportError:
    print("Warning: Dashboard - Could not import shared_ui. Using placeholders.")
    class ModernGradientWidget(QWidget):
        def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)
    class LogoWidget(QWidget):
        def __init__(self, *args, **kwargs): super().__init__(*args, **kwargs)

# Base Page and Specific Page Views
try:
    from .base_dashboard_page import BaseDashboardPage
    from .dashboard_home_page import DashboardHomePage
    from .product_page import ProductPage
    from .sales_page import SalesPage
    from .goals_page import GoalsPage
    from .history_page import HistoryPage
    from .notifications_page import NotificationsPage
    from .profile_page import ProfilePage
    from .settings_page import SettingsPage
except ImportError as e:
    print(f"Warning: Dashboard - Could not import one or more page views: {e}. Using placeholders.")
    class BaseDashboardPage(QWidget): # Basic placeholder for BaseDashboardPage
        def __init__(self, title="Page Title", parent=None):
            super().__init__(parent)
            self.title_label = QLabel(title, self) # Keep a title label at least
            self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.content_layout = QVBoxLayout(self) # Add content_layout attribute
            self.content_layout.addWidget(self.title_label)
        def load_page_data(self): print(f"Placeholder load: {self.title_label.text()}")
        def unload_page_data(self): print(f"Placeholder unload: {self.title_label.text()}")

    _PAGES_TO_PLACEHOLD = {
        "DashboardHomePage": "Dashboard Home", "ProductPage": "Products", "SalesPage": "Sales",
        "GoalsPage": "Goals", "HistoryPage": "History", "NotificationsPage": "Notifications",
        "ProfilePage": "Profile", "SettingsPage": "Settings"
    }
    for _class_name, _title in _PAGES_TO_PLACEHOLD.items():
        if _class_name not in globals():
            if _class_name == "ProductPage": # ProductPage expects specific args
                globals()[_class_name] = type(_class_name, (BaseDashboardPage,), {
                    "__init__": lambda self, owner_username, product_processor, parent=None, title=_title: \
                                  BaseDashboardPage.__init__(self, title, parent)
                })
            else: # Other pages might have simpler constructors for placeholder
                globals()[_class_name] = type(_class_name, (BaseDashboardPage,), {
                    "__init__": lambda self, parent=None, title=_title: \
                                  BaseDashboardPage.__init__(self, title, parent)
                })
# --- End Dependency Imports ---


class DashboardLayoutWidget(QWidget):
    logout_requested = Signal()

    def __init__(self, owner_username, product_processor_instance, parent=None):
        super().__init__(parent)
        self.owner_username = owner_username
        self.product_processor = product_processor_instance

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar_widget = ModernGradientWidget()
        self.sidebar_widget.setFixedWidth(220)
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(10)

        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        self.logo_widget_sidebar = LogoWidget()
        self.sidebar_layout.addWidget(self.logo_widget_sidebar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # --- Content Area with QStackedWidget ---
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: #ffffff;") # Clean white for content pages
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0,0,0,0) # No internal margins for the stacked widget container
        self.content_layout.setSpacing(0)

        self.page_stack = QStackedWidget()
        self.content_layout.addWidget(self.page_stack)

        self.pages = {}
        self.sidebar_buttons = {} # Store button references for styling

        # Order matters for the sidebar if you want a specific button order
        page_definitions = [
            ("Dashboard", DashboardHomePage, []), # Page Key, Class, constructor args
            ("Product", ProductPage, [self.owner_username, self.product_processor]), # Pass args for ProductPage
            ("Sales", SalesPage, []), # Assuming SalesPage might need owner_username later
            ("Goals", GoalsPage, []),
            ("History", HistoryPage, []),
            ("Notifications", NotificationsPage, []),
            ("Profile", ProfilePage, []), # Might need owner_username or full user_data
            ("Settings", SettingsPage, []),
        ]

        for key, PageClass, args in page_definitions:
            try:
                page_instance = PageClass(*args) # Instantiate with arguments
                self.page_stack.addWidget(page_instance)
                self.pages[key] = page_instance
            except Exception as e:
                print(f"Error instantiating page '{key}' ({PageClass.__name__ if PageClass else 'UnknownClass'}): {e}")
                # Add a simple placeholder widget if page instantiation fails
                error_page = QWidget()
                error_layout = QVBoxLayout(error_page)
                error_label = QLabel(f"Error loading '{key}' page.\nCheck console for details.")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                error_label.setStyleSheet("font-size: 16px; color: red;")
                error_layout.addWidget(error_label)
                self.page_stack.addWidget(error_page)
                self.pages[key] = error_page # Store placeholder

        sidebar_buttons_data = [
            ("Dashbord", "Dashboard"), # Icon filename, Page key/Display text
            ("Product", "Product"),
            ("Sales", "Sales"),
            ("Goals", "Goals"),
            ("History", "History"),
            ("Notifications", "Notifications"),
            ("Profile", "Profile"),
            ("Setting", "Settings"),
            ("Log out", "Log Out") # Log Out will be handled differently
        ]

        for icon_name, page_key_or_action in sidebar_buttons_data:
            button_text = page_key_or_action
            button = QPushButton(f"  {button_text}")
            button.setIconSize(QSize(18,18))
            button.setMinimumHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: 500;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.25);
                }
                QPushButton[active="true"] {
                    background-color: rgba(0, 0, 0, 0.2);
                    border-left: 3px solid #FFFFFF;
                    font-weight: bold;
                }
            """)
            try:
                base_path = "assets"
                if hasattr(sys, '_MEIPASS'):
                    base_path = os.path.join(sys._MEIPASS, "assets")
                elif __name__ == "__main__" or not getattr(sys, 'frozen', False):
                    current_file_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
                    project_root_dir = os.path.dirname(current_file_dir)
                    base_path = os.path.join(project_root_dir, "assets")

                icon_path = os.path.join(base_path, f"{icon_name}.png")

                if os.path.exists(icon_path):
                    button.setIcon(QIcon(icon_path))
                else:
                    print(f"Sidebar icon not found: {icon_path} (for button: {button_text})")
            except Exception as e:
                print(f"Error loading icon {icon_name} for {button_text}: {e}")

            self.sidebar_layout.addWidget(button)
            self.sidebar_buttons[page_key_or_action] = button # Store button reference

            if page_key_or_action == "Notifications": # Add spacer after Notifications group
                self.sidebar_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

            if page_key_or_action in self.pages: # It's a navigation button
                button.clicked.connect(lambda checked=False, p=page_key_or_action: self.switch_page(p))
            elif page_key_or_action == "Log Out":
                button.clicked.connect(self.handle_logout_button_clicked_internal) # Renamed

        self.sidebar_layout.addStretch(1) # Push last items to bottom or fill space

        # Add sidebar and content area to the main layout
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_area, 1) # content_area takes remaining space

        if "Dashboard" in self.pages: # Check if Dashboard page was successfully created
            self.switch_page("Dashboard")
        else:
            print("Warning: Dashboard page not available to set as initial page.")


    def switch_page(self, page_key_to_switch):
        if page_key_to_switch in self.pages:
            current_page_widget = self.page_stack.currentWidget()
            target_page = self.pages[page_key_to_switch]

            if current_page_widget == target_page: # Already on the target page
                if isinstance(target_page, BaseDashboardPage): # Still call load_page_data (e.g., for refresh)
                    target_page.load_page_data()
                return

            if isinstance(current_page_widget, BaseDashboardPage):
                current_page_widget.unload_page_data()

            self.page_stack.setCurrentWidget(target_page)
            print(f"Switched to {page_key_to_switch} page.")

            if isinstance(target_page, BaseDashboardPage):
                target_page.load_page_data()

            # Update active button state
            for key, btn in self.sidebar_buttons.items():
                is_active = (key == page_key_to_switch)
                btn.setProperty("active", is_active)
                if btn.style(): # Check if button has a style object
                    btn.style().unpolish(btn)
                    btn.style().polish(btn)
        else:
            print(f"Warning: Page key '{page_key_to_switch}' not found in self.pages.")

    def handle_logout_button_clicked_internal(self): # Renamed to avoid conflict if inherited
        print("Logout button clicked in DashboardLayoutWidget. Emitting logout_requested signal.")
        self.logout_requested.emit()


class DashboardWindow(QMainWindow):
    app_logout_requested = Signal() # This signal will be connected by UserController

    def __init__(self, user_data, main_db_manager_instance): # main_db_manager for users
        super().__init__()
        self.user_data = user_data
        # self.main_db_manager = main_db_manager_instance # Store if needed by DashboardWindow directly

        # --- Product Specific Database and Processor ---
        self.product_db_manager = None
        self.product_processor = None
        try:
            from model.product_database_manager import ProductDatabaseManager
            from processing.product_processing import ProductProcessor
            self.product_db_manager = ProductDatabaseManager() # Manages database_product.db
            self.product_processor = ProductProcessor(self.product_db_manager)
        except ImportError as e:
            print(f"FATAL: DashboardWindow - Could not import Product DB/Processor: {e}")
            # Create dummy/placeholder processors if import fails to prevent crashes
            class DummyProductDBManager:
                def __init__(self, *args, **kwargs): pass
                def close_connection(self): pass
            class DummyProductProcessor:
                def __init__(self, *args, **kwargs): pass
                def get_products_for_display(self, *args, **kwargs): return []
                def add_new_product(self, *args, **kwargs): return False, "Product processor not available.", None
                # Add other methods as ProductPage might call them
                def get_single_product_details(self, *args, **kwargs): return None
                def update_product_details(self, *args, **kwargs): return False, "Product processor not available."
                def remove_product(self, *args, **kwargs): return False, "Product processor not available."

            if not self.product_db_manager: self.product_db_manager = DummyProductDBManager()
            if not self.product_processor: self.product_processor = DummyProductProcessor(self.product_db_manager)


        self.setWindowTitle("Track App - Dashboard")
        if self.user_data and 'name' in self.user_data:
            self.setWindowTitle(f"Track App - Dashboard ({self.user_data['name']})")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_window_layout = QVBoxLayout(self.central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        main_window_layout.setSpacing(0)

        # Get owner_username for product operations
        # Use name as username, ensure it's available. If not, use email or a default.
        owner_username = self.user_data.get('name') if self.user_data else "unknown_user"
        if not owner_username and self.user_data: # Fallback to email if name is not present
            owner_username = self.user_data.get('email', "unknown_user")
        if not owner_username: # Final fallback
             print("CRITICAL: Owner username could not be determined for DashboardWindow!")
             owner_username = "unknown_user_critical_fallback"


        self.dashboard_layout_widget = DashboardLayoutWidget(
            owner_username,
            self.product_processor,
            self
        )
        self.dashboard_layout_widget.logout_requested.connect(self.app_logout_requested.emit)
        main_window_layout.addWidget(self.dashboard_layout_widget)

    def set_user_info(self, user_data): # To update user info if needed later
        self.user_data = user_data
        if self.user_data and 'name' in self.user_data:
            self.setWindowTitle(f"Track App - Dashboard ({self.user_data['name']})")
        
        # Update owner_username in DashboardLayoutWidget if it exists and user_data changed
        if hasattr(self.dashboard_layout_widget, 'owner_username'):
            new_owner_username = self.user_data.get('name') if self.user_data else "unknown_user"
            if not new_owner_username and self.user_data: new_owner_username = self.user_data.get('email', "unknown_user")
            if not new_owner_username : new_owner_username = "unknown_user_critical_fallback" # Should not happen if user_data is valid
            self.dashboard_layout_widget.owner_username = new_owner_username
        
        # Potentially tell current page to reload data if user context changed significantly
        if hasattr(self.dashboard_layout_widget, 'page_stack'):
            current_dash_page = self.dashboard_layout_widget.page_stack.currentWidget()
            if isinstance(current_dash_page, BaseDashboardPage):
                current_dash_page.load_page_data()

    def closeEvent(self, event): # Ensure product DB is also closed
        print("[DashboardWindow closeEvent] Closing product DB manager.")
        if hasattr(self, 'product_db_manager') and self.product_db_manager:
            self.product_db_manager.close_connection()
        super().closeEvent(event)


# For standalone testing of DashboardWindow
if __name__ == "__main__":
    # --- Path adjustment for standalone run ---
    current_file_dir = os.path.dirname(os.path.abspath(__file__ if '__file__' in globals() else sys.executable))
    project_root_dir = os.path.dirname(current_file_dir) # 'view' folder's parent
    # Add project_root to sys.path to allow 'from model...' and 'from processing...'
    if project_root_dir not in sys.path:
        sys.path.insert(0, project_root_dir)
    # --- End path adjustment ---

    try:
        from model.user_database_manager import DatabaseManager as UserDatabaseManager # For user auth
        from model.product_database_manager import ProductDatabaseManager # For actual product DB
        from processing.product_processing import ProductProcessor
        # Import other view components as they are defined in their respective files
        # from view.shared_ui import ModernGradientWidget, LogoWidget (already attempted above)
        # from view.base_dashboard_page import BaseDashboardPage (already attempted above)
        # from view.dashboard_home_page import DashboardHomePage (already attempted above)
        # from view.product_page import ProductPage (already attempted above)
    except ImportError as e:
        print(f"Error during standalone DashboardWindow test preparation (model/processing imports): {e}")
        class UserDatabaseManager:
            def __init__(self, *args, **kwargs): print("Using Dummy UserDatabaseManager for test.")
            def get_user_by_email(self, *args, **kwargs): return None
            def add_user(self, *args, **kwargs): return False, "Dummy add"
            def close_connection(self, *args, **kwargs): pass
        class ProductDatabaseManager:
            def __init__(self, *args, **kwargs): print("Using Dummy ProductDatabaseManager for test.")
            def close_connection(self, *args, **kwargs): pass
        class ProductProcessor:
            def __init__(self, *args, **kwargs): print("Using Dummy ProductProcessor for test.")
            def get_products_for_display(self, *args, **kwargs): return []
            def add_new_product(self, *args, **kwargs): return False, "Dummy Processor: Product not added", None
            def get_single_product_details(self, *args, **kwargs): return None
            def update_product_details(self, *args, **kwargs): return False, "Dummy update"
            def remove_product(self, *args, **kwargs): return False, "Dummy remove"

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    default_font = QFont("Segoe UI", 10)
    app.setFont(default_font)

    test_user_db_manager = UserDatabaseManager() # Manages user_database.db
    # For standalone testing, ensure the product DB file can be created/accessed
    # test_product_db_manager = ProductDatabaseManager() # This will be created inside DashboardWindow

    test_user_data = {"name": "Dashboard Tester", "email": "dashboard.tester@example.com"}

    user_in_db = test_user_db_manager.get_user_by_email(test_user_data["email"])
    if not user_in_db:
        if hasattr(test_user_db_manager, 'add_user'):
            print(f"Adding test user {test_user_data['email']} for dashboard standalone test.")
            success, _ = test_user_db_manager.add_user(test_user_data["name"], test_user_data["email"], "testpass123")
            if success:
                user_in_db = test_user_db_manager.get_user_by_email(test_user_data["email"])
            else:
                print("Failed to add test user for standalone dashboard test.")
    
    if user_in_db:
        test_user_data["id"] = user_in_db["id"]
    else:
        print("CRITICAL: Could not ensure test user exists for standalone dashboard. Using dummy ID.")
        test_user_data["id"] = 999 # Fallback ID

    # DashboardWindow takes the main user_db_manager for its own product_processor init if needed,
    # but primarily uses user_data.
    window = DashboardWindow(user_data=test_user_data, main_db_manager_instance=test_user_db_manager)
    window.resize(1300, 850)
    window.show()
    app_exit_code = app.exec()
    
    # Close connections
    if hasattr(test_user_db_manager, 'close_connection'):
        test_user_db_manager.close_connection()
    if hasattr(window, 'product_db_manager') and window.product_db_manager and hasattr(window.product_db_manager, 'close_connection'):
        window.product_db_manager.close_connection()
        
    sys.exit(app_exit_code)