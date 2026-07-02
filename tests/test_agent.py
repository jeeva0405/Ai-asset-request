import unittest

from agent import AssetRequestAgent


class AssetRequestAgentTests(unittest.TestCase):
    def test_generate_request_requests_missing_employee_id(self):
        agent = AssetRequestAgent()
        agent.slot_manager.update_slot("asset_type", "Laptop")

        result = agent.generate_request()

        self.assertEqual(result, "👤 Please enter your Employee ID.")


if __name__ == "__main__":
    unittest.main()
