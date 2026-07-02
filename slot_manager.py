class SlotManager:
    """
    Manages the required fields (slots) for an asset request.
    """

    REQUIRED_SLOTS = [
        "employee_id",
        "asset_type",
        "asset_name",
        "justification",
    ]

    def __init__(self):
        self.slots = {
            "employee_id": None,
            "asset_type": None,
            "asset_name": None,
            "justification": None,
        }

    def update_slot(self, slot_name, value):
        """
        Update a slot with a value.
        """
        if slot_name in self.slots:
            self.slots[slot_name] = value.strip() if isinstance(value, str) else value

    def get_slot(self, slot_name):
        """
        Get a slot value.
        """
        return self.slots.get(slot_name)

    def get_data(self):
        """
        Return all collected slot values.
        """
        return self.slots

    def get_missing_slots(self):
        """
        Return a list of missing slots.
        """
        return [
            slot
            for slot in self.REQUIRED_SLOTS
            if not self.slots.get(slot)
        ]

    def get_next_missing_slot(self):
        """
        Return the next missing slot.
        """
        missing = self.get_missing_slots()
        return missing[0] if missing else None

    def is_complete(self):
        """
        Check whether all slots are filled.
        """
        return len(self.get_missing_slots()) == 0

    def get_slot_question(self, slot):
        """
        Question to ask if a slot is missing.
        """
        questions = {
            "employee_id":
                "👤 Please enter your Employee ID.",

            "asset_type":
                "💻 What type of asset do you need? (Laptop, Monitor, Software License, etc.)",

            "asset_name":
                "🖥️ Please provide the asset name or model.",

            "justification":
                "📝 Please provide the business justification for this request.",
        }

        return questions.get(
            slot,
            "Please provide the required information."
        )

    def reset(self):
        """
        Clear all slot values.
        """
        for slot in self.REQUIRED_SLOTS:
            self.slots[slot] = None


if __name__ == "__main__":

    manager = SlotManager()

    print("Current Slots:")
    print(manager.get_data())

    manager.update_slot("employee_id", "EMP1001")

    print("\nUpdated Slots:")
    print(manager.get_data())

    print("\nMissing Slots:")
    print(manager.get_missing_slots())

    print("\nNext Question:")
    print(manager.get_slot_question(manager.get_next_missing_slot()))