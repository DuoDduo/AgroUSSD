from abc import ABC, abstractmethod  # ABC for abstract base class

class Product(ABC):
    # Abstract base class for all products (crops, livestock, processed goods)
    def __init__(self, product_name: str, unit_of_measure: str):
        self.name = product_name            # Name of the product
        self.unit = unit_of_measure         # Unit of measurement (e.g., crate, kg)

    @abstractmethod
    def category(self) -> str:
        # Abstract method to define product category (e "crop", "livestock")
        pass

    def to_dict(self) -> dict:
        # Convert Product object to dictionary for storage in JSON
        return {
            "name": self.name,
            "unit": self.unit,
            "category": self.category()      # Calls the implemented category() method
        }
