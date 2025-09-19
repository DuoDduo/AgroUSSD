# src/interface/session_manager.py

class SessionManager:
    def __init__(self):
        self.stack = []              # History of menus/screens navigated
        self.current_user = None     # Currently logged-in user info (dict)
        self.language = "en"         # Default session language

    def push(self, menu_screen):
        # Add the current menu screen to the navigation stack
        self.stack.append(menu_screen)

    def pop(self):
        # Remove the last menu screen from the stack when going back
        if self.stack:
            return self.stack.pop()
        return None

    def top(self):
        # Peek at the current menu screen without removing it
        if self.stack:
            return self.stack[-1]
        return None

    def reset(self):
        # Clear the entire menu stack (e.g., on logout or session end)
        self.stack = []

    def set_user(self, user_info):
        # Store the logged-in user's info in the session
        self.current_user = user_info
        # Update session language if the user has a preferred language
        if isinstance(user_info, dict) and user_info.get("language"):
            self.language = user_info.get("language")

    def clear_user(self):
        # Remove the logged-in user from the session
        self.current_user = None
