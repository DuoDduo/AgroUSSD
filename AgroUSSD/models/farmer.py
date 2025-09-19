from .user import User  # Import the base User class
from utils.translators import translate  # Import translate function for multilingual support

class Farmer(User):  # Farmer inherits from User, so it has name, phone, location, pin, language
    def __init__(
        self,
        name: str,
        phone: str,
        location: str,
        pin: str,
        farm_size: float = 0.0,
        primary_crops=None,
        language="en"
    ):
        # Initialize base User class with common user attributes
        super().__init__(name, phone, location, pin, language=language)
        
        # Specific attributes for Farmer
        self.farm_size = farm_size                  # Farm size in acres
        self.primary_crops = primary_crops or []        # List of crops the farmer grows

    def role(self) -> str:
        # Return the translated role name based on session language
        return translate("farmer_role", self.language)

    def to_dict(self) -> dict:
        # Convert Farmer object to dictionary including base User info
        farmer_data = super().to_dict()                       # Start with base User dictionary
        farmer_data.update({
            "farm_size": self.farm_size,
            "primary_crops": self.primary_crops
        })
        return farmer_data

    @classmethod
    def from_dict(cls, data: dict):
        # Create a Farmer object from a dictionary
        return cls(
            name = data.get("name"),
            phone = data.get("phone"),
            location = data.get("location"),
            pin = data.get("pin"),
            farm_size_in_acres = data.get("farm_size", 0.0),
            primary_crops_list = data.get("primary_crops", []),
            language = data.get("language", "en")
        )
