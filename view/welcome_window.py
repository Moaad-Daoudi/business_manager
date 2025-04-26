from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, 
                              QVBoxLayout, QPushButton, QGraphicsDropShadowEffect)
from PySide6.QtGui import QColor, QLinearGradient, QFont, QIcon, QPainter, QPen, QPainterPath
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Property


class RoundedButton(QPushButton):
    def __init__(self, text, parent=None, primary=False):
        super().__init__(text, parent)
        self._primary = primary
        self._animation = QPropertyAnimation(self, b"color_alpha")
        self._animation.setDuration(200)
        self._animation.setStartValue(0)
        self._animation.setEndValue(40)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._color_alpha = 0
        
        # Effet d'ombre
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        # Style du bouton
        if primary:
            base_color = "#0066CC"  # Bleu professionnel
            hover_color = "#0052A3"
            text_color = "white"
        else:
            base_color = "#ffffff"
            hover_color = "#f2f2f2"
            text_color = "#333333"
            
        self.setMinimumHeight(55)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Arial", 11, QFont.Bold))
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: {text_color};
                border: none;
                border-radius: 12px;
                padding: 15px 25px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            
            QPushButton:pressed {{
                padding-top: 17px;
                padding-bottom: 13px;
            }}
        """)
        
    def get_color_alpha(self):
        return self._color_alpha
        
    def set_color_alpha(self, alpha):
        self._color_alpha = alpha
        self.update()
        
    color_alpha = Property(int, get_color_alpha, set_color_alpha)
    
    def enterEvent(self, event):
        self._animation.setDirection(QPropertyAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self._animation.setDirection(QPropertyAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)

class RoundedWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Création du chemin du rectangle arrondi
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 25, 25)
        
        # Remplissage avec un fond blanc semi-transparent
        painter.fillPath(path, QColor(255, 255, 255, 240))
        
        # Dessin d'une bordure subtile
        painter.setPen(QPen(QColor(230, 230, 230), 1))
        painter.drawPath(path)

class BackgroundWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Créer un dégradé avec les couleurs spécifiées
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 102, 204))   # Bleu foncé en haut
        gradient.setColorAt(1, QColor(95, 238, 251))  # Bleu clair en bas
        
        # Dessiner le fond dégradé
        painter.fillRect(self.rect(), gradient)

class LogoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 80)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fond circulaire
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(0, 0, 80, 80)
        
        # Dessin d'un logo "T" simplifié
        painter.setPen(QPen(QColor(0, 102, 204), 5))  # Utiliser la même couleur bleue que le dégradé
        painter.drawLine(40, 20, 40, 60)  # Ligne verticale
        painter.drawLine(25, 20, 55, 20)  # Ligne horizontale

class ContentWidget(RoundedWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 600)
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)
        self.layout.setAlignment(Qt.AlignTop)
        
        # Logo
        self.logo = LogoWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(self.logo)
        self.layout.addLayout(logo_layout)
        self.layout.addSpacing(10)
        
        # Titre
        self.label = QLabel("Track App", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            font-family: 'Arial';
            font-size: 38px;
            font-weight: bold;
            color: #0066CC;
            margin-bottom: 10px;
        """)
        self.layout.addWidget(self.label)
        
        # Description
        self.label2 = QLabel("Welcome to our tracking application."
                            "Manage your tasks, track your progress and "
                            "achieve your goals with our intuitive interface.", self)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setWordWrap(True)
        self.label2.setStyleSheet("""
            font-family: 'Arial';
            font-size: 16px;
            color: #555555;
            margin-bottom: 20px;
            line-height: 150%;
        """)
        self.layout.addWidget(self.label2)
        
        # Espace
        self.layout.addSpacing(40)
        
        # Boutons
        self.login = RoundedButton("Login", self, primary=True)
        self.layout.addWidget(self.login)
        
        self.layout.addSpacing(15)
        
        self.register = RoundedButton("Sign up", self)
        self.layout.addWidget(self.register)
        
        # Ajout d'informations de version en bas
        self.version_label = QLabel("Version 1.0.1", self)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet("""
            font-family: 'Arial';
            font-size: 12px;
            color: #777777;
            margin-top: 20px;
        """)
        self.layout.addStretch()
        self.layout.addWidget(self.version_label)
        
class WelcomeWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track App")
        
        # Création du widget avec gradient bleu pour l'arrière-plan
        background_widget = BackgroundWidget()
        
        # Création du widget de contenu et ajout à l'arrière-plan
        self.content = ContentWidget()
        background_widget.layout.addWidget(self.content)
        
        # Définition du widget principal
        self.setCentralWidget(background_widget)
        
        # Propriétés de la fenêtre
        self.resize(800, 700)
        self.setMinimumSize(640, 680)
        
        # Centrer la fenêtre sur l'écran
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

# if __name__ == "__main__":
#     app = QApplication([])
    
#     # Définition d'une police pour toute l'application
#     # font = QFont("Arial", 10)
#     # app.setFont(font)
    
#     window = WelcomeWindow()  
#     window.show()
    
#     app.exit(app.exec())