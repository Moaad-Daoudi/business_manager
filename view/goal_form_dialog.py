from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                               QDoubleSpinBox, QSpinBox, QPushButton, QComboBox,
                               QDialogButtonBox, QDateEdit, QMessageBox, QLabel,
                               QHBoxLayout, QFrame, QSpacerItem, QSizePolicy,
                               QScrollArea, QWidget)
from PySide6.QtCore import QDate, Qt, QEvent
from PySide6.QtGui import QFont, QIcon


class ScrollEventBlocker(QWidget):
    def eventFilter(self, watched, event):
        scroll_events = {
            QEvent.Type.Wheel,
            QEvent.Type.Scroll,
            QEvent.Type.Gesture,
        }
        event.ignore()
        
        if event.type() in scroll_events:
            if isinstance(watched, (QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit)):
                if watched.hasFocus():
                    watched.clearFocus()
                return True
        
        return super().eventFilter(watched, event)


class GoalFormDialog(QDialog):
    def __init__(self, product_processor, user_id, parent=None):
        super().__init__(parent)
        self.product_processor = product_processor
        self.user_id = user_id
        
        self.setWindowTitle("Create New Sales Target")
        self.setMinimumWidth(520)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        
        self.setStyleSheet("""
            QDialog {
                background: #ffffff;
                border-radius: 16px;
            }
            QLabel {
                color: #374151;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
            }
            /* Clear, modern input styling */
            QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QDateEdit {
                padding: 14px 16px;
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background: #ffffff;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #111827;
                min-height: 20px;
                selection-background-color: #3b82f6;
                selection-color: white;
            }
            /* Clear focus states */
            QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, 
            QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3b82f6;
                background: #ffffff;
                border-color: #3498db;
                outline: none;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            /* Clear hover states */
            QLineEdit:hover, QDoubleSpinBox:hover, QSpinBox:hover,
            QComboBox:hover, QDateEdit:hover {
                border: 2px solid #6b7280;
                background: #fafafa;
            }
            QLineEdit:hover:focus, QDoubleSpinBox:hover:focus, QSpinBox:hover:focus,
            QComboBox:hover:focus, QDateEdit:hover:focus {
                border: 2px solid #3b82f6;
                background: #ffffff;
                border-color: #3498db;
                outline: none;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            /* ComboBox specific styling */
            QComboBox {
                padding-right: 40px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #6b7280;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #d1d5db;
                border-radius: 8px;
                background: white;
                selection-background-color: #3b82f6;
                selection-color: white;
                padding: 4px;
            }
            /* DateEdit specific styling */
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border: none;
                background: transparent;
            }
            QDateEdit::down-arrow {
                width: 12px;
                height: 12px;
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #6b7280;
            }
            /* SpinBox button styling */
            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                width: 20px;
                border: none;
                background: transparent;
            }
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {
                width: 8px;
                height: 8px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #6b7280;
            }
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {
                width: 8px;
                height: 8px;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #6b7280;
            }
            /* Placeholder text styling */
            QLineEdit[placeholderText] {
                color: #9ca3af;
            }
        """)
        
        self._setup_ui()
        self._populate_products()

    def _setup_ui(self):
        self.scroll_blocker = ScrollEventBlocker(self)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(20)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""                  
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

        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll_content_widget = QWidget()
        form_container_layout = QVBoxLayout(scroll_content_widget)
        form_container_layout.setContentsMargins(0, 0, 20, 0)  
        form_container_layout.setSpacing(32)      
          
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        title_label = QLabel("Create New Sales Goal")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #1f2937; margin-bottom: 8px;")
        
        subtitle_label = QLabel("Set ambitious targets and track your progress")
        subtitle_label.setFont(QFont("Segoe UI", 15))
        subtitle_label.setStyleSheet("color: #6b7280; margin-bottom: 20px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        form_container_layout.addLayout(header_layout)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background: #e5e7eb; max-height: 1px; border: none;")
        form_container_layout.addWidget(divider)
        
        self._add_goal_info_section(form_container_layout)
        self._add_targets_section(form_container_layout)
        self._add_timeline_section(form_container_layout)
        
        form_container_layout.addSpacing(20)
        
        scroll_area.setWidget(scroll_content_widget)
        main_layout.addWidget(scroll_area)
        
        self._create_buttons(main_layout)

    def _add_goal_info_section(self, parent_layout):
        """Add Goal Information section with clear inputs"""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setSpacing(16)
        
        title = QLabel("Goal Information")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1f2937; margin-bottom: 8px;")
        section_layout.addWidget(title)
        
        name_layout = QVBoxLayout()
        name_layout.setSpacing(6)
        name_label = QLabel("Goal Name *")
        name_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        name_label.setStyleSheet("color: #374151;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Q4 Premium Sales Drive")
        self.name_input.setMinimumHeight(50)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        section_layout.addLayout(name_layout)
        
        product_layout = QVBoxLayout()
        product_layout.setSpacing(6)
        product_label = QLabel("Target Product")
        product_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        product_label.setStyleSheet("color: #374151;")
        self.product_combo = QComboBox()
        self.product_combo.setMinimumHeight(50)
        product_layout.addWidget(product_label)
        product_layout.addWidget(self.product_combo)
        section_layout.addLayout(product_layout)
        
        parent_layout.addWidget(section_widget)
        
        self.product_combo.installEventFilter(self.scroll_blocker)

    def _add_targets_section(self, parent_layout):
        """Add Sales Targets section with clear inputs"""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setSpacing(16)
        
        title = QLabel("Sales Targets")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1f2937; margin-bottom: 8px;")
        section_layout.addWidget(title)
        
        revenue_layout = QVBoxLayout()
        revenue_layout.setSpacing(6)
        revenue_label = QLabel("Revenue Target")
        revenue_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        revenue_label.setStyleSheet("color: #374151;")
        self.revenue_input = QDoubleSpinBox()
        self.revenue_input.setRange(0, 9999999.99)
        self.revenue_input.setDecimals(2)
        self.revenue_input.setPrefix("$ ")
        self.revenue_input.setSpecialValueText("No revenue target")
        self.revenue_input.setMinimumHeight(50)
        self.revenue_input.setValue(0)  
        revenue_layout.addWidget(revenue_label)
        revenue_layout.addWidget(self.revenue_input)
        section_layout.addLayout(revenue_layout)
        
        self.revenue_input.installEventFilter(self.scroll_blocker)
        
        quantity_layout = QVBoxLayout()
        quantity_layout.setSpacing(6)
        quantity_label = QLabel("Quantity Target")
        quantity_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        quantity_label.setStyleSheet("color: #374151;")
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 999999)
        self.quantity_input.setSuffix(" units")
        self.quantity_input.setSpecialValueText("No quantity target")
        self.quantity_input.setMinimumHeight(50)
        self.quantity_input.setValue(0)  
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_input)
        section_layout.addLayout(quantity_layout)
        
        parent_layout.addWidget(section_widget)
        
        self.quantity_input.installEventFilter(self.scroll_blocker)

    def _add_timeline_section(self, parent_layout):
        """Add Timeline section with clear inputs"""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setSpacing(16)
        
        title = QLabel("Timeline")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1f2937; margin-bottom: 8px;")
        section_layout.addWidget(title)
        
        start_layout = QVBoxLayout()
        start_layout.setSpacing(6)
        start_label = QLabel("Start Date")
        start_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        start_label.setStyleSheet("color: #374151;")
        self.start_date_input = QDateEdit(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setMinimumHeight(50)
        self.start_date_input.setDisplayFormat("MMMM d, yyyy")
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_date_input)
        section_layout.addLayout(start_layout)
        
        self.start_date_input.installEventFilter(self.scroll_blocker)
        
        deadline_layout = QVBoxLayout()
        deadline_layout.setSpacing(6)
        deadline_label = QLabel("Deadline")
        deadline_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        deadline_label.setStyleSheet("color: #374151;")
        self.deadline_input = QDateEdit(QDate.currentDate().addMonths(1))
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setMinimumHeight(50)
        self.deadline_input.setDisplayFormat("MMMM d, yyyy")
        deadline_layout.addWidget(deadline_label)
        deadline_layout.addWidget(self.deadline_input)
        section_layout.addLayout(deadline_layout)
        
        self.deadline_input.installEventFilter(self.scroll_blocker)
        
        parent_layout.addWidget(section_widget)

    def _create_buttons(self, parent_layout):
        """Create clear, well-styled buttons"""
        button_container = QFrame()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 24, 0, 0)
        button_layout.setSpacing(16)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        cancel_btn.setFixedHeight(52)
        cancel_btn.setMinimumWidth(120)
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f9fafb;
                color: #374151;
                border: 2px solid #d1d5db;
                border-radius: 10px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background: #f3f4f6;
                border: 2px solid #9ca3af;
            }
            QPushButton:pressed {
                background: #e5e7eb;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        create_btn = QPushButton("Create Goal")
        create_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        create_btn.setFixedHeight(52)
        create_btn.setMinimumWidth(160)
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                padding: 0 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            QPushButton:pressed {
                background: #1d4ed8;
            }
        """)
        create_btn.clicked.connect(self.accept)
        create_btn.setDefault(True)  
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(create_btn)
        
        parent_layout.addWidget(button_container)

    def _populate_products(self):
        """Populate the product combobox"""
        self.product_combo.addItem("Global (All Products)", None)
        try:
            products = self.product_processor.get_products_for_display(self.user_id)
            for p in products:
                self.product_combo.addItem(f"{p['product_name']}", p['id'])
        except Exception as e:
            print(f"Error populating products: {e}")

    def get_goal_data(self):
        """Get and validate goal data"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", 
                              "Goal name is required.")
            self.name_input.setFocus()
            return None
            
        if self.start_date_input.date() > self.deadline_input.date():
            QMessageBox.warning(self, "Validation Error", 
                              "Start date cannot be after the deadline.")
            self.start_date_input.setFocus()
            return None
            
        if self.revenue_input.value() == 0 and self.quantity_input.value() == 0:
            reply = QMessageBox.question(self, "No Targets Set", 
                                       "You haven't set any revenue or quantity targets. Continue anyway?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return None

        start_date = self.start_date_input.date().toString(Qt.ISODate) + " 00:00:00"
        deadline = self.deadline_input.date().toString(Qt.ISODate) + " 23:59:59"

        return {
            "goal_name": self.name_input.text().strip(),
            "product_id": self.product_combo.currentData(),
            "target_revenue": self.revenue_input.value() if self.revenue_input.value() > 0 else None,
            "target_quantity": self.quantity_input.value() if self.quantity_input.value() > 0 else None,
            "start_date": start_date,
            "deadline": deadline
        }
        