from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QLinearGradient, QPalette, QBrush, QFont
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QGroupBox, QLabel, QLineEdit, 
    QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, 
    QScrollArea, QDialog, QGraphicsDropShadowEffect
)
import sys

class ModernGradientWidget(QWidget):
    def __init__(self):
        super().__init__()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 102, 204))   
        gradient.setColorAt(1, QColor(95, 238, 251))  
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)


class StyledGroupBox(QGroupBox):
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        # Ombre portée pour effet 3D
        self.setGraphicsEffect(self.createShadowEffect())
        
    def createShadowEffect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        return shadow


class FeaturesGroupBox(StyledGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()
        
    def setupUI(self):
        self.setStyleSheet("""
            QGroupBox {
                background-color: rgba(13, 71, 161, 0.85);  /* Bleu foncé semi-transparent */
                border-radius: 16px;
                border: none;
                color: white;
            }
        """)
        
        # Utiliser un layout vertical pour une meilleure organisation
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Logo et titre
        header_layout = QHBoxLayout()
        
        # Titre avec typographie moderne
        title_label = QLabel("Trackconnect Pro")
        title_label.setStyleSheet("""
            font-weight: 800;
            font-size: 42px;
            color: white;
            background: transparent;
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Sous-titre
        subtitle = QLabel("Gestion financière interactive et intelligente")
        subtitle.setStyleSheet("""
            font-weight: 300;
            font-size: 18px;
            color: rgba(255, 255, 255, 0.85);
            background: transparent;
            margin-bottom: 10px;
        """)
        layout.addWidget(subtitle)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        layout.addSpacing(20)
        
        # Avantages avec icônes modernes
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
            icon_label.setStyleSheet("""
                font-size: 24px;
                background: transparent;
                margin-right: 10px;
                color : white;
            """)
            
            text_label = QLabel(text)
            text_label.setStyleSheet("""
                font-weight: 400;
                font-size: 18px;
                color: white;
                background: transparent;
            """)
            
            item_layout.addWidget(icon_label)
            item_layout.addWidget(text_label, 1)
            layout.addLayout(item_layout)
            
        # Ajouter un espace extensible à la fin
        layout.addStretch()
        
        # Bouton d'appel à l'action (CTA) au bas de la carte
        self.cta_button = QPushButton("En savoir plus")
        self.cta_button.setStyleSheet("""
            QPushButton {
                background-color: #90CAF9;  /* Bleu très clair */
                color: #0D47A1;  /* Bleu très foncé */
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #BBDEFB;
            }
            QPushButton:pressed {
                background-color: #64B5F6;
            }
        """)
        layout.addWidget(self.cta_button)


class LoginGroupBox(StyledGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUI()
        
    def setupUI(self):
        self.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # En-tête
        header = QLabel("Welcome back")
        header.setStyleSheet("""
            font-weight: 700;
            font-size: 24px;
            color: #0D47A1;  /* Bleu foncé */
        """)
        layout.addWidget(header)
        
        # Sous-titre
        subtitle = QLabel("Sign in to continue")
        subtitle.setStyleSheet("""
            font-weight: 400;
            font-size: 16px;
            color: #1976D2;  /* Bleu moyen */
            margin-bottom: 10px;
        """)
        layout.addWidget(subtitle)
        
        # Fonction pour créer des champs de saisie
        def create_input_field(label_text, placeholder, password=False):
            field_layout = QVBoxLayout()
            field_layout.setSpacing(8)
            
            label = QLabel(label_text)
            label.setStyleSheet("""
                font-weight: 500;
                font-size: 14px;
                color: #1976D2;  /* Bleu moyen */
            """)
            
            input_field = QLineEdit()
            input_field.setPlaceholderText(placeholder)
            if password:
                input_field.setEchoMode(QLineEdit.Password)
            
            input_field.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #BBDEFB;  /* Bleu très clair */
                    border-radius: 10px;
                    padding: 14px;
                    font-size: 15px;
                    background-color: #E3F2FD;  /* Bleu pâle */
                }
                QLineEdit:focus {
                    border: 2px solid #2196F3;  /* Bleu vif */
                    background-color: white;
                }
            """)
            input_field.setMinimumHeight(48)
            
            field_layout.addWidget(label)
            field_layout.addWidget(input_field)
            
            return field_layout, input_field
        
        # Champs de saisie
        email_layout, self.email_input = create_input_field("Email", "Enter your email")
        layout.addLayout(email_layout)
        
        password_layout, self.password_input = create_input_field("Password", "Enter your password", password=True)
        layout.addLayout(password_layout)
        
        # Options "Se souvenir de moi" et "Mot de passe oublié"
        options_layout = QHBoxLayout()
        
        # Option "Se souvenir de moi"
        remember_layout = QHBoxLayout()
        remember_checkbox = QCheckBox()
        remember_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #BBDEFB;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;  /* Bleu vif */
                border: 1px solid #2196F3;
                image: url('check.png');
            }
        """)
        
        remember_text = QLabel("Remember me")
        remember_text.setStyleSheet("""
            font-weight: 400;
            font-size: 14px;
            color: #1976D2;  /* Bleu moyen */
        """)
        
        remember_layout.addWidget(remember_checkbox)
        remember_layout.addWidget(remember_text)
        
        # Option "Mot de passe oublié"
        forgot_password = QPushButton("Forgot password?")
        forgot_password.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2196F3;  /* Bleu vif */
                font-size: 14px;
                font-weight: 600;
                border: none;
                text-align: right;
            }
            QPushButton:hover {
                color: #1565C0;  /* Bleu soutenu */
            }
        """)
        forgot_password.setCursor(Qt.PointingHandCursor)
        
        options_layout.addLayout(remember_layout)
        options_layout.addStretch()
        options_layout.addWidget(forgot_password)
        layout.addLayout(options_layout)
        
        # Espaceur
        layout.addSpacing(20)
        
        # Bouton de connexion
        login_button = QPushButton("Sign in")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #1565C0;  /* Bleu soutenu */
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                padding: 14px;
            }
            QPushButton:hover {
                background-color: #0D47A1;  /* Bleu plus foncé */
            }
            QPushButton:pressed {
                background-color: #0A3D91;  /* Bleu très foncé */
            }
        """)
        login_button.setMinimumHeight(50)
        layout.addWidget(login_button)
        
        # Séparateur "ou"
        or_container = QHBoxLayout()
        
        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_line.setStyleSheet("background-color: #E3F2FD;")
        left_line.setFixedHeight(1)
        
        or_label = QLabel("OR")
        or_label.setStyleSheet("""
            font-size: 14px;
            color: #78909C;
            margin: 0 15px;
        """)
        
        right_line = QFrame()
        right_line.setFrameShape(QFrame.HLine)
        right_line.setStyleSheet("background-color: #E3F2FD;")
        right_line.setFixedHeight(1)
        
        or_container.addWidget(left_line)
        or_container.addWidget(or_label)
        or_container.addWidget(right_line)
        layout.addLayout(or_container)
        
        # Boutons de connexion sociale
        social_layout = QHBoxLayout()
        social_layout.setSpacing(15)
        
        # Fonction pour créer un bouton social
        def create_social_button(icon, name, color):
            button = QPushButton(f"{icon} {name}")
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px;
                }}
                QPushButton:hover {{
                    background-color: {color}D0;
                }}
            """)
            return button
        
                
        # Créer un compte
        signup_layout = QHBoxLayout()
        signup_layout.setAlignment(Qt.AlignCenter)
        
        signup_text = QLabel("Don't have an account?")
        signup_text.setStyleSheet("color: #1976D2; font-size: 14px;")  # Bleu moyen
        
        font =QFont()
        font.setUnderline(True)
        signup_link = QPushButton("Sign up")
        signup_link.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #2196F3;  /* Bleu vif */
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            QPushButton:hover {
                color: #1565C0;  /* Bleu soutenu */
            }
        """)
        signup_link.setCursor(Qt.PointingHandCursor)
        signup_link.setFont(font)
        
        signup_layout.addWidget(signup_text)
        signup_layout.addWidget(signup_link)
        layout.addLayout(signup_layout)
        
        # Ajouter un espace extensible à la fin
        layout.addStretch()


class ProjectInfoDialog(QDialog):
    """Dialogue moderne pour afficher les informations détaillées du projet"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BizTrack360 - Détails du projet")
        self.setMinimumSize(800, 650)
        self.setModal(True)
        
        # Appliquer un style avec des coins arrondis et bordure bleue
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 16px;
                border: 2px solid #1976D2;
            }
        """)
        
        self.setupUI()
        
        # Effet de transition à l'ouverture
        self.setWindowOpacity(0)
        self.fade_in_animation()
        
    def setupUI(self):
        # Layout principal avec marges
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # En-tête avec dégradé
        header = QWidget()
        header.setMinimumHeight(120)
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 #1565C0, stop:1 #42A5F5);
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        # Titre principal sans icône
        title_container = QVBoxLayout()
        
        title = QLabel("BizTrack360")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: white;")
        
        subtitle = QLabel("Application de gestion financière interactive")
        subtitle.setStyleSheet("font-size: 16px; color: rgba(255,255,255,0.85);")
        
        title_container.addWidget(title)
        title_container.addWidget(subtitle)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # Zone de contenu défilante
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: white;
                border: none;
            }
            QScrollBar:vertical {
                background: #F5F5F5;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #BBDEFB;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #90CAF9;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(25)
        
        # Résumé du projet
        summary_title = QLabel("À propos de BizTrack360 :")
        summary_title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #0D47A1;
            margin-top: 5px;
        """)
        
        summary_text = QLabel(
            "BizTrack360 est une application de gestion financière intuitive développée pour les entrepreneurs "
            "et vendeurs de toutes tailles. Découvrez comment elle peut transformer votre business :"
        )
        summary_text.setWordWrap(True)
        summary_text.setStyleSheet("font-size: 16px; color: #424242; line-height: 150%;")
        
        content_layout.addWidget(summary_title)
        content_layout.addWidget(summary_text)
        
        # Nouveaux avantages avec style moderne
        advantages = [
            {
                "title": "Gérez votre activité comme un pro, sans prise de tête",
                "description": "BizTrack360 vous offre un espace centralisé pour tout gérer : vos produits, vos ventes, vos objectifs, votre historique, vos performances. En gros, vous avez tout sous la main, sans avoir besoin de dix applis différentes ou de vous battre avec des tableaux Excel mal foutus. C'est simple, clair, et ça vous fait gagner un temps fou."
            },
            {
                "title": "Des graphiques et des chiffres qui parlent enfin votre langue",
                "description": "Pas besoin d'être analyste pour comprendre vos résultats. L'application transforme vos données en graphiques lisibles et dashboards propres. Vous voyez instantanément quels produits cartonnent, combien vous avez gagné, et si vous êtes sur la bonne voie pour atteindre vos objectifs."
            },
            {
                "title": "Fixez vos objectifs, suivez vos progrès, soyez récompensé",
                "description": "Fixez des objectifs de vente par produit ou globalement, suivez votre progression jour après jour, et recevez une notification dès que vous atteignez un palier. C'est motivant, c'est clair, et surtout… ça vous pousse à vendre mieux, pas juste plus."
            },
            {
                "title": "Des notifications utiles, pas juste du bruit",
                "description": "L'application vous prévient quand votre stock devient critique, quand une vente est enregistrée ou quand un objectif est atteint. Vous restez informé sans devoir surveiller l'écran comme un zombie. Moins de stress, plus de réactivité."
            },
            {
                "title": "Pensée pour les petits entrepreneurs qui veulent aller plus loin",
                "description": "Pas besoin d'avoir une boîte avec 15 employés pour en profiter. Que vous vendiez sur Instagram, dans une boutique, au marché ou en ligne, BizTrack360 vous donne des outils puissants, sans la complexité ni le prix des logiciels de gestion classiques."
            }
        ]
        
        for advantage in advantages:
            # Container pour chaque avantage avec style de carte
            advantage_card = QGroupBox()
            advantage_card.setStyleSheet("""
                QGroupBox {
                    background-color: #F5F9FF;
                    border-radius: 12px;
                    border: 1px solid #E3F2FD;
                    padding: 15px;
                    margin-bottom: 5px;
                }
            """)
            
            card_layout = QVBoxLayout(advantage_card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(10)
            
            # Titre
            title_label = QLabel(advantage["title"])
            title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: 700;
                color: #1565C0;
            """)
            title_label.setWordWrap(True)
            
            # Description
            desc_label = QLabel(advantage["description"])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                font-size: 15px;
                color: #424242;
                line-height: 145%;
            """)
            
            card_layout.addWidget(title_label)
            card_layout.addWidget(desc_label)
            
            content_layout.addWidget(advantage_card)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #E3F2FD; margin: 10px 0;")
        separator.setFixedHeight(1)
        content_layout.addWidget(separator)
        
        # Technologies utilisées
        tech_title = QLabel("Technologies utilisées :")
        tech_title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #0D47A1;
            margin-top: 5px;
        """)
        content_layout.addWidget(tech_title)
        
        technologies = [
            "<b>PySide6</b> (UI)",
            "<b>SQLite3</b> (Base de données locale)",
            "<b>Matplotlib / PyQtGraph</b> (Visualisation)",
            "<b>Python natif</b> (Backend, logique)"
        ]
        
        tech_container = QWidget()
        tech_container.setStyleSheet("""
            background-color: #F5F9FF;
            border-radius: 12px;
            border: 1px solid #E3F2FD;
            padding: 15px;
        """)
        
        tech_grid = QHBoxLayout(tech_container)
        tech_grid.setContentsMargins(20, 15, 20, 15)
        tech_grid.setSpacing(20)
        
        for tech in technologies:
            tech_item = QLabel(tech)
            tech_item.setWordWrap(True)
            tech_item.setStyleSheet("""
                font-size: 15px;
                color: #424242;
                padding: 10px;
                background-color: white;
                border-radius: 8px;
                border: 1px solid #E3F2FD;
            """)
            tech_item.setAlignment(Qt.AlignCenter)
            tech_grid.addWidget(tech_item)
        
        content_layout.addWidget(tech_container)
        
        # Espaceur en bas
        content_layout.addStretch()
        
        # Bouton de fermeture et CTA
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(40, 20, 40, 30)
        
        # Bouton d'inscription
        signup_button = QPushButton("Créer un compte")
        signup_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                padding: 12px 30px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        signup_button.setCursor(Qt.PointingHandCursor)
        
        # Bouton de fermeture
        close_button = QPushButton("Fermer")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #424242;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                padding: 12px 30px;
                border: 1px solid #E0E0E0;
            }
            QPushButton:hover {
                background-color: #EEEEEE;
            }
            QPushButton:pressed {
                background-color: #E0E0E0;
            }
        """)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(signup_button)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        
        # Configuration du scroll area
        scroll_area.setWidget(content_widget)
        
        # Ajout des composants au layout principal
        main_layout.addWidget(header)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(button_container)
    
    def fade_in_animation(self):
        """Animation de fondu à l'ouverture"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BizTrack360 - Login")
        self.setMinimumSize(1200, 800)
        
        # Appliquer une police moderne à l'ensemble de l'application
        font = QFont("Segoe UI", 10)
        QApplication.setFont(font)
        
        # Créer le widget de fond avec dégradé
        self.gradient_widget = ModernGradientWidget()
        self.setCentralWidget(self.gradient_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(self.gradient_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Groupbox des fonctionnalités
        self.features_box = FeaturesGroupBox(self.gradient_widget)
        main_layout.addWidget(self.features_box, 1)
        
        # Connecter le bouton "En savoir plus" à l'action d'ouverture du dialogue
        self.features_box.cta_button.clicked.connect(self.showProjectInfo)
        
        # Groupbox de connexion
        self.login_box = LoginGroupBox(self.gradient_widget)
        main_layout.addWidget(self.login_box, 1)
    
    def showProjectInfo(self):
        """Affiche le dialogue d'information du projet avec animation"""
        info_dialog = ProjectInfoDialog(self)
        info_dialog.exec_()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
    
#     # Appliquer un style global
#     app.setStyle("Fusion")
    
#     window = LoginWindow()
#     window.show()
    
#     sys.exit(app.exec())