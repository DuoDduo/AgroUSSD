from .base_interface import USSDInterface
from services.harvest_service import HarvestService
from services.market_service import MarketService
from services.user_service import UserService
from utils.data_handler import load_json, save_json
from utils.validate import input_non_empty_text, input_positive_float

class FarmerMenu(USSDInterface):
    def __init__(self, session, input_fn=input, print_fn=print, language="en"):
        super().__init__(session, language)
        self.input_function = input_fn  # Function to read user input
        self.print_function = print_fn  # Function to display messages
        self.harvest_service = HarvestService(language=self.language)  # Handle harvest records
        self.market_service = MarketService(language=self.language)    # Handle market prices
        self.user_service = UserService(language=self.language)        # Handle user info

    # Render the farmer menu and handle user choices
    def render(self):
        current_user = self.session.current_user

        # Display menu
        self.print_function(
            f"\n{self.t('hello')} {current_user.get('name')} {self.t('farmer')}"
            f"\n1. {self.t('record_harvest')}"
            f"\n2. {self.t('my_harvests')}"
            f"\n3. {self.t('set_market_price')}"
            f"\n4. {self.t('update_profile')}"
            f"\n5. {self.t('logout')}"
        )

        # Get user choice
        user_input = self.input_function(f"{self.t('select_option')}: ").strip()
        validated_choice = self.validate_choice(user_input, 5)

        # Logout option
        if validated_choice in ("#00", 5):
            self.session.clear_user()
            self.print_function(self.t("logged_out"))
            return

        # Option 1: Record a new harvest
        if validated_choice == 1:
            product_name = input_non_empty_text(self.input_function, f"{self.t('enter_product_name')}: ")
            quantity = input_positive_float(self.input_function, f"{self.t('enter_quantity_units')}: ")
            quality = input_non_empty_text(self.input_function, f"{self.t('enter_quality')}: ")
            asking_price = input_positive_float(self.input_function, f"{self.t('enter_asking_price')}: ")

            recorded_harvest = self.harvest_service.record_harvest(
                farmer_phone=current_user["phone"],
                product_name=product_name,
                quantity=quantity,
                quality=quality,
                asking_price=asking_price
            )
            self.print_function(f"{self.t('harvest_recorded')}: {recorded_harvest['harvest']['id']}")

        # Option 2: View all harvests recorded by the farmer
        elif validated_choice == 2:
            harvests_data = self.harvest_service.list_harvests(farmer_phone=current_user["phone"])
            if not harvests_data or not harvests_data.get("harvests"):
                self.print_function(self.t("no_harvests_recorded"))
            else:
                self.print_function("\nMy Harvest")
                for h in harvests_data["harvests"]:
                    self.print_function(
                        f"{h['product_name']} - {h['quantity']} {h.get('quality')} | "
                        f"{self.t('asking_price')}: ₦{h['asking_price']}"
                    )

        # Option 3: Set market price for a product
        elif validated_choice == 3:
            product_name = input_non_empty_text(self.input_function, f"{self.t('enter_product_name_for_price')}: ")
            market_location = input_non_empty_text(self.input_function, f"{self.t('enter_market_location')}: ")
            price = input_positive_float(self.input_function, f"{self.t('enter_price')}: ")
            self.market_service.set_price(product_name, market_location, price)
            self.print_function(self.t("market_price_updated"))

        # Option 4: Update profile
        elif validated_choice == 4:
            updated_name = input_non_empty_text(self.input_function, f"{self.t('name')} ({current_user.get('name')}): ") or current_user.get("name")
            updated_location = input_non_empty_text(self.input_function, f"{self.t('location')} ({current_user.get('location')}): ") or current_user.get("location")

            user_record = self.user_service.get_user(current_user["phone"])
            user_record["name"] = updated_name
            user_record["location"] = updated_location

            all_users = load_json(self.user_service.users_path)
            for idx, u in enumerate(all_users):
                if u["phone"] == user_record["phone"]:
                    all_users[idx] = user_record
            save_json(self.user_service.users_path, all_users)

            self.session.set_user(user_record)
            self.print_function(self.t("profile_updated"))

        else:
            self.print_function(self.t("invalid_choice"))

    # Keep displaying menu until user logs out
    def render_loop(self):
        while self.session.current_user:
            self.render()
