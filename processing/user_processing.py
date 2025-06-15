class UserProcessor:
    def __init__(self, db_manager):  
        self.db_manager = db_manager 

    def register_new_user(self, name, email, password):
        if not all([name, email, password]):
            return False, "All fields (name, email, password) are required."
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        success, message = self.db_manager.add_user(name, email, password)
        return success, message

    def authenticate_user(self, email, password):
        if not all([email, password]):
            return False, "Email and password are required.", None

        user = self.db_manager.get_user_by_email(email)
        if user:
            if self.db_manager.verify_password(user["password_hash"], password):
                safe_user_data = {"id": user["id"], "name": user["name"], "email": user["email"]}
                return True, "Login successful.", safe_user_data
            else:
                return False, "Invalid email or password.", None
        else:
            return False, "Invalid email or password.", None
        

    def update_user_details(self, user_id, new_data):
        """Updates user's name and email."""
        if not user_id or not new_data.get('name') or not new_data.get('email'):
            return False, "Name and email cannot be empty."
        
        return self.db_manager.update_user(user_id, new_data)

    def change_password(self, user_id, old_password, new_password):
        """Changes a user's password after verifying the old one."""
        if not all([user_id, old_password, new_password]):
            return False, "All password fields are required."
        if len(new_password) < 8:
            return False, "New password must be at least 8 characters long."
            
        user = self.db_manager.get_user_by_id(user_id)
        if not user:
            return False, "User not found."
            
        if not self.db_manager.verify_password(user['password_hash'], old_password):
            return False, "The old password you entered is incorrect."
            
        update_data = {'password': new_password}
        return self.db_manager.update_user(user_id, update_data)