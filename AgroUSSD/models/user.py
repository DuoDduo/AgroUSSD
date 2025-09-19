from abc import ABC, abstractmethod

class User(ABC):
    """Abstract base class for users."""
    def __init__(self, name: str, phone: str, location: str, pin: str, language = "en"):
        self.name = name
        self.phone = phone
        self.location = location
        self.pin = pin  
        self.language = language

    @abstractmethod
    def role(self) -> str:
        pass

    def to_dict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "location": self.location,
            "pin": self.pin,
            "type": self.role(),
            "language": self.language
        }

    @classmethod
    def from_dict(cls, data: dict):
    
        raise NotImplementedError("from_dict must be implemented in subclasses")