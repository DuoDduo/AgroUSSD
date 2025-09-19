from .user import User  # Import the base User class
from utils.translators import translate  # Import 

class Buyer(User):  # Buyer inherits from User, meaning it gets name, phone, location, pin, language
    def __init__(
        self, 
        name: str, 
        phone: str, 
        location: str, 
        pin: str, 
        business_name: str = None, 
        language: str = "en"
    ):
        # Initialize the base User class with name, phone, location, pin, and language
        super().__init__(name, phone, location, pin, language)
        
        # Store the buyer's business name (optional)
        self.business_name = business_name

    def role(self) -> str:
        # Return the role of this user (Buyer), translated to the selected language
        return translate("buyer_role", self.language)

    def to_dict(self) -> dict:
        # Convert the Buyer object into a dictionary
        buyer_data = super().to_dict()  # Get dictionary from base User class
        buyer_data.update({
            "business_name": self.business_name,  # Add the business name
            "language": self.language             # Add preferred language
        })
        return buyer_data

    @classmethod
    def from_dict(buyer_cls, data: dict):
        # Create a Buyer instance from a dictionary
        return buyer_cls(
            name=data.get("name"),
            phone=data.get("phone"),
            location=data.get("location"),
            pin=data.get("pin"),
            business_name=data.get("business_name"),
            language=data.get("language", "en")
        )
