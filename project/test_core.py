"""
test_core.py

Unit tests for the core helper functions:
- storage.generate_next_id
- validation.is_valid_email
- validation.is_not_empty
- validation.id_exists
- validation.find_record_by_id

Run with:
python -m unittest test_core.py -v
"""

import unittest

import storage
import validation


class TestStorageHelpers(unittest.TestCase):
    """Tests for storage helper functions."""

    def test_generate_next_id_empty_list(self):
        result = storage.generate_next_id(
            [],
            "program_id",
            "PRG"
        )

        self.assertEqual(result, "PRG001")

    def test_generate_next_id_with_existing_records(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG002"}
        ]

        result = storage.generate_next_id(
            records,
            "program_id",
            "PRG"
        )

        self.assertEqual(result, "PRG003")

    def test_generate_next_id_with_gap(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG003"}
        ]

        result = storage.generate_next_id(
            records,
            "program_id",
            "PRG"
        )

        self.assertEqual(result, "PRG004")

    def test_generate_next_id_ignores_invalid_ids(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "INVALID"},
            {"program_id": "PRG002"}
        ]

        result = storage.generate_next_id(
            records,
            "program_id",
            "PRG"
        )

        self.assertEqual(result, "PRG003")

    def test_generate_service_id(self):
        records = [
            {"service_id": "SVC001"},
            {"service_id": "SVC002"}
        ]

        result = storage.generate_next_id(
            records,
            "service_id",
            "SVC"
        )

        self.assertEqual(result, "SVC003")


class TestValidationHelpers(unittest.TestCase):
    """Tests for validation helper functions."""

    def test_is_not_empty_true(self):
        self.assertTrue(
            validation.is_not_empty("Hello")
        )

    def test_is_not_empty_false_for_blank(self):
        self.assertFalse(
            validation.is_not_empty("   ")
        )

    def test_is_not_empty_false_for_empty_string(self):
        self.assertFalse(
            validation.is_not_empty("")
        )

    def test_valid_email(self):
        self.assertTrue(
            validation.is_valid_email(
                "someone@example.com"
            )
        )

    def test_invalid_email_missing_at(self):
        self.assertFalse(
            validation.is_valid_email(
                "someone.example.com"
            )
        )

    def test_invalid_email_missing_dot(self):
        self.assertFalse(
            validation.is_valid_email(
                "someone@examplecom"
            )
        )

    def test_id_exists_true(self):
        records = [
            {"service_id": "SVC001"}
        ]

        self.assertTrue(
            validation.id_exists(
                records,
                "service_id",
                "SVC001"
            )
        )

    def test_id_exists_false(self):
        records = [
            {"service_id": "SVC001"}
        ]

        self.assertFalse(
            validation.id_exists(
                records,
                "service_id",
                "SVC999"
            )
        )

    def test_find_record_by_id_found(self):
        records = [
            {
                "inquiry_id": "INQ001",
                "customer_name": "Rohan"
            }
        ]

        result = validation.find_record_by_id(
            records,
            "inquiry_id",
            "INQ001"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["customer_name"],
            "Rohan"
        )

    def test_find_record_by_id_not_found(self):
        records = [
            {
                "inquiry_id": "INQ001"
            }
        ]

        result = validation.find_record_by_id(
            records,
            "inquiry_id",
            "INQ999"
        )

        self.assertIsNone(result)

    def test_find_record_by_id_case_insensitive(self):
        records = [
            {
                "service_id": "SVC001",
                "service_name": "Cloud Hosting"
            }
        ]

        result = validation.find_record_by_id(
            records,
            "service_id",
            "svc001"
        )

        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()