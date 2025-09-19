from utils.data_handler import load_json, save_json
from utils.translators import translate
from models.farmer import Farmer
from models.buyer import Buyer
from typing import Optional


class UserService:
    def __init__(self, users_path="data/users.json", language="en"):
        self.users_path = users_path  # Path to the JSON file storing users
        self.language = language      # Default language for messages
        self._ensure_file()           # Ensure users file exists

    # Ensure the users JSON file exists; create an empty list if not
    def _ensure_file(self):
        try:
            load_json(self.users_path)
        except FileNotFoundError:
            save_json(self.users_path, [])

    # Register a new farmer with validations
    def register_farmer(
        self,
        name: str,
        phone: str,
        location: str,
        pin: str,
        farm_size: float,
        primary_crops: list,
        language: str = None
    ):
        all_users = load_json(self.users_path)

        # Check if phone number already exists
        if any(user['phone'] == phone for user in all_users):
            raise ValueError(translate("phone_already_registered", language or self.language))

        # Create a Farmer object
        new_farmer = Farmer(
            name=name,
            phone=phone,
            location=location,
            pin=pin,
            farm_size=farm_size,
            primary_crops=primary_crops,
            language=language or self.language
        )

        # Save farmer to users list
        all_users.append(new_farmer.to_dict())
        save_json(self.users_path, all_users)

        print(translate("registration_success", language or self.language))
        return new_farmer

    # Register a new buyer with validations
    def register_buyer(
        self,
        name: str,
        phone: str,
        location: str,
        pin: str,
        business_name: str = None,
        language: str = None
    ):
        all_users = load_json(self.users_path)

        # Check if phone number already exists
        if any(user['phone'] == phone for user in all_users):
            raise ValueError(translate("phone_already_registered", language or self.language))

        # Create a Buyer object
        new_buyer = Buyer(
            name=name,
            phone=phone,
            location=location,
            pin=pin,
            business_name=business_name,
            language=language or self.language
        )

        # Save buyer to users list
        all_users.append(new_buyer.to_dict())
        save_json(self.users_path, all_users)

        print(translate("registration_success", language or self.language))
        return new_buyer

    # Authenticate a user by phone and PIN
    def authenticate(self, phone: str, pin: str) -> Optional[dict]:
        all_users = load_json(self.users_path)

        for user in all_users:
            if user['phone'] == phone and user['pin'] == pin:
                print(translate("login_success", user.get("language", self.language)))
                return user

        # Return None if authentication fails
        print(translate("login_failed", self.language))
        return None

    # Retrieve a user by phone number
    def get_user(self, phone: str) -> Optional[dict]:
        all_users = load_json(self.users_path)
        for user in all_users:
            if user['phone'] == phone:
                return user
        return None

    # List all farmers with optional filtering by location or crop
    def list_farmers(self, location: str = None, product: str = None):
        all_users = load_json(self.users_path)

        # Filter users to only farmers
        farmers = [user for user in all_users if user.get('type') == 'farmer']

        # Filter by location if provided
        if location:
            farmers = [farmer for farmer in farmers if farmer.get('location') == location]

        # Filter by primary crop if provided
        if product:
            farmers = [
                farmer for farmer in farmers
                if product.lower() in [crop.lower() for crop in farmer.get('primary_crops', [])]
            ]

        # Show message if no farmers found
        if not farmers:
            print(translate("no_farmers_found", self.language))

        return farmers
