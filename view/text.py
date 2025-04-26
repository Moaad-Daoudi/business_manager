from PySide6.QtGui import QColor, QLinearGradient, QPalette, QBrush
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QGroupBox, QLabel, QLineEdit, QFrame, QPushButton

class GradientWidget(QWidget):
    def __init__(self):
        super().__init__()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 102, 204))   
        gradient.setColorAt(1, QColor(95, 238, 251))  
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class Groupbox_Widget(QGroupBox):
    def __init__(self):
        super().__init__()   
        self.setStyleSheet("color: white; background-color: #38BDF8;")
        self.setGeometry(200, 50, 575, 700)

        label = QLabel("🔥 Trackconnect Pro", self) # self is passed as the parent of the QLabel. In this case, self refers to the instance of the Groupbox_Widget class
        label.setStyleSheet("font-weight: 900; font-size: 40px")
        label.move(100, 200)
        
        advantages = QLabel(
            "• Fast and smart job matching\n\n"
            "• Real-time market insights with AI\n\n"
            "• Advanced sentiment analysis\n\n"
            "• Fully customizable experience\n\n"
            "• Perfect for small businesses and job seekers", self)
        advantages.setStyleSheet("font-weight: 400; font-size: 20px;")
        advantages.move(170, 300)
        
        
        
class Group_Widget2(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("color: black; background-color: white;")
        self.setGeometry(775, 50, 575, 700)  # Set x, y, width, height

        # Add a layout and content
        label = QLabel("Sign up for free to track your product", self)
        label.setStyleSheet("font-weight: 700; font-size: 20px;")
        label.move(120, 150)
        
        frame = QFrame(self)
        frame.setGeometry(50, 200, 500, 700)  # Set x, y, width, height
        frame.setStyleSheet("background-color: transparent;")  # No border for the frame

        name_label = QLabel("What should we call you?", frame)
        name_label.setStyleSheet("font-weight:400;")
        name_label.move(10, 20)

        name_input = QLineEdit(frame)
        name_input.setPlaceholderText("Enter your name")
        name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid lightgray;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        name_input.setGeometry(10, 50, 450, 30)
        
        email_label = QLabel("What's your email?", frame)
        email_label.setStyleSheet("font-weight: 400;")
        email_label.move(10, 100)
        
        email_input = QLineEdit(frame)
        email_input.setPlaceholderText("Enter your email")
        email_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid lightgray;
                border-radius: 10px;
                padding: 5px;
            }  
            """)
        email_input.setGeometry(10, 130, 450, 30)
        
        password_label = QLabel("Create a password", frame)
        password_label.setStyleSheet("font-weight: 400;")
        password_label.move(10, 180)
        
        password_input = QLineEdit(frame)
        password_input.setPlaceholderText("Enter your password")
        password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid lightgray;
                border-radius: 10px;
                padding: 5px;
            }  
            """)
        password_input.setGeometry(10, 210, 450, 30)
        description_password = QLabel("Use 8 or more characters with a mix of letters, numbers & symbols", frame)
        description_password.setStyleSheet("font-weight: 200;")
        description_password.move(10, 250)
        
        policy = QLabel("By creating an account, you agree to the Terms of use and Privacy Policy.", frame)
        policy.setStyleSheet("font-weight: 400;")
        policy.move(10, 300)
        
        botton = QPushButton("Create an account", frame)
        botton.setStyleSheet("background-color: gray; color: white; border-radius: 12px; font-size: 16px;")
        botton.setGeometry(70, 320, 320, 50)
        
class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to my app")
        self.resize(900, 800)

        # Create the gradient background
        gradient_widget = GradientWidget()
        self.setCentralWidget(gradient_widget)

        # Add the group box with absolute positioning
        box = Groupbox_Widget()
        box.setParent(gradient_widget)  # Set the parent to the gradient widget
        
        box2 = Group_Widget2()
        box2.setParent(gradient_widget)

if __name__ == "__main__": 
    app = QApplication([]) 
    window = MainWindow()    
    window.show()            
    app.exec()
