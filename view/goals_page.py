# view/goals_page.py
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                               QScrollArea, QFrame, QProgressBar, QMessageBox, QWidget)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QIcon
from datetime import datetime

from .base_dashboard_page import BaseDashboardPage
from processing.goals_processor import GoalsProcessor
from .goal_form_dialog import GoalFormDialog
from .shared_ui import StyledAlertDialog

class GoalCardWidget(QFrame):
    delete_requested = Signal(int, str)

    def __init__(self, goal_data, parent=None):
        super().__init__(parent)
        self.goal_id = goal_data['id']
        self.goal_name = goal_data['goal_name']
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("goalCard")
        self.setStyleSheet("#goalCard { border: 1px solid #ddd; border-radius: 8px; background-color: white; }")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)

        header_layout = QHBoxLayout()
        name_label = QLabel(self.goal_name)
        name_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("assets/icons/delete.png"))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFEBEE; /* Light red background */
                border-radius: 14px; /* Half of the fixed size to make it a circle */
                border: none;
            }
            QPushButton:hover {
                background-color: #FFCDD2; /* Slightly darker red on hover */
            }
            QPushButton:pressed {
                background-color: #EF9A9A; /* Even darker when clicked */
            }
        """)
        delete_btn.setToolTip("Delete Goal")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.goal_id, self.goal_name))
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(delete_btn)
        main_layout.addLayout(header_layout)

        start = datetime.fromisoformat(goal_data['start_date']).strftime('%b %d, %Y')
        end = datetime.fromisoformat(goal_data['deadline']).strftime('%b %d, %Y')
        date_label = QLabel(f"Period: {start} to {end}")
        date_label.setStyleSheet("color: #666;")
        main_layout.addWidget(date_label)

        if goal_data.get('target_revenue'):
            self._create_progress_section(main_layout, "Revenue", 
                                          goal_data['current_revenue'], 
                                          goal_data['target_revenue'], is_money=True)
        if goal_data.get('target_quantity'):
            self._create_progress_section(main_layout, "Quantity", 
                                          goal_data['current_quantity'], 
                                          goal_data['target_quantity'])
                                          

    def _create_progress_section(self, layout, name, current, target, is_money=False):
        layout.addSpacing(10)
        
        progress_layout = QHBoxLayout()
        label = QLabel(f"{name} Target:")
        
        # This logic correctly handles the values being None from the database
        current = current or 0
        target = target or 1 # Use 1 to avoid division by zero errors

        # This part for formatting the text is correct
        if is_money:
            value_text = f"<b>${current:,.2f}</b> / ${target:,.2f}"
        else:
            value_text = f"<b>{current:,}</b> / {target:,} units"
            
        value_label = QLabel(value_text)
        value_label.setAlignment(Qt.AlignRight)
        
        progress_layout.addWidget(label)
        progress_layout.addWidget(value_label)
        layout.addLayout(progress_layout)

        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setTextVisible(False) # Hide the default "55%" text
        
        # --- THIS IS THE CRITICAL FIX ---
        # Calculate the raw percentage
        raw_percentage = (current / target * 100) if target > 0 else 0
        # Cap the value at 100 before setting it on the progress bar
        capped_percentage = min(raw_percentage, 100)
        progress_bar.setValue(int(capped_percentage))
        # --------------------------------

        # Apply a style to make it look good
        if raw_percentage >= 100:
            # A green color for completed goals
            progress_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #ccc; border-radius: 5px; background-color: #e9ecef; }
                QProgressBar::chunk { background-color: #27ae60; border-radius: 4px; }
            """)
        else:
            # A blue color for in-progress goals
            progress_bar.setStyleSheet("""
                QProgressBar { border: 1px solid #ccc; border-radius: 5px; background-color: #e9ecef; }
                QProgressBar::chunk { background-color: #3498db; border-radius: 4px; }
            """)

        layout.addWidget(progress_bar)
        
class GoalsPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, data_changed_signal, parent=None):
        super().__init__("Sales Targets & Goals", parent=parent)
        self.user_id = user_id
        self.product_processor = product_processor
        self.goals_processor = GoalsProcessor(product_processor.db_manager)

        self.data_changed_signal = data_changed_signal
        self.data_changed_signal.connect(self.refresh_goals_list)

        top_bar = QHBoxLayout()
        add_goal_btn = QPushButton(QIcon("assets/icons/add.png"), "  Create New Goal")
        add_goal_btn.clicked.connect(self.open_add_goal_dialog)
        top_bar.addStretch()
        top_bar.addWidget(add_goal_btn)
        self.content_layout.addLayout(top_bar)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        self.goals_layout = QVBoxLayout(scroll_content)
        self.goals_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area.setWidget(scroll_content)
        self.content_layout.addWidget(self.scroll_area)

    def load_page_data(self):
        super().load_page_data()
        self.refresh_goals_list()

    def refresh_goals_list(self):
        while self.goals_layout.count():
            child = self.goals_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        goals = self.goals_processor.get_all_goals_with_progress(self.user_id)
        
        if not goals:
            no_goals_label = QLabel("No goals set yet. Click 'Create New Goal' to get started!")
            no_goals_label.setAlignment(Qt.AlignCenter)
            no_goals_label.setStyleSheet("font-size: 16px; color: #888;")
            self.goals_layout.addWidget(no_goals_label)
        else:
            for goal in goals:
                card = GoalCardWidget(goal)
                card.delete_requested.connect(self.handle_delete_goal)
                self.goals_layout.addWidget(card)

    def open_add_goal_dialog(self):
        dialog = GoalFormDialog(self.product_processor, self.user_id, self)
        if dialog.exec():
            goal_data = dialog.get_goal_data()
            if goal_data:
                success, message = self.goals_processor.add_new_goal(self.user_id, goal_data)
                StyledAlertDialog.show_alert("Create Goal", message, "info" if success else "error")
                if success:
                    self.data_changed_signal.emit("goals")
                    
    def handle_delete_goal(self, goal_id, goal_name):
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete the goal:\n'{goal_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, message = self.goals_processor.delete_goal(self.user_id, goal_id)
            StyledAlertDialog.show_alert("Delete Goal", message, "info" if success else "error")
            if success:
                # Emit the signal to notify all connected pages
                self.data_changed_signal.emit("goals")