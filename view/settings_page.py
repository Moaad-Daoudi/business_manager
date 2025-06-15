import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QFileDialog, QMessageBox, QApplication, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QIcon

from .base_dashboard_page import BaseDashboardPage
from .shared_ui import StyledAlertDialog

class SettingsPage(BaseDashboardPage):
    def __init__(self, user_id, product_processor, user_processor, data_changed_signal, parent=None):
        super().__init__("Application Settings", parent=parent)
        self.user_id = user_id
        self.product_processor = product_processor
        self.user_processor = user_processor
        self.data_changed_signal = data_changed_signal
        
        self.content_layout.addWidget(self._create_data_management_card())
        self.content_layout.addStretch()

    def load_page_data(self):
        super().load_page_data()
        pass 

    def _create_styled_card(self, title):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #FFFFFF, stop:1 #F8FAFC);
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 32px;
                margin: 8px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(24)
        card_layout.setContentsMargins(32, 32, 32, 32)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #1F2937;
                font-size: 24px;
                font-weight: 700;
                margin-bottom: 8px;
                padding: 0;
                border: none;
                background: transparent;
            }
        """)
        card_layout.addWidget(title_label)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #E2E8F0, stop:1 transparent);
                border: none;
                height: 2px;
                margin: 16px 0;
            }
        """)
        card_layout.addWidget(separator)
        
        return card, card_layout

    def _create_data_management_card(self):
        """Crée la carte pour les fonctionnalités d'import/export et de sauvegarde avec un design moderne."""
        card, layout = self._create_styled_card("Data Management")
        
        export_section = QVBoxLayout()
        export_section.setSpacing(16)
        
        export_title = QLabel("  Export Data")
        export_title.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
                padding: 0;
                border: none;
                background: transparent;
            }
        """)
        export_section.addWidget(export_title)
        
        export_desc = QLabel("Export your data in various formats for backup or analysis")
        export_desc.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 14px;
                font-weight: 400;
                margin-bottom: 16px;
                padding: 0;
                border: none;
                background: transparent;
            }
        """)
        export_section.addWidget(export_desc)
        
        export_csv_btn = QPushButton(QIcon("assets/icons/csv.png"), " Export to CSV")
        export_csv_btn.setIconSize(QSize(18,18))
        export_csv_btn.setCursor(Qt.PointingHandCursor)
        export_csv_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3B82F6, stop:1 #2563EB);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563EB, stop:1 #1D4ED8);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: #1D4ED8;
            }
        """)
        export_csv_btn.clicked.connect(self.export_data_csv)
        
        export_excel_btn = QPushButton(QIcon("assets/icons/xls.png"), " Export to Excel")
        export_excel_btn.setIconSize(QSize(18,18))
        export_excel_btn.setCursor(Qt.PointingHandCursor)
        export_excel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #10B981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #059669, stop:1 #047857);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: #047857;
            }
        """)
        export_excel_btn.clicked.connect(self.export_data_excel)
        
        export_pdf_btn = QPushButton(QIcon("assets/icons/pdf.png"), " Export to PDF")
        export_pdf_btn.setIconSize(QSize(18,18))
        export_pdf_btn.setCursor(Qt.PointingHandCursor)
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #F59E0B, stop:1 #D97706);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #D97706, stop:1 #B45309);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: #B45309;
            }
        """)
        export_pdf_btn.clicked.connect(self.export_data_pdf)
        
        export_button_layout = QHBoxLayout()
        export_button_layout.setSpacing(16)
        export_button_layout.addWidget(export_csv_btn)
        export_button_layout.addWidget(export_excel_btn)
        export_button_layout.addWidget(export_pdf_btn)
        export_button_layout.addStretch()
        
        export_section.addLayout(export_button_layout)
        layout.addLayout(export_section)
        
        section_separator = QFrame()
        section_separator.setFrameShape(QFrame.HLine)
        section_separator.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, stop:0.5 #E5E7EB, stop:1 transparent);
                border: none;
                height: 1px;
                margin: 24px 0;
            }
        """)
        layout.addWidget(section_separator)
        
        backup_section = QVBoxLayout()
        backup_section.setSpacing(16)
        
        backup_title = QLabel("  Database Management")
        backup_title.setStyleSheet("""
            QLabel {
                color: #374151;
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
                padding: 0;
                border: none;
                background: transparent;
            }
        """)
        backup_section.addWidget(backup_title)
        
        backup_desc = QLabel("Create backups of your database and restore from previous backups")
        backup_desc.setStyleSheet("""
            QLabel {
                color: #6B7280;
                font-size: 14px;
                font-weight: 400;
                margin-bottom: 16px;
                padding: 0;
                border: none;
                background: transparent;
            }
        """)
        backup_section.addWidget(backup_desc)
        
        backup_btn = QPushButton("Backup Database")
        backup_btn.setIconSize(QSize(18,18))
        backup_btn.setCursor(Qt.PointingHandCursor)
        backup_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6B7280, stop:1 #4B5563);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4B5563, stop:1 #374151);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: #374151;
            }
        """)
        backup_btn.clicked.connect(self.backup_database)
        
        restore_btn = QPushButton(" Restore from Backup")
        restore_btn.setIconSize(QSize(18,18))
        restore_btn.setCursor(Qt.PointingHandCursor)
        restore_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #EF4444, stop:1 #DC2626);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #DC2626, stop:1 #B91C1C);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: #B91C1C;
            }
        """)
        restore_btn.clicked.connect(self.restore_database)
        
        backup_button_layout = QHBoxLayout()
        backup_button_layout.setSpacing(16)
        backup_button_layout.addWidget(backup_btn)
        backup_button_layout.addWidget(restore_btn)
        backup_button_layout.addStretch()
        
        backup_section.addLayout(backup_button_layout)
        layout.addLayout(backup_section)
        
        return card

    def export_data_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data as CSV", "sales_and_products_report.csv", "CSV Files (*.csv)")
        if file_path:
            success, message = self.product_processor.export_products_and_sales_to_csv(self.user_id, file_path)
            StyledAlertDialog.show_alert("Export CSV", message, "info" if success else "error")
            
    def export_data_excel(self):
        default_filename = f"sales_report_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data as Excel", default_filename, "Excel Files (*.xlsx)")
        if file_path:
            success, message = self.product_processor.export_data_to_excel(self.user_id, file_path)
            StyledAlertDialog.show_alert("Export Excel", message, "info" if success else "error")

    def export_data_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Data as PDF", "sales_and_products_report.pdf", "PDF Files (*.pdf)")
        if file_path:
            success, message = self.product_processor.export_products_and_sales_to_pdf(self.user_id, file_path)
            StyledAlertDialog.show_alert("Export PDF", message, "info" if success else "error")

    def backup_database(self):
        db_path = self.product_processor.db_manager.db_path
        default_name = f"backup_{datetime.now().strftime('%Y-%m-%d')}.db"
        file_path, _ = QFileDialog.getSaveFileName(self, "Backup Database", default_name, "Database Files (*.db)")
        if file_path:
            try:
                shutil.copy(db_path, file_path)
                StyledAlertDialog.show_alert("Backup", "Database backup successful!", "info")
            except Exception as e:
                StyledAlertDialog.show_alert("Backup Error", f"Could not create backup: {e}", "error")

    def restore_database(self):
        reply = QMessageBox.warning(self, "Confirm Restore",
                                     "Restoring from a backup will overwrite ALL current data and restart the application.\n\nAre you sure you want to continue?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Backup File", "", "Database Files (*.db)")
        if file_path:
            db_manager = self.product_processor.db_manager
            db_manager.close_connection()
            try:
                shutil.copy(file_path, db_manager.db_path)
                StyledAlertDialog.show_alert("Restore Successful", 
                                             "Restore successful!\n\nThe application will now close. Please restart it to use the restored data.", 
                                             "info")
                QApplication.instance().quit()
            except Exception as e:
                StyledAlertDialog.show_alert("Restore Error", f"Could not restore database: {e}", "error")
                db_manager.close_and_reopen_connection()