from .base_interface import USSDInterface
from services.user_service import UserService
from services.harvest_service import HarvestService
from services.connection_service import ConnectionService
from utils.validate import input_non_empty_text

class BuyerMenu(USSDInterface):
    def __init__(self, session, input_fn=input, print_fn=print, language="en"):
        super().__init__(session, language)
        self.input_function = input_fn
        self.print_function = print_fn
        self.user_service = UserService(language=self.language)
        self.harvest_service = HarvestService(language=self.language)
        self.connection_service = ConnectionService(language=self.language)

    # Render buyer menu and handle user input
    def render(self):
        current_user = self.session.current_user

        # Display buyer menu
        self.print_function(
            f"\n{self.t('hello')} {current_user.get('name')} ({self.t('buyer')})"
            f"\n1. {self.t('search_produce')}"
            f"\n2. {self.t('browse_farmers')}"
            f"\n3. {self.t('contact_farmer')}"
            f"\n4. {self.t('logout')}"
        )

        user_choice = self.input_function(f"{self.t('select_option')}: ").strip()
        validated_choice = self.validate_choice(user_choice, 4)

        # Logout
        if validated_choice in ("#00", 4):
            self.session.clear_user()
            self.print_function(self.t("logged_out"))
            return

        # Option 1: Search produce
        if validated_choice == 1:
            product_name = input_non_empty_text(self.input_function, f"{self.t('enter_product_name')}: ")
            preferred_location = self.input_function(f"{self.t('preferred_location_optional')}: ").strip() or None

            search_results = self.harvest_service.search_harvests(
                product_name=product_name,
                location=preferred_location,
                users_service=self.user_service
            )

            if not search_results or not search_results.get("harvests"):
                self.print_function(self.t("no_offers_found"))
            else:
                self.print_function("\n=== Search Results ===")
                for h in search_results["harvests"]:
                    farmer_info = self.user_service.get_user(h["farmer_phone"])
                    self.print_function(
                        f"{h['product_name']} - {h['quantity']} units | "
                        f"{self.t('asking_price')}: ₦{h['asking_price']} | "
                        f"{self.t('farmer')}: {farmer_info.get('name')} ({farmer_info.get('phone')})"
                    )

        # Option 2: Browse farmers
        elif validated_choice == 2:
            search_location = self.input_function(f"{self.t('enter_location_optional')}: ").strip() or None
            farmers_list = self.user_service.list_farmers(location=search_location)

            if not farmers_list:
                self.print_function(self.t("no_farmers"))
            else:
                self.print_function("\n=== Farmers List ===")
                for f in farmers_list:
                    self.print_function(
                        f"{f['name']} - {f['phone']} | {self.t('crops')}: {', '.join(f.get('primary_crops', []))}"
                    )

        # Option 3: Contact a farmer
        elif validated_choice == 3:
            farmer_phone = input_non_empty_text(self.input_function, f"{self.t('enter_farmer_phone')}: ")
            farmer_harvests = self.harvest_service.list_harvests(farmer_phone=farmer_phone)

            if not farmer_harvests or not farmer_harvests.get("harvests"):
                self.print_function(self.t("no_harvests_for_farmer"))
            else:
                first_harvest = farmer_harvests["harvests"][0]
                self.connection_service.record_connection(
                    buyer_phone=current_user["phone"],
                    farmer_phone=farmer_phone,
                    harvest_id=first_harvest["id"]
                )
                farmer_info = self.user_service.get_user(farmer_phone)
                self.print_function(
                    f"{self.t('contact_recorded')} | {self.t('farmer_number')}: {farmer_info.get('phone')}"
                )

        else:
            self.print_function(self.t("invalid_choice"))

    # Keep displaying menu until logout
    def render_loop(self):
        while self.session.current_user:
            self.render()
