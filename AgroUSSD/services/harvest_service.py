import os
from utils.data_handler import load_json, save_json
from models.harvest import Harvest
from utils.translators import translate  # Import translation utility for multi-language support


class HarvestService:
    def __init__(self, harvest_path="data/harvests.json", language="en"):
        self.harvest_path = harvest_path
        self.language = language  # Store the selected language for messages

        # Ensure the harvest data file exists, create empty if missing
        try:
            load_json(self.harvest_path)
        except FileNotFoundError:
            save_json(self.harvest_path, [])

    # Record a new harvest entry for a farmer
    def record_harvest(self, farmer_phone: str, product_name: str, quantity: float, quality: str, asking_price: float):
        all_harvests = load_json(self.harvest_path)

        # Create a new Harvest object
        new_harvest = Harvest(
            farmer_phone=farmer_phone,
            product_name=product_name,
            quantity=quantity,
            quality=quality,
            asking_price=asking_price,
        )

        # Append new harvest to existing list and save
        all_harvests.append(new_harvest.to_dict())
        save_json(self.harvest_path, all_harvests)

        return {
            "message": translate("Harvest recorded successfully", self.language),
            "harvest": new_harvest.to_dict(),
        }

    # List all harvests, optionally filtered by farmer's phone number
    def list_harvests(self, farmer_phone: str = None):
        all_harvests = load_json(self.harvest_path)

        # Filter harvests for a specific farmer if provided
        if farmer_phone:
            all_harvests = [harvest for harvest in all_harvests if harvest["farmer_phone"] == farmer_phone]

        # Return message if no harvests found
        if not all_harvests:
            return {
                "message": translate("No harvest records found.", self.language),
                "harvests": [],
            }

        return {
            "message": translate("Harvest list retrieved", self.language),
            "harvests": all_harvests
        }

    # Search harvests by product name and/or farmer location
    def search_harvests(self, product_name: str = None, location: str = None, users_service=None):
        all_harvests = load_json(self.harvest_path)

        # Filter by product name if given
        if product_name:
            all_harvests = [harvest for harvest in all_harvests if harvest["product_name"].lower() == product_name.lower()]

        # Filter by farmer location if given and a user service is provided
        if location and users_service:
            filtered_harvests = []
            for harvest in all_harvests:
                farmer = users_service.get_user(harvest["farmer_phone"])
                if farmer and farmer.get("location", "").lower() == location.lower():
                    filtered_harvests.append(harvest)
            all_harvests = filtered_harvests

        # Return message if no matching harvests
        if not all_harvests:
            return {
                "message": translate("No matching harvests found.", self.language),
                "harvests": [],
            }

        return {
            "message": translate("Harvest search results", self.language),
            "harvests": all_harvests
        }
