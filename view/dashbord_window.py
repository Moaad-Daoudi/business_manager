from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QColor, QLinearGradient, QPalette, QBrush, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QHBoxLayout, QListWidget, QVBoxLayout,
    QPushButton, QSpacerItem, QSizePolicy
)
import sys
from welcome_window import LogoWidget

class ModernGradientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.updateGradient()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGradient()
    
    def updateGradient(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 102, 204))
        gradient.setColorAt(1, QColor(95, 238, 251))
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class Layout(QWidget):
    def __init__(self):
        super().__init__()
        # Layout principal
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Widget sidebar avec gradient
        self.sidebar_widget = ModernGradientWidget()
        self.sidebar_widget.setFixedWidth(200)

        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignTop) # Garder l'alignement en haut pour les boutons
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(20)

        # Ajouter un espace flexible en haut pour pousser le logo vers le centre
        self.sidebar_layout.addStretch(1)

        # Créer et ajouter le LogoWidget
        self.logo_widget_sidebar = LogoWidget()
        self.sidebar_layout.addWidget(self.logo_widget_sidebar, alignment=Qt.AlignCenter)

        # Ajouter un espace flexible après le logo pour le pousser vers le centre
        self.sidebar_layout.addStretch(1)
        self.sidebar_layout.addItem(QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        

        # Création des boutons de la sidebar en blanc
        sidebar_buttons = ["    Dashbord", "    Product", "   Sales",
                           "    Goals", "    History", "    Notifications", "    Profile", "    Setting", "    Log out"]

        for button_name in sidebar_buttons:
            button = QPushButton(button_name)
            button.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 8px 16px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """)
            icon = QIcon(f"assets/{button_name.strip()}.png")
            button.setIcon(icon)
            self.sidebar_layout.addWidget(button)
            if button_name == "Setting" :
                self.sidebar_layout.addItem(QSpacerItem(0, 230, QSizePolicy.Minimum, QSizePolicy.Fixed))
            else :
                self.sidebar_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Ajouter un widget extensible à la fin pour pousser les boutons vers le haut
        self.sidebar_layout.addStretch(5)

        # Widget et layout de contenu
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        # Ajout des widgets au layout principal
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget, 1)
        
class DashbordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(1200, 800)
        
        # Créer le widget avec un fond blanc pour le contenu principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Appliquer le layout avec sidebar et contenu
        self.layout_widget = Layout()
        
        # Ajouter le layout au widget central
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.layout_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Appliquer un style global
    app.setStyle("Fusion")

    window = DashbordWindow()
    window.show()

    sys.exit(app.exec())