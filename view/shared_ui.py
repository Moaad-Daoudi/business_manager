# view/shared_ui.py
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Property, Signal, QSize
from PySide6.QtGui import QColor, QLinearGradient, QPalette, QBrush, QFont, QIcon, QPainter, QPen, QPainterPath
from PySide6.QtWidgets import (
    QWidget, QGroupBox, QLabel, QLineEdit, QFrame, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox, QScrollArea, QDialog,
    QGraphicsDropShadowEffect, QApplication
)

# --- Widgets from welcome_window.py ---

class RoundedButton(QPushButton):
    def __init__(self, text, parent=None, primary=False):
        super().__init__(text, parent)
        self._primary = primary
        # Animation part removed for brevity in this refactor; can be re-added if essential.

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

        if primary:
            base_color = "#0066CC"; hover_color = "#0052A3"; text_color = "white"
        else:
            base_color = "#ffffff"; hover_color = "#f2f2f2"; text_color = "#333333"

        self.setMinimumHeight(55)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Arial", 11, QFont.Bold))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color}; color: {text_color};
                border: none; border-radius: 12px; padding: 15px 25px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {hover_color}; }}
            QPushButton:pressed {{
                padding-top: 17px; padding-bottom: 13px;
                background-color: {hover_color if primary else base_color}; /* Adjust pressed color */
            }}
        """)

class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 25, 25)
        painter.fillPath(path, QColor(255, 255, 255, 240)) # Semi-transparent white
        painter.setPen(QPen(QColor(230, 230, 230), 1)) # Subtle border
        painter.drawPath(path)

class BackgroundWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self) # Public for adding content
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._gradient = QLinearGradient(0, 0, 0, 0) # Initialize
        self._gradient.setColorAt(0, QColor(0, 102, 204))
        self._gradient.setColorAt(1, QColor(95, 238, 251))
        self.setAutoFillBackground(True)
        self._update_palette()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._gradient.setFinalStop(0, self.height())
        self._update_palette()
        self.update()

    def _update_palette(self):
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(self._gradient))
        self.setPalette(palette)


class LogoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255)) # White circle background
        painter.drawEllipse(0, 0, 80, 80)
        painter.setPen(QPen(QColor(0, 102, 204), 5)) # Blue "T"
        painter.drawLine(40, 20, 40, 60)
        painter.drawLine(25, 20, 55, 20)


# --- Widgets from login_window.py / signup_window.py ---

class ModernGradientWidget(QWidget): # Used in Login/Signup pages and Dashboard Sidebar
    def __init__(self):
        super().__init__()
        self._gradient = QLinearGradient(0, 0, 0, 0) # Initialize
        self._gradient.setColorAt(0, QColor(0, 102, 204))
        self._gradient.setColorAt(1, QColor(95, 238, 251))
        self.setAutoFillBackground(True)
        self._update_palette()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._gradient.setFinalStop(0, self.height())
        self._update_palette()

    def _update_palette(self):
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(self._gradient))
        self.setPalette(palette)

class StyledGroupBox(QGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setGraphicsEffect(self.createShadowEffect())

    def createShadowEffect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        return shadow

class FeaturesGroupBox(StyledGroupBox):
    # Signal for "En savoir plus" button
    learn_more_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()

    def setupUI(self):
        self.setStyleSheet("""
            QGroupBox {
                background-color: rgba(13, 71, 161, 0.85);
                border-radius: 16px; border: none; color: white;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30); layout.setSpacing(20)

        header_layout = QHBoxLayout()
        title_label = QLabel("Trackconnect Pro")
        title_label.setStyleSheet("font-weight: 800; font-size: 42px; color: white; background: transparent;")
        header_layout.addWidget(title_label); header_layout.addStretch()
        layout.addLayout(header_layout)

        subtitle = QLabel("Gestion financière interactive et intelligente")
        subtitle.setStyleSheet("font-weight: 300; font-size: 18px; color: rgba(255, 255, 255, 0.85); background: transparent; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        separator = QFrame(); separator.setFrameShape(QFrame.HLine); separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);"); separator.setFixedHeight(1)
        layout.addWidget(separator); layout.addSpacing(20)

        advantages = [
            ("•", "Centralisation de toute la gestion produit et vente"),
            ("•", "Prise de décision plus intelligente grâce aux analyses visuelles"),
            ("•", "Gain de temps monstre"),
            ("•", "Motivation boostée par les objectifs et les notifications"),
            ("•", "Accessible aux petits vendeurs, pas besoin d'être une grosse boîte")
        ]
        for icon, text in advantages:
            item_layout = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 24px; background: transparent; margin-right: 10px; color: white;")
            text_label = QLabel(text)
            text_label.setStyleSheet("font-weight: 400; font-size: 18px; color: white; background: transparent;")
            item_layout.addWidget(icon_label); item_layout.addWidget(text_label, 1)
            layout.addLayout(item_layout)

        layout.addStretch()
        self.cta_button = QPushButton("En savoir plus")
        self.cta_button.setStyleSheet("""
            QPushButton {
                background-color: #90CAF9; color: #0D47A1; border-radius: 10px;
                font-size: 16px; font-weight: 600; padding: 12px;
            }
            QPushButton:hover { background-color: #BBDEFB; }
            QPushButton:pressed { background-color: #64B5F6; }
        """)
        layout.addWidget(self.cta_button)
        self.cta_button.clicked.connect(self.learn_more_clicked.emit) # Emit signal


