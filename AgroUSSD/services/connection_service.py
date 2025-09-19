from utils.data_handler import load_json, save_json
from utils.translators import translate  # Translation utility for multi-language support


class ConnectionService:
    def __init__(self, connections_path="data/connections.json", language="en"):
        self.connections_path = connections_path  # File path for storing connection records
        self.language = language                  # Session language for translations

        # Ensure the connections file exists; create an empty list if it doesn't
        try:
            load_json(self.connections_path)
        except FileNotFoundError:
            save_json(self.connections_path, [])

    # Record a new connection between a buyer and a farmer
    def record_connection(self, buyer_phone: str, farmer_phone: str, harvest_id: str):
        all_connections = load_json(self.connections_path)  # Load existing connections

        # Prepare the new connection record
        new_connection = {
            "buyer_phone": buyer_phone,
            "farmer_phone": farmer_phone,
            "harvest_id": harvest_id
        }

        all_connections.append(new_connection)               # Add new connection to the list
        save_json(self.connections_path, all_connections)   # Save updated connections list

        # Return confirmation message and the newly recorded connection
        return {
            "message": translate("Connection recorded successfully", self.language),
            "connection": new_connection
        }

    # Retrieve all connections
    def list_connections(self):
        all_connections = load_json(self.connections_path)  # Load connections from file

        # Return message and empty list if no connections found
        if not all_connections:
            return {
                "message": translate("No connections found.", self.language),
                "connections": []
            }

        # Return all connections with success message
        return {
            "message": translate("Connections retrieved successfully", self.language),
            "connections": all_connections
        }
