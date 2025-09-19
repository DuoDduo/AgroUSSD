# src/main.py
from interface.session_manager import SessionManager
from interface.language_menu import LanguageMenu
from interface.main_menu import MainMenu
from utils.translators import translate

def run():
    session = SessionManager()

    # Show USSD dial + language selection first
    lang_menu = LanguageMenu(session)
    lang_menu.render()

    # Now continue with the main menu using selected language
    menu = MainMenu(session)
    try:
        menu.render_loop()
    except SystemExit:
        lang = getattr(session, "language", "en")
        print(translate("thank_you_bye", lang))

if __name__ == "__main__":
    run()
