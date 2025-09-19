# src/interfaces/base_interface.py
from abc import ABC, abstractmethod
from utils.translators import translate

class USSDInterface(ABC):
    MAX_OPTIONS = 8

    def __init__(self, session, language: str = None, user: dict = None):
        self.session = session
        # prefer explicit language, otherwise session.language, otherwise 'en'
        self.language = language or getattr(session, "language", "en")
        self.user = user
        # if user has a preferred language, override
        if self.user and isinstance(self.user, dict) and self.user.get("language"):
            self.language = self.user.get("language")

    @abstractmethod
    def render(self):
        pass

    def validate_choice(self, choice: str, max_opt: int):
        special = ["*0", "*9", "#00"]
        if choice in special:
            return choice
        if not choice.isdigit():
            print(translate("invalid_input", self.language))
            return None
        i = int(choice)
        if 1 <= i <= max_opt:
            return i
        print(translate("invalid_input", self.language))
        return None

    def t(self, key: str):
        return translate(key, self.language)
