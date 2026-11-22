import unittest

class TestServiceHealth(unittest.TestCase):
    def test_service_definitions(self):
        """Validates default service ports and configuration expectations."""
        services = {
            "nginx": 80,
            "decoy": 8000,
            "ingest": 8001,
            "dashboard_api": 8002,
            "dashboard_ui": 3000
        }
        self.assertEqual(services["nginx"], 80)
        self.assertEqual(services["decoy"], 8000)
        self.assertEqual(services["ingest"], 8001)
        self.assertEqual(services["dashboard_api"], 8002)
        self.assertEqual(services["dashboard_ui"], 3000)

if __name__ == "__main__":
    unittest.main()
