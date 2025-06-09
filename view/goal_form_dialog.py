# view/goal_form_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                               QDoubleSpinBox, QSpinBox, QPushButton, QComboBox,
                               QDialogButtonBox, QDateEdit, QMessageBox)
from PySide6.QtCore import QDate, Qt

class GoalFormDialog(QDialog):
    def __init__(self, product_processor, user_id, parent=None):
        super().__init__(parent)
        self.product_processor = product_processor
        self.user_id = user_id
        
        self.setWindowTitle("Create New Sales Target")
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Q4 T-Shirt Sales Drive")
        
        self.product_combo = QComboBox()
        
        self.revenue_input = QDoubleSpinBox()
        self.revenue_input.setRange(0, 9999999.99)
        self.revenue_input.setPrefix("$ ")
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 999999)
        
        self.start_date_input = QDateEdit(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        
        self.deadline_input = QDateEdit(QDate.currentDate().addMonths(1))
        self.deadline_input.setCalendarPopup(True)

        form_layout.addRow("Goal Name*:", self.name_input)
        form_layout.addRow("Target Product:", self.product_combo)
        form_layout.addRow("Target Revenue:", self.revenue_input)
        form_layout.addRow("Target Quantity:", self.quantity_input)
        form_layout.addRow("Start Date:", self.start_date_input)
        form_layout.addRow("Deadline*:", self.deadline_input)
        
        layout.addLayout(form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self._populate_products()

    def _populate_products(self):
        self.product_combo.addItem("Global (All Products)", None) # None for product_id
        products = self.product_processor.get_products_for_display(self.user_id)
        for p in products:
            self.product_combo.addItem(p['product_name'], p['id'])

    def get_goal_data(self):
        start_date = self.start_date_input.date().toString(Qt.ISODate) + " 00:00:00"
        deadline = self.deadline_input.date().toString(Qt.ISODate) + " 23:59:59"

        if self.start_date_input.date() > self.deadline_input.date():
            QMessageBox.warning(self, "Invalid Dates", "The start date cannot be after the deadline.")
            return None

        return {
            "goal_name": self.name_input.text().strip(),
            "product_id": self.product_combo.currentData(),
            "target_revenue": self.revenue_input.value() if self.revenue_input.value() > 0 else None,
            "target_quantity": self.quantity_input.value() if self.quantity_input.value() > 0 else None,
            "start_date": start_date,
            "deadline": deadline
        }