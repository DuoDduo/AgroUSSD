# src/interface/language_menu.py
class LanguageMenu:
    def __init__(self, session, input_fn=input, print_fn=print):
        self.session = session
        self.input_function = input_fn      # Function to read user input
        self.print_function = print_fn      # Function to display messages

    # Display USSD welcome and language selection menu
    def render(self):
        # Step 1: Prompt user to dial the USSD code
        while True:
            self.print_function("\nWelcome to AgroUSSD")
            self.print_function("Dial *882# to start (or type 'exit' to quit):")
            dialed_code = self.input_function("> ").strip()

            if dialed_code.lower() == "exit":
                self.print_function("Goodbye.")
                raise SystemExit

            if dialed_code == "*882#":
                break  # Correct USSD code entered

            self.print_function("Invalid USSD code. Please dial *882# to continue.")

        # Step 2: Language selection
        self.print_function("\nSelect Language / Yan Ede / Họrọ Asụsụ / Zaɓi Harshe:")
        language_options = ["English", "Yoruba", "Igbo", "Hausa", "Pidgin"]

        for index, language in enumerate(language_options, start=1):
            self.print_function(f"{index}. {language}")

        selected_option = self.input_function("> ").strip()

        # Map selection to language code
        language_mapping = {
            "1": "en",
            "2": "yo",
            "3": "ig",
            "4": "ha",
            "5": "pi"
        }
        chosen_language_code = language_mapping.get(selected_option, "en")
        self.session.language = chosen_language_code

        # If a user is logged in, update their language preference too
        if hasattr(self.session, "current_user") and isinstance(self.session.current_user, dict):
            self.session.current_user["language"] = chosen_language_code

        # Confirm language selection
        self.print_function(f"\nLanguage set to {chosen_language_code.upper()}.\n")
