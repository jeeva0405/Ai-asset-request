import uuid

from slot_manager import SlotManager
from validation import validate_employee, is_asset_allowed


class AssetRequestAgent:

    def __init__(self):
        self.slot_manager = SlotManager()

    def start_conversation(self):
        return (
            "Hello! 👋\n"
            "Please describe your asset request.\n\n"
            "Example:\n"
            "My employee ID is EMP1001. "
            "I need a Dell Latitude laptop for AI development."
        )

    def process_extracted_data(self, extracted_data):
        """
        Receives JSON extracted by Gemini AI and updates slots.
        """

        # Update slots with extracted values
        for slot, value in extracted_data.items():

            if (
                slot in self.slot_manager.slots
                and value
                and value.strip() != ""
            ):
                self.slot_manager.update_slot(slot, value)

        # Current collected data
        data = self.slot_manager.get_data()

        # Validate Employee ID if available
        if data["employee_id"]:

            valid, employee = validate_employee(
                data["employee_id"]
            )

            if not valid:
                self.slot_manager.update_slot(
                    "employee_id",
                    None,
                )

                return (
                    "❌ Employee ID not found.\n"
                    "Please enter a valid Employee ID."
                )

        # Ask for missing information
        missing = self.slot_manager.get_next_missing_slot()

        if missing:
            return self.slot_manager.get_slot_question(
                missing
            )

        # Generate request
        return self.generate_request()

    def generate_request(self):

        data = self.slot_manager.get_data()

        valid, employee = validate_employee(
            data["employee_id"]
        )

        if not valid:
            return (
                "❌ Employee validation failed."
            )

        if not is_asset_allowed(
            employee,
            data["asset_type"],
        ):
            return (
                "❌ You are not eligible "
                "to request this asset."
            )

        request = {
            "request_id": f"AR-{str(uuid.uuid4())[:8].upper()}",
            "employee_id": data["employee_id"],
            "asset_type": data["asset_type"],
            "asset_name": data["asset_name"],
            "justification": data["justification"],
            "status": "Submitted",
        }

        return request


if __name__ == "__main__":

    agent = AssetRequestAgent()

    sample = {
        "employee_id": "EMP1001",
        "asset_type": "Laptop",
        "asset_name": "Dell Latitude 5440",
        "justification": "AI Development",
    }

    result = agent.process_extracted_data(sample)

    print(result)