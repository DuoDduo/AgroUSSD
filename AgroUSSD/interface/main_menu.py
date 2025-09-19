from .base_interface import USSDInterface
from services.user_service import UserService
from interface.farmer_menu import FarmerMenu
from interface.buyer_menu import BuyerMenu
from utils.validate import input_pin, input_phone
from utils.translators import translate
from utils.validate import input_phone, input_pin, input_non_empty_text, input_positive_float, input_crops_list


class MainMenu(USSDInterface):
    def __init__(self, session, input_fn=input, print_fn=print):
        super().__init__(session)
        self.input_function = input_fn        # Function to read user input
        self.print_function = print_fn        # Function to display messages
        self.user_service = UserService()     # Service for registration and authentication

        # Ask user to select language if session does not already have one
        if not getattr(session, "language", None):
            self.prompt_language_selection()

    # Ask user to select preferred language
    def prompt_language_selection(self):
        self.print_function("Select Language / Yan Ede / Họrọ Asụsụ / Zaɓi Harshe:")
        language_options = ["English", "Yoruba", "Igbo", "Hausa", "Pidgin"]

        # Display all language options
        for option_index, language_name in enumerate(language_options, start=1):
            self.print_function(f"{option_index}. {language_name}")

        user_choice = self.input_function(">").strip()

        # Map user input to language code
        language_mapping = {"1": "en", "2": "yo", "3": "ig", "4": "ha", "5": "pi"}
        selected_language_code = language_mapping.get(user_choice, "en")
        self.language = selected_language_code
        self.session.language = selected_language_code

        # Confirm language selection
        self.print_function(f"Language set to {language_options[int(user_choice)-1].upper()}.")

    # Translate a text key to the current language
    def translate_text(self, key: str):
        return translate(key, self.language)

    # Display main menu and handle user input
    def render(self):
        # Display translated menu options
        self.print_function(
            f"{self.translate_text('welcome_message')}\n"
            f"1. {self.translate_text('register_farmer')}\n"
            f"2. {self.translate_text('register_buyer')}\n"
            f"3. {self.translate_text('login')}\n"
            f"4. {self.translate_text('browse_market_prices')}\n"
            f"5. {self.translate_text('search_farmers')}\n"
            f"6. {self.translate_text('exit')}"
        )

        # Get user input and validate
        user_input = self.input_function(self.translate_text("menu_prompt") + ": ").strip()
        validated_choice = self.validate_choice(user_input, 6)

        # Handle navigation shortcuts
        if validated_choice in ("*0", "*9"):  # Go back / home
            return
        if validated_choice in ("#00", 6):  # Exit the app
            self.print_function(self.translate_text("thank_you_bye"))
            raise SystemExit

        # Option 1: Register Farmer
        if validated_choice == 1:
            
            farmer_name = input_non_empty_text(self.input_function, "Enter your Name: ")
            farmer_phone = input_phone(self.input_function, "Enter your Phone Number (0XXXXXXXXXX): ")
            farmer_location = input_non_empty_text(self.input_function, "Enter your Location: ")
            farm_size_in_acres = input_positive_float(self.input_function, "Enter your Farm Size in acres: ")
            primary_crops_list = input_crops_list(self.input_function, "Enter your Primary Crops (comma separated): ")
            farmer_pin = input_pin(self.input_function, "Enter your 4 or 6-digit PIN: ")



            try:
                registered_farmer = self.user_service.register_farmer(
                    name = farmer_name,
                    phone = farmer_phone,
                    location = farmer_location,
                    pin = farmer_pin,
                    farm_size = farm_size_in_acres,
                    primary_crops =primary_crops_list
                )
                self.print_function(f"{self.translate_text('farmer_registered')}: {registered_farmer.name} ({registered_farmer.phone})")
            except Exception as error_message:
                self.print_function(f"{self.translate_text('error')}: {error_message}")

        # Option 2: Register Buyer
        elif validated_choice == 2:
            buyer_name = self.input_function(self.translate_text("enter_name")).strip()
            buyer_phone = input_phone(self.input_function, self.translate_text("enter_phone"))
            buyer_location = self.input_function(self.translate_text("enter_location")).strip()
            business_name = self.input_function(self.translate_text("enter_business_name")).strip() or None
            buyer_pin = input_pin(self.input_function)

            try:
                registered_buyer = self.user_service.register_buyer(
                    name=buyer_name,
                    phone=buyer_phone,
                    location=buyer_location,
                    pin=buyer_pin,
                    business_name=business_name
                )
                self.print_function(f"{self.translate_text('buyer_registered')}: {registered_buyer.name} ({registered_buyer.phone})")
            except Exception as error_message:
                self.print_function(f"{self.translate_text('error')}: {error_message}")

        # Option 3: Login
        elif validated_choice == 3:
            login_phone = input_phone(self.input_function, self.translate_text("enter_phone"))
            login_pin = self.input_function(self.translate_text("enter_pin")).strip()
            authenticated_user = self.user_service.authenticate(phone=login_phone, pin=login_pin)

            if not authenticated_user:
                self.print_function(self.translate_text("invalid_credentials"))
                return

            # Store logged-in user in session
            self.session.set_user(authenticated_user)

            # Redirect user to appropriate menu
            if authenticated_user.get("type") == "farmer_role":
                FarmerMenu(self.session, self.input_function, self.print_function).render_loop()
            else:
                BuyerMenu(self.session, self.input_function, self.print_function).render_loop()

        # Option 4: Browse Market Prices
        elif validated_choice == 4:
            from services.market_service import MarketService
            market_service = MarketService()
            product_name = self.input_function(self.translate_text("enter_product_name")).strip()
            product_price_comparison = market_service.compare_prices(product_name)

            if not product_price_comparison:
                self.print_function(self.translate_text("no_market_data"))
            else:
                for product_info in product_price_comparison:
                    self.print_function(f"{product_info['location']}: ₦{product_info['price']}")

        # Option 5: Search Farmers
        elif validated_choice == 5:
            search_location = self.input_function(self.translate_text("search_location")).strip() or None
            search_product = self.input_function(self.translate_text("search_product")).strip() or None
            matched_farmers = self.user_service.list_farmers(location=search_location, product=search_product)

            if not matched_farmers:
                self.print_function(self.translate_text("no_farmers_found"))
            else:
                for farmer in matched_farmers:
                    self.print_function(
                        f"{farmer['name']} - {farmer['phone']} - {farmer['location']} - "
                        f"{self.translate_text('crops')}: {', '.join(farmer.get('primary_crops', []))}"
                    )

        else:
            # Invalid menu selection
            self.print_function(self.translate_text("invalid_choice"))

    # Keep displaying the menu until user exits
    def render_loop(self):
        while True:
            self.render()
