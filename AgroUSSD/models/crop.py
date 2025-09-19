from .product import Product  # Import the base Product class

class Crop(Product):  # Crop inherits from Product, so it has name and unit
    def __init__(self, crop_name: str, unit: str = "crate", variety: str = None):
        # Initialize the base Product class with crop name and unit
        super().__init__(crop_name, unit)
        
        # Optional attribute for specifying crop variety
        self.variety = variety

    def category(self) -> str:
        # Return the category of this product, always 'crop'
        return "crop"

    def to_dict(self) -> dict:
        # Convert Crop object into a dictionary
        crop_data = super().to_dict()  # Start with base Product dictionary
        crop_data.update({"variety": self.variety})  # Add variety field
        return crop_data
