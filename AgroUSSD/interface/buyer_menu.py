from .base_interface import USSDInterface
from services.user_service import UserService
from services.harvest_service import HarvestService
from services.connection_service import ConnectionService


class BuyerMenu(USSDInterface):
    def __init__(self, session, input_fn=input, print_fn=print, language="en"):
        super().__init__(session, language)
        self.input_function = input_fn           # Function to read user input
        self.print_function = print_fn           # Function to display messages
        self.user_service = UserService(language=self.language)  # Handle user-related operations
        self.harvest_service = HarvestService(language=self.language)  # Handle harvest offers
        self.connection_service = ConnectionService(language=self.language)  # Handle buyer-farmer connections

    # Display the buyer menu and handle input
    def render(self):
        current_user = self.session.current_user

        # Display localized buyer menu
        self.print_function(
            f"{self.t('hello')} {current_user.get('name')} ({self.t('buyer')})\n"
            f"1. {self.t('search_produce')}\n"
            f"2. {self.t('browse_farmers')}\n"
            f"3. {self.t('contact_farmer')}\n"
            f"4. {self.t('logout')}"
        )

        # Read user menu selection
        user_input = self.input_function(f"{self.t('select_option')}: ").strip()
        validated_choice = self.validate_choice(user_input, 4)  # Validate input

        # Handle special navigation options
        if validated_choice == "*0":  # Go back
            return
        if validated_choice == "*9":  # Go to main menu
            return
        if validated_choice in ("#00", 4):  # Logout
            self.session.clear_user()
            self.print_function(self.t("logged_out"))
            return

        # Option 1: Search available produce
        if validated_choice == 1:
            product_name = self.input_function(f"{self.t('enter_product_name')}: ").strip()
            preferred_location = self.input_function(f"{self.t('preferred_location_optional')}: ").strip() or None

            search_results = self.harvest_service.search_harvests(
                product_name=product_name,
                location=preferred_location,
                users_service=self.user_service
            )

            if not search_results or not search_results.get("harvests"):
                self.print_function(self.t("no_offers_found"))
            else:
                for harvest in search_results["harvests"]:
                    farmer_info = self.user_service.get_user(harvest["farmer_phone"])
                    self.print_function(
                        f"{harvest['product_name']} {harvest['quantity']}u - "
                        f"{self.t('asking_price')} ₦{harvest['asking_price']} - "
                        f"{self.t('farmer')}: {farmer_info.get('name')} ({farmer_info.get('phone')})"
                    )

        # Option 2: Browse farmers
        elif validated_choice == 2:
            search_location = self.input_function(f"{self.t('enter_location_optional')}: ").strip() or None
            farmers_list = self.user_service.list_farmers(location=search_location)

            if not farmers_list:
                self.print_function(self.t("no_farmers"))
            else:
                for farmer in farmers_list:
                    self.print_function(
                        f"{farmer['name']} - {farmer['phone']} - "
                        f"{self.t('crops')}: {', '.join(farmer.get('primary_crops', []))}"
                    )

        # Option 3: Contact a farmer
        elif validated_choice == 3:
            farmer_phone_number = self.input_function(f"{self.t('enter_farmer_phone')}: ").strip()
            farmer_harvests = self.harvest_service.list_harvests(farmer_phone=farmer_phone_number)

            if not farmer_harvests or not farmer_harvests.get("harvests"):
                self.print_function(self.t("no_harvests_for_farmer"))
            else:
                first_harvest = farmer_harvests["harvests"][0]  # pick the first available harvest
                self.connection_service.record_connection(
                    buyer_phone=current_user["phone"],
                    farmer_phone=farmer_phone_number,
                    harvest_id=first_harvest["id"]
                )
                farmer_info = self.user_service.get_user(farmer_phone_number)
                self.print_function(
                    f"{self.t('contact_recorded')} "
                    f"{self.t('farmer_number')}: {farmer_info.get('phone')}"
                )

        # Invalid menu option
        else:
            self.print_function(self.t("invalid_choice"))

    # Keep displaying the menu until user logs out
    def render_loop(self):
        while self.session.current_user:
            self.render()
