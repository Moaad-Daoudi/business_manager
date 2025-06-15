from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                               QScrollArea, QFrame, QProgressBar, QMessageBox, QWidget)
from PySide6.QtCore import Qt, Signal, QSize
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
        
        self.setFrameShape(QFrame.NoFrame)
        self.setObjectName("goalCard")
        
        self.setStyleSheet("""
            #goalCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(46,204,113,0.05), 
                    stop:0.5 rgba(52,152,219,0.05), 
                    stop:1 rgba(155,89,182,0.05));
                border: 1px solid rgba(46,204,113,0.2);
                border-radius: 16px;
                margin: 0px;
            }
            #goalCard:hover {
                border: 1px solid #cbd5e1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        name_label = QLabel(self.goal_name)
        name_label.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
        name_label.setStyleSheet("color: #1e293b; font-weight: 600;")
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("assets/icons/delete.png"))
        delete_btn.setIconSize(QSize(32, 32))
        delete_btn.setFixedSize(32, 32)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setToolTip("Delete Gools")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 16px;
                padding: 0px;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.goal_id, self.goal_name))
        
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(delete_btn)
        main_layout.addLayout(header_layout)

        start = datetime.fromisoformat(goal_data['start_date']).strftime('%b %d, %Y')
        end = datetime.fromisoformat(goal_data['deadline']).strftime('%b %d, %Y')
        
        date_label = QLabel(f"{start} → {end}")
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet("color: #64748b; padding: 8px 0px;")
        main_layout.addWidget(date_label)

        if goal_data.get('target_revenue'):
            self._create_progress_section(main_layout, "Revenue Target",
                                          goal_data['current_revenue'], 
                                          goal_data['target_revenue'], 
                                          is_money=True, color="#10b981")
        if goal_data.get('target_quantity'):
            self._create_progress_section(main_layout, "Quantity Target",
                                          goal_data['current_quantity'], 
                                          goal_data['target_quantity'],
                                          color="#3b82f6")
                                          
    def _create_progress_section(self, layout, name, current, target, is_money=False, color="#3b82f6"):
        section_layout = QVBoxLayout()
        section_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        
        title_label = QLabel(name)
        title_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #374151;")
        
        try:
            current = float(current or 0)
            target = float(target or 1)
        except (ValueError, TypeError):
            current = 0
            target = 1
            
        if is_money:
            value_text = f"<span style='font-weight: 600; color: {color}; font-size: 14px;'>${current:,.2f}</span> <span style='color: #9ca3af; font-size: 13px;'>/ ${target:,.2f}</span>"
        else:
            value_text = f"<span style='font-weight: 600; color: {color}; font-size: 14px;'>{current:,.0f}</span> <span style='color: #9ca3af; font-size: 13px;'>/ {target:,.0f} units</span>"
            
        value_label = QLabel(value_text)
        value_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(value_label)
        section_layout.addLayout(header_layout)

        progress_bar = QProgressBar()
        
        max_value = max(target, current) if current > target else target
        progress_bar.setRange(0, int(max_value))
        progress_bar.setValue(int(current))
            
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(6)
        
        progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 3px;
                background: #f1f5f9;
            }}
            QProgressBar::chunk {{
                background: {color};
                border-radius: 3px;
            }}
        """)
        
        section_layout.addWidget(progress_bar)
        
        percentage = (current / target * 100) if target > 0 else 0
        percentage_label = QLabel(f"{percentage:.1f}% Complete")
        percentage_label.setFont(QFont("Segoe UI", 11))
        percentage_label.setStyleSheet(f"color: {color}; font-weight: 500;")
        section_layout.addWidget(percentage_label)
        
        layout.addLayout(section_layout)
        
    def _lighten_color(self, hex_color):
        """Lighten a hex color for gradient effect"""
        if hex_color == "#10b981":
            return "#34d399"
        elif hex_color == "#3b82f6":
            return "#60a5fa"
        return hex_color

class GoalsPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, data_changed_signal, parent=None):
        super().__init__("Sales Targets & Goals", parent=parent)
        self.user_id = user_id
        self.product_processor = product_processor
        self.goals_processor = GoalsProcessor(product_processor.db_manager)

        self.data_changed_signal = data_changed_signal
        self.data_changed_signal.connect(self.handle_global_data_change)

        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
            }
        """)

        top_bar_widget = QFrame()
        top_bar_widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(74,144,226,0.05), stop:1 rgba(46,204,113,0.05));
                border-radius: 16px;
                padding: 16px;
                border: 1px solid #E8F4FD;
            }
        """)
        
        top_bar = QHBoxLayout(top_bar_widget)
        top_bar.setContentsMargins(24, 20, 24, 20)
        
        page_title = QLabel("Your Sales Goals")
        page_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        page_title.setStyleSheet("color: #1e293b;")
        
        add_goal_btn = QPushButton("Create New Goal")
        add_goal_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        add_goal_btn.setFixedHeight(40)
        add_goal_btn.setCursor(Qt.PointingHandCursor)
        add_goal_btn.setStyleSheet("""
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                min-width: 140px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
            QPushButton:pressed {
                background: #1d4ed8;
            }
        """)
        add_goal_btn.clicked.connect(self.open_add_goal_dialog)
        
        top_bar.addWidget(page_title)
        top_bar.addStretch()
        top_bar.addWidget(add_goal_btn)
        self.content_layout.addWidget(top_bar_widget)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 6px;
                border-radius: 3px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.goals_layout = QVBoxLayout(scroll_content)
        self.goals_layout.setAlignment(Qt.AlignTop)
        self.goals_layout.setSpacing(16)
        self.goals_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area.setWidget(scroll_content)
        self.content_layout.addWidget(self.scroll_area)

    def load_page_data(self):
        super().load_page_data()
        self.refresh_goals_list()

    def handle_global_data_change(self, data_type):
        """Refreshes the goals list if relevant data changed."""
        if data_type in ["goals", "reset"]:
            self.refresh_goals_list()

    def refresh_goals_list(self):
        while self.goals_layout.count():
            child = self.goals_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        goals = self.goals_processor.get_all_goals_with_progress(self.user_id)
        
        if not goals:
            empty_state = QFrame()
            empty_state.setStyleSheet("""
                QFrame {
                    background: white;
                    border: 2px dashed #cbd5e1;
                    border-radius: 12px;
                    padding: 40px;
                    margin: 20px 0px;
                }
            """)
            
            empty_layout = QVBoxLayout(empty_state)
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(12)
                        
            empty_title = QLabel("No Goals Set Yet")
            empty_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
            empty_title.setAlignment(Qt.AlignCenter)
            empty_title.setStyleSheet("color: #64748b;")
            
            empty_subtitle = QLabel("Create your first sales goal to start tracking your progress!")
            empty_subtitle.setFont(QFont("Segoe UI", 12))
            empty_subtitle.setAlignment(Qt.AlignCenter)
            empty_subtitle.setStyleSheet("color: #94a3b8;")
            
            empty_layout.addWidget(empty_title)
            empty_layout.addWidget(empty_subtitle)
            
            self.goals_layout.addWidget(empty_state)
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
                    log_desc = f"Created new goal: '{goal_data.get('goal_name')}'"
                    self.goals_processor.db_manager.add_activity_log(self.user_id, "Goal", log_desc)
                    self.data_changed_signal.emit("goals")
                    
    def handle_delete_goal(self, goal_id, goal_name):
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete the goal:\n'{goal_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, message = self.goals_processor.delete_goal(self.user_id, goal_id)
            StyledAlertDialog.show_alert("Delete Goal", message, "info" if success else "error")
            if success:
                log_desc = f"Deleted goal: '{goal_name}'"
                self.goals_processor.db_manager.add_activity_log(self.user_id, "Goal", log_desc)
                self.data_changed_signal.emit("goals")