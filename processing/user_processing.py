# processing/user_processing.py
# from model.user_database_manager import UserDatabaseManager # Injected

class UserProcessor:
    def __init__(self, user_db_manager): # Expect UserDatabaseManager instance
        self.user_db_manager = user_db_manager # Changed attribute name for clarity

    def register_new_user(self, name, email, password):
        if not all([name, email, password]):
            return False, "All fields (name, email, password) are required."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        success, message = self.user_db_manager.add_user(name, email, password)
        return success, message

    def authenticate_user(self, email, password):
        if not all([email, password]):
            return False, "Email and password are required.", None

        user = self.user_db_manager.get_user_by_email(email)
        if user:
            if self.user_db_manager.verify_password(user["password_hash"], password):
                safe_user_data = {"id": user["id"], "name": user["name"], "email": user["email"]}
                return True, "Login successful.", safe_user_data
            else:
                return False, "Invalid email or password.", None
        else:
            return False, "Invalid email or password.", None