class ProjectInfoDialog(QDialog):
    signup_action_requested = Signal() # Signal for "Créer un compte"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BizTrack360 - Détails du projet")
        self.setMinimumSize(800, 650)
        self.setModal(True)
        self.setStyleSheet("QDialog { background-color: white; border-radius: 16px; border: 2px solid #1976D2; }")
        self.setupUI()
        self.setWindowOpacity(0) # For fade-in
        self.fade_in_animation()

    def setupUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0); main_layout.setSpacing(0)

        # Header
        header = QWidget(); header.setMinimumHeight(120)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1565C0, stop:1 #42A5F5);
            border-top-left-radius: 14px; border-top-right-radius: 14px;
        """)
        header_layout = QHBoxLayout(header); header_layout.setContentsMargins(30, 20, 30, 20)
        title_container = QVBoxLayout()
        title = QLabel("BizTrack360")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: white;")
        subtitle_dlg = QLabel("Application de gestion financière interactive")
        subtitle_dlg.setStyleSheet("font-size: 16px; color: rgba(255,255,255,0.85);")
        title_container.addWidget(title); title_container.addWidget(subtitle_dlg)
        header_layout.addLayout(title_container); header_layout.addStretch()

        # Scroll Area for Content
        scroll_area = QScrollArea(); scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea { background-color: white; border: none; }
            QScrollBar:vertical { background: #F5F5F5; width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #BBDEFB; border-radius: 5px; }
            QScrollBar::handle:vertical:hover { background: #90CAF9; }
        """)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 30, 40, 30); content_layout.setSpacing(25)

        # Summary
        summary_title = QLabel("À propos de BizTrack360 :"); summary_title.setStyleSheet("font-size: 24px; font-weight: 700; color: #0D47A1; margin-top: 5px;")
        summary_text = QLabel(
            "BizTrack360 est une application de gestion financière intuitive développée pour les entrepreneurs "
            "et vendeurs de toutes tailles. Découvrez comment elle peut transformer votre business :"
        ); summary_text.setWordWrap(True); summary_text.setStyleSheet("font-size: 16px; color: #424242; line-height: 150%;")
        content_layout.addWidget(summary_title); content_layout.addWidget(summary_text)

        # Advantages
        advantages_data = [
            {"title": "Gérez votre activité comme un pro, sans prise de tête", "description": "BizTrack360 vous offre un espace centralisé pour tout gérer : vos produits, vos ventes, vos objectifs, votre historique, vos performances. En gros, vous avez tout sous la main, sans avoir besoin de dix applis différentes ou de vous battre avec des tableaux Excel mal foutus. C'est simple, clair, et ça vous fait gagner un temps fou."},
            {"title": "Des graphiques et des chiffres qui parlent enfin votre langue", "description": "Pas besoin d'être analyste pour comprendre vos résultats. L'application transforme vos données en graphiques lisibles et dashboards propres. Vous voyez instantanément quels produits cartonnent, combien vous avez gagné, et si vous êtes sur la bonne voie pour atteindre vos objectifs."},
            {"title": "Fixez vos objectifs, suivez vos progrès, soyez récompensé", "description": "Fixez des objectifs de vente par produit ou globalement, suivez votre progression jour après jour, et recevez une notification dès que vous atteignez un palier. C'est motivant, c'est clair, et surtout… ça vous pousse à vendre mieux, pas juste plus."},
            {"title": "Des notifications utiles, pas juste du bruit", "description": "L'application vous prévient quand votre stock devient critique, quand une vente est enregistrée ou quand un objectif est atteint. Vous restez informé sans devoir surveiller l'écran comme un zombie. Moins de stress, plus de réactivité."},
            {"title": "Pensée pour les petits entrepreneurs qui veulent aller plus loin", "description": "Pas besoin d'avoir une boîte avec 15 employés pour en profiter. Que vous vendiez sur Instagram, dans une boutique, au marché ou en ligne, BizTrack360 vous donne des outils puissants, sans la complexité ni le prix des logiciels de gestion classiques."}
        ]
        for advantage in advantages_data:
            advantage_card = QGroupBox()
            advantage_card.setStyleSheet("QGroupBox { background-color: #F5F9FF; border-radius: 12px; border: 1px solid #E3F2FD; padding: 15px; margin-bottom: 5px; }")
            card_layout = QVBoxLayout(advantage_card); card_layout.setContentsMargins(20, 20, 20, 20); card_layout.setSpacing(10)
            title_label = QLabel(advantage["title"]); title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #1565C0;"); title_label.setWordWrap(True)
            desc_label = QLabel(advantage["description"]); desc_label.setWordWrap(True); desc_label.setStyleSheet("font-size: 15px; color: #424242; line-height: 145%;")
            card_layout.addWidget(title_label); card_layout.addWidget(desc_label)
            content_layout.addWidget(advantage_card)

        # Separator
        separator = QFrame(); separator.setFrameShape(QFrame.HLine); separator.setStyleSheet("background-color: #E3F2FD; margin: 10px 0;"); separator.setFixedHeight(1)
        content_layout.addWidget(separator)

        # Technologies
        tech_title = QLabel("Technologies utilisées :"); tech_title.setStyleSheet("font-size: 20px; font-weight: 700; color: #0D47A1; margin-top: 5px;")
        content_layout.addWidget(tech_title)
        technologies = ["<b>PySide6</b> (UI)", "<b>SQLite3</b> (Base de données locale)", "<b>Matplotlib / PyQtGraph</b> (Visualisation)", "<b>Python natif</b> (Backend, logique)"]
        tech_container = QWidget(); tech_container.setStyleSheet("background-color: #F5F9FF; border-radius: 12px; border: 1px solid #E3F2FD; padding: 15px;")
        tech_grid = QHBoxLayout(tech_container); tech_grid.setContentsMargins(20, 15, 20, 15); tech_grid.setSpacing(20)
        for tech in technologies:
            tech_item = QLabel(tech); tech_item.setWordWrap(True)
            tech_item.setStyleSheet("font-size: 15px; color: #424242; padding: 10px; background-color: white; border-radius: 8px; border: 1px solid #E3F2FD;")
            tech_item.setAlignment(Qt.AlignCenter); tech_grid.addWidget(tech_item)
        content_layout.addWidget(tech_container)
        content_layout.addStretch()

        # Buttons (bottom)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container); button_layout.setContentsMargins(40, 20, 40, 30)
        self.signup_button_dlg = QPushButton("Créer un compte")
        self.signup_button_dlg.setStyleSheet("""
            QPushButton { background-color: #1976D2; color: white; border-radius: 8px;
                          font-size: 16px; font-weight: 600; padding: 12px 30px; }
            QPushButton:hover { background-color: #1565C0; }
            QPushButton:pressed { background-color: #0D47A1; }
        """); self.signup_button_dlg.setCursor(Qt.PointingHandCursor)
        self.signup_button_dlg.clicked.connect(self._emit_signup_action) # Connect to emit signal

        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("""
            QPushButton { background-color: #F5F5F5; color: #424242; border-radius: 8px;
                          font-size: 16px; font-weight: 600; padding: 12px 30px; border: 1px solid #E0E0E0; }
            QPushButton:hover { background-color: #EEEEEE; }
            QPushButton:pressed { background-color: #E0E0E0; }
        """); close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.accept) # Closes the dialog

        button_layout.addWidget(self.signup_button_dlg); button_layout.addStretch(); button_layout.addWidget(close_button)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(header); main_layout.addWidget(scroll_area); main_layout.addWidget(button_container)

    def _emit_signup_action(self):
        self.signup_action_requested.emit()
        self.accept() # Close dialog after emitting

    def fade_in_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(250); self.animation.setStartValue(0); self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad); self.animation.start()
        
