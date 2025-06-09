# view/dashboard_window.py
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QSpacerItem, QSizePolicy, QStackedWidget
)
import os

from processing.product_processing import ProductProcessor
from processing.user_processing import UserProcessor

from .shared_ui import ModernGradientWidget, LogoWidget
from .base_dashboard_page import BaseDashboardPage
from .dashboard_home_page import DashboardHomePage
from .product_page import ProductPage
from .sales_page import SalesPage
from .goals_page import GoalsPage
from .profile_page import ProfilePage
from .settings_page import SettingsPage

class DashboardLayoutWidget(QWidget):
    logout_requested = Signal()
    # This signal allows pages to communicate with each other indirectly.
    data_changed = Signal(str)

    def __init__(self, user_id, product_processor_instance, user_processor_instance, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.product_processor = product_processor_instance
        self.user_processor = user_processor_instance

        # Connect the signal to a handler within this layout
        self.data_changed.connect(self.handle_data_change)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- Sidebar Setup ---
        # The sidebar's style comes from the ModernGradientWidget class itself
        # and is not affected by any global themes in this version.
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

        # --- Content Area Setup ---
        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: #ffffff;") # A simple, constant background
        self.content_layout = QVBoxLayout(self.content_area)
        self.page_stack = QStackedWidget()
        self.content_layout.addWidget(self.page_stack)

        self.pages = {}
        self.sidebar_buttons = {}

        # This list correctly defines all pages and the arguments they need to function.
        page_definitions = [
            ("Dashboard", DashboardHomePage, []),
            ("Product", ProductPage, [self.user_id, self.product_processor, self.data_changed]),
            ("Sales", SalesPage, [self.user_id, self.product_processor, self.data_changed]),
            ("Goals", GoalsPage, [self.user_id, self.product_processor, self.data_changed]),
            ("Profile", ProfilePage, [self.user_id, self.user_processor, self.data_changed]),
            ("Settings", SettingsPage, []),
        ]

        for key, PageClass, args in page_definitions:
            page_instance = PageClass(*args)
            self.page_stack.addWidget(page_instance)
            self.pages[key] = page_instance

        sidebar_buttons_data = [
            ("Dashbord", "Dashboard"), ("Product", "Product"), ("Sales", "Sales"),
            ("Goals", "Goals"),
            ("Profile", "Profile"), ("Setting", "Settings"), ("Log out", "Log Out")
        ]

        for icon_name, page_key_or_action in sidebar_buttons_data:
            button = QPushButton(f"  {page_key_or_action}")
            button.setIconSize(QSize(18, 18))
            button.setMinimumHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    color: white; background-color: transparent; border: none;
                    text-align: left; padding: 8px 16px; font-size: 14px;
                    font-weight: 500; border-radius: 5px;
                }
                QPushButton:hover { background-color: rgba(255, 255, 255, 0.15); }
                QPushButton:pressed { background-color: rgba(255, 255, 255, 0.25); }
                QPushButton[active="true"] {
                    background-color: rgba(0, 0, 0, 0.2);
                    border-left: 3px solid #FFFFFF; font-weight: bold;
                }
            """)
            
            icon_path = os.path.join("assets", f"{icon_name}.png")
            if os.path.exists(icon_path):
                 button.setIcon(QIcon(icon_path))

            self.sidebar_layout.addWidget(button)
            self.sidebar_buttons[page_key_or_action] = button

            if page_key_or_action in self.pages:
                button.clicked.connect(lambda checked=False, p=page_key_or_action: self.switch_page(p))
            elif page_key_or_action == "Log Out":
                button.clicked.connect(self.logout_requested.emit)

        self.sidebar_layout.addStretch(1)
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_area, 1)
        self.switch_page("Dashboard")

    def switch_page(self, page_key):
        if page_key in self.pages:
            target_page = self.pages[page_key]
            if self.page_stack.currentWidget() != target_page:
                if isinstance(self.page_stack.currentWidget(), BaseDashboardPage):
                    self.page_stack.currentWidget().unload_page_data()
                
                self.page_stack.setCurrentWidget(target_page)
                
                if isinstance(target_page, BaseDashboardPage):
                    target_page.load_page_data()

            for key, btn in self.sidebar_buttons.items():
                btn.setProperty("active", key == page_key)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
    
    def handle_data_change(self, data_type):
        """Refreshes the main window title if the user's name changed."""
        if data_type == "user_info":
            print("Dashboard detected user info change, updating window title...")
            main_window = self.window()
            if main_window and hasattr(main_window, 'set_user_info'):
                fresh_user_data = self.user_processor.db_manager.get_user_by_id(self.user_id)
                if fresh_user_data:
                    main_window.set_user_info(fresh_user_data)

class DashboardWindow(QMainWindow):
    app_logout_requested = Signal()

    def __init__(self, user_data, db_manager_instance, user_processor_instance):
        super().__init__()
        self.user_data = user_data
        self.product_processor = ProductProcessor(db_manager_instance)
        self.user_processor = user_processor_instance

        self.setWindowTitle(f"Track App - Dashboard ({self.user_data.get('name', 'Unknown')})")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_window_layout = QVBoxLayout(self.central_widget)
        main_window_layout.setContentsMargins(0, 0, 0, 0)

        user_id = self.user_data.get('id')
        if not user_id:
             print("CRITICAL: User ID not found in user_data! Cannot initialize dashboard.")
             return

        self.dashboard_layout_widget = DashboardLayoutWidget(
            user_id=user_id,
            product_processor_instance=self.product_processor,
            user_processor_instance=self.user_processor,
            parent=self
        )
        self.dashboard_layout_widget.logout_requested.connect(self.app_logout_requested.emit)
        main_window_layout.addWidget(self.dashboard_layout_widget)

    def set_user_info(self, user_data):
        self.user_data = user_data
        if self.user_data:
            self.setWindowTitle(f"Track App - Dashboard ({self.user_data.get('name', '')})")
            if hasattr(self.dashboard_layout_widget, 'user_id'):
                self.dashboard_layout_widget.user_id = self.user_data.get('id')
            current_page = self.dashboard_layout_widget.page_stack.currentWidget()
            if isinstance(current_page, BaseDashboardPage):
                current_page.load_page_data()

    def closeEvent(self, event):
        print("[DashboardWindow] Closing.")
        super().closeEvent(event)