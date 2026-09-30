import unittest

from storage import generate_next_id
from validation import (
    is_not_empty,
    is_valid_email,
    id_exists,
    find_record_by_id,
    is_valid_status
)


class TestStorageFunctions(unittest.TestCase):
    """Test storage-related functions."""

    def test_generate_first_id(self):
        records = []

        result = generate_next_id(
            records,
            "PRG",
            "program_id"
        )

        self.assertEqual(result, "PRG001")

    def test_generate_next_id(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG002"},
            {"program_id": "PRG003"}
        ]

        result = generate_next_id(
            records,
            "PRG",
            "program_id"
        )

        self.assertEqual(result, "PRG004")

    def test_generate_id_with_gap(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG003"}
        ]

        result = generate_next_id(
            records,
            "PRG",
            "program_id"
        )

        self.assertEqual(result, "PRG004")

    def test_ignore_invalid_ids(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "INVALID"},
            {"program_id": "PRG002"}
        ]

        result = generate_next_id(
            records,
            "PRG",
            "program_id"
        )

        self.assertEqual(result, "PRG003")


class TestValidationFunctions(unittest.TestCase):
    """Test validation functions."""

    def test_not_empty(self):
        self.assertTrue(
            is_not_empty("Python")
        )

    def test_empty_string(self):
        self.assertFalse(
            is_not_empty("")
        )

    def test_spaces_only(self):
        self.assertFalse(
            is_not_empty("   ")
        )

    def test_none_value(self):
        self.assertFalse(
            is_not_empty(None)
        )

    def test_valid_email(self):
        self.assertTrue(
            is_valid_email("test@example.com")
        )

    def test_invalid_email(self):
        self.assertFalse(
            is_valid_email("testexample.com")
        )

    def test_invalid_email_without_domain(self):
        self.assertFalse(
            is_valid_email("test@")
        )

    def test_existing_id(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG002"}
        ]

        self.assertTrue(
            id_exists(
                records,
                "program_id",
                "PRG001"
            )
        )

    def test_non_existing_id(self):
        records = [
            {"program_id": "PRG001"},
            {"program_id": "PRG002"}
        ]

        self.assertFalse(
            id_exists(
                records,
                "program_id",
                "PRG005"
            )
        )

    def test_case_insensitive_id(self):
        records = [
            {"program_id": "PRG001"}
        ]

        self.assertTrue(
            id_exists(
                records,
                "program_id",
                "prg001"
            )
        )

    def test_find_existing_record(self):
        records = [
            {
                "program_id": "PRG001",
                "program_name": "Python Programming"
            }
        ]

        result = find_record_by_id(
            records,
            "program_id",
            "PRG001"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["program_name"],
            "Python Programming"
        )

    def test_find_missing_record(self):
        records = [
            {"program_id": "PRG001"}
        ]

        result = find_record_by_id(
            records,
            "program_id",
            "PRG999"
        )

        self.assertIsNone(result)

    def test_valid_status(self):
        self.assertTrue(
            is_valid_status(
                "Active",
                ["Active", "Inactive"]
            )
        )

    def test_invalid_status(self):
        self.assertFalse(
            is_valid_status(
                "Unknown",
                ["Active", "Inactive"]
            )
        )


if __name__ == "__main__":
    unittest.main()