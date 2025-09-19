import uuid  # For generating unique IDs
from datetime import datetime  # For timestamping when harvest is created

class Harvest:
    # Represents a harvest record linked to a farmer
    def __init__(
        self,
        farmer_phone: str,
        product_name: str,
        quantity: float,
        quality: str,
        asking_price: float,
        created_at=None,
        harvest_id=None
    ):
        self.id = harvest_id or str(uuid.uuid4())  # Unique ID for each harvest
        self.farmer_phone = farmer_phone           # Farmer's phone number
        self.product_name = product_name           # Name of the crop/product
        self.quantity = quantity                   # Quantity in units
        self.quality = quality                     # Quality description (e.g., "good", "premium")
        self.asking_price = asking_price           # Asking price per unit
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Timestamp

    def to_dict(self) -> dict:
        # Convert Harvest object to dictionary for storage in JSON 
        return {
            "id": self.id,
            "farmer_phone": self.farmer_phone,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "quality": self.quality,
            "asking_price": self.asking_price,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(harvest_cls, data: dict):
        # Create a Harvest object from a dictionary
        return harvest_cls(
            farmer_phone=data.get("farmer_phone"),
            product_name=data.get("product_name"),
            quantity=data.get("quantity"),
            quality=data.get("quality"),
            asking_price=data.get("asking_price"),
            created_at=data.get("created_at"),
            harvest_id=data.get("id")
        )
