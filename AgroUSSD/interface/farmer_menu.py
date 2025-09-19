from .base_interface import USSDInterface
from services.harvest_service import HarvestService
from services.market_service import MarketService
from services.user_service import UserService
from utils.data_handler import load_json, save_json


class FarmerMenu(USSDInterface):
    def __init__(self, session, input_fn=input, print_fn=print, language="en"):
        super().__init__(session, language)
        self.input_function = input_fn                     # Function to read user input
        self.print_function = print_fn                     # Function to display messages
        self.harvest_service = HarvestService(language=self.language)  # Handle harvest records
        self.market_service = MarketService(language=self.language)    # Handle market prices
        self.user_service = UserService(language=self.language)        # Handle user info

    # Display the farmer menu and handle input
    def render(self):
        current_user = self.session.current_user

        # Display localized farmer menu
        self.print_function(
            f"{self.t('hello')} {current_user.get('name')} ({self.t('farmer')})\n"
            f"1. {self.t('record_harvest')}\n"
            f"2. {self.t('my_harvests')}\n"
            f"3. {self.t('set_market_price')}\n"
            f"4. {self.t('update_profile')}\n"
            f"5. {self.t('logout')}"
        )

        # Read user menu selection
        user_input = self.input_function(f"{self.t('select_option')}: ").strip()
        validated_choice = self.validate_choice(user_input, 5)  # Validate input

        # Handle special navigation options
        if validated_choice == "*0":  # Go back
            return
        if validated_choice == "*9":  # Go to main menu
            return
        if validated_choice in ("#00", 5):  # Logout
            self.session.clear_user()
            self.print_function(self.t("logged_out"))
            return

        # Option 1: Record a new harvest
        if validated_choice == 1:
            product_name = self.input_function(f"{self.t('enter_product_name')}: ").strip()
            quantity = float(self.input_function(f"{self.t('enter_quantity_units')}: ").strip() or 0)
            quality = self.input_function(f"{self.t('enter_quality')}: ").strip() or "good"
            asking_price = float(self.input_function(f"{self.t('enter_asking_price')}: ").strip() or 0)

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
                for harvest in harvests_data["harvests"]:
                    self.print_function(
                        f"{harvest['product_name']} - {harvest['quantity']} {harvest.get('quality')} - "
                        f"{self.t('asking_price')}: ₦{harvest['asking_price']}"
                    )

        # Option 3: Set market price for a product
        elif validated_choice == 3:
            product_name = self.input_function(f"{self.t('enter_product_name_for_price')}: ").strip()
            market_location = self.input_function(f"{self.t('enter_market_location')}: ").strip()
            price = float(self.input_function(f"{self.t('enter_price')}: ").strip() or 0)

            self.market_service.set_price(product_name, market_location, price)
            self.print_function(self.t("market_price_updated"))

        # Option 4: Update farmer profile
        elif validated_choice == 4:
            updated_name = self.input_function(f"{self.t('name')} ({current_user.get('name')}): ").strip() or current_user.get("name")
            updated_location = self.input_function(f"{self.t('location')} ({current_user.get('location')}): ").strip() or current_user.get("location")

            user_record = self.user_service.get_user(current_user["phone"])
            user_record["name"] = updated_name
            user_record["location"] = updated_location

            # Save updated user record to storage
            all_users = load_json(self.user_service.users_path)
            for index, record in enumerate(all_users):
                if record["phone"] == user_record["phone"]:
                    all_users[index] = user_record
            save_json(self.user_service.users_path, all_users)

            # Update session with new user info
            self.session.set_user(user_record)
            self.print_function(self.t("profile_updated"))

        # Invalid menu option
        else:
            self.print_function(self.t("invalid_choice"))

    # Keep displaying the menu until user logs out
    def render_loop(self):
        while self.session.current_user:
            self.render()