# view/shared_ui.py
# ... (other imports: QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, Qt, QFont, QColor)

# (Keep RoundedButton, RoundedWidget, BackgroundWidget, LogoWidget, ModernGradientWidget,
# StyledGroupBox, FeaturesGroupBox, ProjectInfoDialog as they are)


# --- NEW: Styled Alert Dialog ---
class StyledAlertDialog(QDialog):
    def __init__(self, title, message, alert_type="info", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(450)
        self.setModal(True)

        # Base styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0; /* Lighter border */
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header (colored based on alert_type)
        header_widget = QWidget()
        header_widget.setMinimumHeight(60) # Reduced header height
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 15, 20, 15)

        icon_label = QLabel() # For icon
        icon_label.setFixedSize(28, 28)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        if alert_type == "error":
            header_bg_color = "#FFEBEE" # Light red
            header_text_color = "#D32F2F" # Darker red
            icon_char = "✕" # Or use an SVG/PNG icon
            icon_font_size = "20px"
        elif alert_type == "warning":
            header_bg_color = "#FFF9C4" # Light yellow
            header_text_color = "#FBC02D" # Darker yellow
            icon_char = "⚠"
            icon_font_size = "20px"
        else: # info
            header_bg_color = "#E3F2FD" # Light blue
            header_text_color = "#1976D2" # Darker blue
            icon_char = "ℹ"
            icon_font_size = "20px"

        header_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {header_bg_color};
                border-top-left-radius: 11px;
                border-top-right-radius: 11px;
            }}
        """)

        icon_label.setText(icon_char)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {header_text_color};
                font-size: {icon_font_size};
                font-weight: bold;
                background-color: transparent;
            }}
        """)

        self.title_label_dlg = QLabel(title) # Renamed to avoid conflict
        self.title_label_dlg.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: 600;
                color: {header_text_color};
                background-color: transparent;
            }}
        """)

        header_layout.addWidget(icon_label)
        header_layout.addSpacing(10)
        header_layout.addWidget(self.title_label_dlg)
        header_layout.addStretch()

        main_layout.addWidget(header_widget)

        # Message content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 20, 25, 25) # Increased padding
        content_layout.setSpacing(15)

        self.message_label_dlg = QLabel(message) # Renamed to avoid conflict
        self.message_label_dlg.setWordWrap(True)
        self.message_label_dlg.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #424242; /* Dark grey for message */
                line-height: 140%;
            }
        """)
        content_layout.addWidget(self.message_label_dlg)
        main_layout.addWidget(content_widget)

        # Footer with OK button
        footer_widget = QWidget()
        footer_widget.setStyleSheet("background-color: #F5F5F5; border-bottom-left-radius: 11px; border-bottom-right-radius: 11px;")
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        footer_layout.addStretch()

        self.ok_button = QPushButton("OK")
        self.ok_button.setMinimumHeight(36)
        self.ok_button.setMinimumWidth(90)
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {header_text_color}; /* Use header text color for button */
                color: white;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {QColor(header_text_color).darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {QColor(header_text_color).darker(120).name()};
            }}
        """)
        self.ok_button.clicked.connect(self.accept)
        footer_layout.addWidget(self.ok_button)

        main_layout.addWidget(footer_widget)
        self.adjustSize() # Adjust dialog size to content

    @staticmethod
    def show_alert(title, message, alert_type="info", parent=None):
        dialog = StyledAlertDialog(title, message, alert_type, parent)
        return dialog.exec()

# --- QLineEdit Stylesheet Update (within LoginGroupBox/SignupGroupBox or globally) ---
# We will apply this dynamically. The base style will be in the GroupBox classes.
# An "error" property will be added to QLineEdit to trigger the red border.

# QLineEdit base style (example for login/signup forms)
# This will be part of the create_input_field function in login_window.py and signup_window.py
BASE_LINE_EDIT_STYLE = """
    QLineEdit {
        border: 1px solid #BBDEFB; /* Default border */
        border-radius: 10px;
        padding: 12px;
        font-size: 15px;
        background-color: #E3F2FD;
    }
    QLineEdit:focus {
        border: 2px solid #2196F3; /* Focus border */
        background-color: white;
    }
    QLineEdit[error="true"] { /* Style for error state */
        border: 2px solid #D32F2F; /* Red border for error */
        background-color: #FFEBEE; /* Light red background for error */
    }
"""