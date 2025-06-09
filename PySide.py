# QApplication: Initializes and manages the GUI app, event loop, and app-wide settings.
    # app = QApplication(sys.argv) : Initializes the Qt application with command-line arguments.
    # show() : Tells Qt to actually display the widget
    # app.exec() : Starts the Qt event loop — this blocks until the app exits. Returns an exit code.
    # QApplication.instance() : is a static method that returns the single, active instance of QApplication. In any running GUI application, there is only one QApplication object.
# QMainWindow: Main window class that supports menus, toolbars, status bars, etc.
    # setWindowTitle() : Sets the window title.
    # resize(WIDTH, HEIGHT) :Sets the initial size of the window
    # setMinimumSize(WIDTH, HEIGHT) : Prevents the window from being resized below a certain size
    # setCentralWidget() : 
# QStackedWidget: Container widget that stacks other widgets on top of each other (like a deck), but only one is visible at a time.
    # setCentralWidget(self.stacked_widget) : Sets it as the central widget of the window
    # setCurrentWidget(): this sets the currently visible widget in the stack
    # self.stacked_widget.currentWidget() : It returns the currently visible widget from the stack.
# QFont: Used to set fonts globally or per widget.
    # QFont("Segoe UI", 10) : creates a font description object. It describes a font that is from the "Segoe UI" family and has a size of 10 points ( font family name(e.g., "Arial", "Times New Roman", "Segoe UI"), Point size(e.g., 10), Weight (e.g., Bold, Normal, Light), Style (e.g., Italic, Oblique), And other properties like underline, strikeout, etc. )
    # app.setFont(font) : This line takes the font description we just created and tells the main application object (app) to use it as the default font. From this point forward, any new widget that doesn't have its own specific font set will automatically inherit and use the font that we initialise
    # setStyle("Fusion") : Sets the UI style to "Fusion", a clean, cross-platform look.
# QGuiApplication: Low-level interface to interact with the system's screens, clipboard, etc.
    # primaryScreen() : ( Gets the main monitor/screen ) This is a static method of the QGuiApplication class. It specifically queries the operating system for the primary display. The primary display is typically the one where the main taskbar or menu bar resides.
# sys : Gives you access to command-line arguments and system-level functions like sys.exit()
# QTimer: Used to delay or schedule something to happen later (like reverting a button style after a short animation).
    # QTimer.singleShot(delay_in_ms, function_to_call) : It's a static method that tells Qt: “Wait for X milliseconds, then call this function one time.”
# QPushButton :
    # clicked : This is the event itself. It's like the physical push of the doorbell button. The button's only job is to announce, "I have been pushed!" It doesn't know or care what happens next.
    # connect : The method that makes the connection
    # self.on_button_click: The "slot" (our method) that will run.
    # emit() : ( fires the signal ) Broadcasts the signal. It actively fires the event and sends data to all listeners
        # self.button.clicked.connect(self.on_button_click)
#



# The addWidget() method in PySide6 (and in Qt in general) is used to add a widget (like a button, label, text box, etc.) to a layout (like QVBoxLayout, QHBoxLayout, QGridLayout, etc.).
# self.original_welcome_login_btn_style = self.welcome_page.content_card.login_button.styleSheet()
    # .styleSheet(): this grabs the current stylesheet of the button — that's how it looks (colors, fonts, borders, etc.).



# getattr(my_object, "attribute_name") : equivalent to my_object.attribute_name. gets an attribute from an object using its name as a string
# setattr(obj, name, value): Sets an attribute. Equivalent to obj.name = value.
# hasattr(obj, name): Checks if an attribute exists. Returns True or False.
# delattr(obj, name): Deletes an attribute. Equivalent to del obj.name.
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
