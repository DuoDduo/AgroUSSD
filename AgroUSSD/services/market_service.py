import os
from utils.data_handler import load_json, save_json
from utils.translators import translate


class MarketService:
    def __init__(self, market_path="data/market_prices.json", language="en"):
        self.market_path = market_path        # Path to JSON file storing market prices
        self.language = language              # Language code for translations

        # Ensure the market data file exists
        try:
            load_json(self.market_path)
        except FileNotFoundError:
            save_json(self.market_path, [])

    # Set or update price for a specific product at a location
    def set_price(self, product_name: str, location: str, price: float):
        market_data = load_json(self.market_path)  # Load existing market data

        # Check if record exists for product at the location
        for product_record in market_data:
            if product_record['product_name'].lower() == product_name.lower() and \
               product_record['location'].lower() == location.lower():
                product_record['price'] = price      # Update existing price
                save_json(self.market_path, market_data)
                print(translate("price_updated", self.language))
                return product_record                 # Return updated record

        # Add new record if it doesn't exist
        new_price_record = {
            'product_name': product_name,
            'location': location,
            'price': price
        }
        market_data.append(new_price_record)
        save_json(self.market_path, market_data)
        print(translate("price_set", self.language))
        return new_price_record

    # Get list of prices optionally filtered by product and/or location
    def get_prices(self, product_name: str = None, location: str = None):
        market_data = load_json(self.market_path)    # Load all market data
        filtered_records = market_data               # Start with all records

        # Filter by product name if provided
        if product_name:
            filtered_records = [
                record for record in filtered_records
                if record['product_name'].lower() == product_name.lower()
            ]

        # Filter by location if provided
        if location:
            filtered_records = [
                record for record in filtered_records
                if record['location'].lower() == location.lower()
            ]

        # Print the results
        if not filtered_records:
            print(translate("no_price_data", self.language))
        else:
            print(translate("price_list_header", self.language))
            for record in filtered_records:
                print(f"{record['product_name']} - {record['location']}: ₦{record['price']}")

        return filtered_records

    # Compare prices for a product across all locations
    def compare_prices(self, product_name: str):
        # Filter all records for the product
        product_records = [
            record for record in load_json(self.market_path)
            if record['product_name'].lower() == product_name.lower()
        ]

        if not product_records:
            print(translate("no_price_data", self.language))
            return []

        # Sort records by price descending
        sorted_records = sorted(product_records, key=lambda record: record['price'], reverse=True)

        # Display comparison
        print(translate("compare_price_header", self.language))
        for record in sorted_records:
            print(f"{record['location']}: ₦{record['price']}")

        return sorted_records
