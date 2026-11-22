import unittest
import json
import os

class TestEventPipeline(unittest.TestCase):
    def test_sample_events_schema(self):
        sample_file = os.path.join(os.path.dirname(__file__), "..", "sample_data", "demo_events.json")
        with open(sample_file, "r", encoding="utf-8") as f:
            events = json.load(f)

        self.assertEqual(len(events), 8, "Expected 8 sample events matching the internship validation findings")
        for evt in events:
            self.assertIn("source_ip", evt)
            self.assertIn("method", evt)
            self.assertIn("endpoint", evt)
            self.assertIn("event_type", evt)
            self.assertIn("status_code", evt)
            self.assertIn("severity", evt)
            # Strict validation: Ensure passwords in payload_summary are redacted
            if "payload_summary" in evt and "password" in evt["payload_summary"]:
                self.assertEqual(evt["payload_summary"]["password"], "[REDACTED]")

if __name__ == "__main__":
    unittest.main()
