import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import inquiries
import programs
import reports
import search
import services
import storage
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


# ----------------------------------------------------------------------
# Helpers: every test below uses a temporary data folder, so the real
# JSON files in data/ are never touched.
# ----------------------------------------------------------------------

class TempDataTestCase(unittest.TestCase):
    """Base class: temporary data folder + helper to run functions with input."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        patcher = patch.object(storage, "DATA_FOLDER", self.temp_dir.name)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.temp_dir.cleanup)

    def run_with_input(self, function, *answers):
        """Run function with fake keyboard input; return printed output."""
        buffer = io.StringIO()
        with patch("builtins.input", side_effect=list(answers)):
            with redirect_stdout(buffer):
                function()
        return buffer.getvalue()

    def read_json(self, filename):
        with open(os.path.join(self.temp_dir.name, filename), encoding="utf-8") as f:
            return json.load(f)


class TestJsonStorage(TempDataTestCase):

    def test_missing_file_is_created_empty(self):
        self.assertEqual(storage.load_data("x.json"), [])
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir.name, "x.json")))

    def test_missing_file_uses_defaults(self):
        data = storage.load_data("x.json", [{"a": 1}])
        self.assertEqual(data, [{"a": 1}])
        self.assertEqual(self.read_json("x.json"), [{"a": 1}])

    def test_save_and_load(self):
        self.assertTrue(storage.save_data("x.json", [{"id": "1"}]))
        self.assertEqual(storage.load_data("x.json"), [{"id": "1"}])

    def test_empty_records(self):
        storage.save_data("x.json", [])
        self.assertEqual(storage.load_data("x.json"), [])

    def test_corrupted_json_is_safe_and_backed_up(self):
        path = os.path.join(self.temp_dir.name, "x.json")
        with open(path, "w") as f:
            f.write("{not valid json")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(storage.load_data("x.json"), [])
        self.assertTrue(os.path.exists(path + ".corrupt"))

    def test_json_not_a_list(self):
        path = os.path.join(self.temp_dir.name, "x.json")
        with open(path, "w") as f:
            f.write('{"a": 1}')
        with redirect_stdout(io.StringIO()):
            self.assertEqual(storage.load_data("x.json"), [])

    def test_non_dict_records_are_ignored(self):
        storage.save_data("x.json", [{"a": 1}, "text", 5])
        self.assertEqual(storage.load_data("x.json"), [{"a": 1}])


class TestPrograms(TempDataTestCase):

    def add(self, name="Data Science", category="AI", duration="2 Weeks", status="1"):
        return self.run_with_input(programs.add_program, name, category, duration, status)

    def test_default_data_loaded_when_file_missing(self):
        self.assertEqual(len(programs.load_programs()), 3)

    def test_add_valid_program_and_persist(self):
        self.add()
        saved = self.read_json("programs.json")
        self.assertEqual(saved[-1]["program_id"], "PRG004")
        self.assertEqual(saved[-1]["status"], "Active")
        # "restart": load again from disk
        self.assertEqual(programs.load_programs()[-1]["program_name"], "Data Science")

    def test_add_empty_name_and_category_are_re_asked(self):
        out = self.run_with_input(
            programs.add_program, "", "Name", "   ", "Cat", "Dur", "2")
        self.assertIn("cannot be empty", out)
        self.assertEqual(programs.load_programs()[-1]["status"], "Inactive")

    def test_add_invalid_status_not_saved(self):
        out = self.run_with_input(programs.add_program, "N", "C", "D", "9")
        self.assertIn("not added", out)
        self.assertEqual(len(programs.load_programs()), 3)

    def test_view(self):
        out = self.run_with_input(programs.view_programs)
        self.assertIn("PRG001", out)
        self.assertIn("PRG003", out)

    def test_view_empty(self):
        storage.save_data("programs.json", [])
        self.assertIn("No programs found", self.run_with_input(programs.view_programs))

    def test_search_existing_by_name_and_category_case_insensitive(self):
        self.assertIn("Cloud DevOps", self.run_with_input(programs.search_programs, "CLOUD"))
        self.assertIn("Found 2", self.run_with_input(programs.search_programs, "software"))

    def test_search_nonexistent_and_empty(self):
        self.assertIn("No matching", self.run_with_input(programs.search_programs, "zzz"))
        self.assertIn("cannot be empty", self.run_with_input(programs.search_programs, " "))

    def test_filter_active_inactive(self):
        self.run_with_input(programs.update_program, "PRG002", "", "", "", "2")
        active = self.run_with_input(programs.filter_programs_by_status, "1")
        inactive = self.run_with_input(programs.filter_programs_by_status, "2")
        self.assertNotIn("PRG002", active)
        self.assertIn("PRG002", inactive)

    def test_filter_invalid_choice(self):
        self.assertIn("Invalid", self.run_with_input(programs.filter_programs_by_status, "x"))

    def test_update_existing_case_insensitive_id(self):
        self.run_with_input(programs.update_program, "prg001", "New Name", "", "", "3")
        record = programs.load_programs()[0]
        self.assertEqual(record["program_name"], "New Name")
        self.assertEqual(record["status"], "Active")

    def test_update_nonexistent(self):
        out = self.run_with_input(programs.update_program, "PRG999")
        self.assertIn("No program found", out)

    def test_update_invalid_status_choice_changes_nothing(self):
        self.run_with_input(programs.update_program, "PRG001", "Changed", "", "", "9")
        self.assertNotEqual(programs.load_programs()[0]["program_name"], "Changed")

    def test_delete_existing(self):
        self.run_with_input(programs.delete_program, "PRG002", "y")
        ids = [p["program_id"] for p in programs.load_programs()]
        self.assertEqual(ids, ["PRG001", "PRG003"])

    def test_delete_cancelled(self):
        self.run_with_input(programs.delete_program, "PRG002", "n")
        self.assertEqual(len(programs.load_programs()), 3)

    def test_delete_nonexistent_and_invalid_id(self):
        self.assertIn("No program found", self.run_with_input(programs.delete_program, "PRG999"))
        self.assertIn("No program found", self.run_with_input(programs.delete_program, "???"))
        self.assertIn("No program found", self.run_with_input(programs.delete_program, ""))

    def test_ids_never_reused_after_delete(self):
        self.run_with_input(programs.delete_program, "PRG003", "y")
        self.add()
        self.add(name="Another")
        ids = [p["program_id"] for p in programs.load_programs()]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids[-1], "PRG004")

    def test_menu_invalid_choice_then_back(self):
        out = self.run_with_input(programs.program_menu, "99", "abc", "", "7")
        self.assertEqual(out.count("Invalid choice"), 3)


class TestServices(TempDataTestCase):

    def add(self, name="SEO Audit", category="Marketing", desc="Site SEO review", status="1"):
        return self.run_with_input(services.add_service, name, category, desc, status)

    def test_add_valid_and_persist(self):
        self.add()
        saved = self.read_json("services.json")
        self.assertEqual(saved[-1]["service_id"], "SVC004")
        self.assertEqual(services.load_services()[-1]["service_name"], "SEO Audit")

    def test_add_empty_input_re_asked_and_invalid_status(self):
        out = self.run_with_input(services.add_service, "", "Name", "Cat", "", "Desc", "1")
        self.assertEqual(out.count("cannot be empty"), 2)
        out = self.run_with_input(services.add_service, "N", "C", "D", "x")
        self.assertIn("not added", out)
        self.assertEqual(len(services.load_services()), 4)

    def test_view(self):
        self.assertIn("SVC001", self.run_with_input(services.view_services))

    def test_search_existing_nonexistent(self):
        self.assertIn("Cloud Hosting", self.run_with_input(services.search_services, "hosting"))
        self.assertIn("Infrastructure", self.run_with_input(services.search_services, "infra"))
        self.assertIn("No matching", self.run_with_input(services.search_services, "zzz"))

    def test_filter_by_status(self):
        self.run_with_input(services.update_service, "SVC001", "", "", "", "2")
        self.assertIn("SVC001", self.run_with_input(services.filter_services_by_status, "2"))
        self.assertNotIn("SVC001", self.run_with_input(services.filter_services_by_status, "1"))

    def test_update_existing_and_nonexistent(self):
        self.run_with_input(services.update_service, "svc002", "", "Hosting", "", "")
        self.assertEqual(services.load_services()[1]["category"], "Hosting")
        self.assertIn("No service found", self.run_with_input(services.update_service, "SVC999"))

    def test_delete_existing_and_nonexistent(self):
        self.run_with_input(services.delete_service, "SVC001", "y")
        self.assertEqual(len(services.load_services()), 2)
        self.assertIn("No service found", self.run_with_input(services.delete_service, "SVC001"))


class TestInquiries(TempDataTestCase):

    def add(self, name="Asha Rao", email="asha@example.com", service="Cloud Hosting",
            message="Need pricing", status="1"):
        return self.run_with_input(inquiries.add_inquiry, name, email, service, message, status)

    def test_add_valid_and_persist(self):
        self.add()
        saved = self.read_json("inquiries.json")
        self.assertEqual(saved[-1]["inquiry_id"], "INQ002")
        self.assertEqual(saved[-1]["status"], "Open")

    def test_invalid_email_re_asked(self):
        out = self.run_with_input(
            inquiries.add_inquiry, "Name", "bad-email", "a@b", "ok@example.com", "Svc", "Msg", "1")
        self.assertEqual(out.count("Invalid email"), 2)
        self.assertEqual(inquiries.load_inquiries()[-1]["email"], "ok@example.com")

    def test_empty_customer_name_re_asked(self):
        out = self.run_with_input(
            inquiries.add_inquiry, "", "Real Name", "a@example.com", "Svc", "Msg", "1")
        self.assertIn("cannot be empty", out)

    def test_view(self):
        self.assertIn("INQ001", self.run_with_input(inquiries.view_inquiries))

    def test_search_by_customer_email_service(self):
        self.add()
        self.assertIn("Asha Rao", self.run_with_input(inquiries.search_inquiries, "asha"))
        self.assertIn("Asha Rao", self.run_with_input(inquiries.search_inquiries, "ASHA@EXAMPLE"))
        self.assertIn("Asha Rao", self.run_with_input(inquiries.search_inquiries, "cloud"))
        self.assertIn("No matching", self.run_with_input(inquiries.search_inquiries, "nobody"))

    def test_update_inquiry(self):
        self.run_with_input(inquiries.update_inquiry, "inq001", "Rohan S", "new@example.com", "", "", "2")
        record = inquiries.load_inquiries()[0]
        self.assertEqual(record["customer_name"], "Rohan S")
        self.assertEqual(record["email"], "new@example.com")
        self.assertEqual(record["status"], "In Progress")

    def test_update_inquiry_invalid_email_changes_nothing(self):
        out = self.run_with_input(inquiries.update_inquiry, "INQ001", "X", "bad")
        self.assertIn("Invalid email", out)
        self.assertEqual(inquiries.load_inquiries()[0]["customer_name"], "Rohan Sharma")

    def test_update_status_and_invalid_choice(self):
        self.run_with_input(inquiries.update_inquiry_status, "INQ001", "3")
        self.assertEqual(inquiries.load_inquiries()[0]["status"], "Closed")
        out = self.run_with_input(inquiries.update_inquiry_status, "INQ001", "7")
        self.assertIn("Invalid status", out)
        self.assertEqual(inquiries.load_inquiries()[0]["status"], "Closed")

    def test_invalid_and_missing_ids(self):
        for func, args in [(inquiries.update_inquiry, ("INQ999",)),
                           (inquiries.update_inquiry_status, ("abc",)),
                           (inquiries.delete_inquiry, ("",))]:
            self.assertIn("No inquiry found", self.run_with_input(func, *args))

    def test_delete(self):
        self.run_with_input(inquiries.delete_inquiry, "INQ001", "y")
        self.assertEqual(inquiries.load_inquiries(), [])

    def test_filter_each_status(self):
        self.add(name="Prog Person", status="2")
        self.add(name="Closed Person", status="3")
        self.assertIn("Rohan", self.run_with_input(inquiries.filter_inquiries_by_status, "1"))
        out = self.run_with_input(inquiries.filter_inquiries_by_status, "2")
        self.assertIn("Prog Person", out)
        self.assertNotIn("Rohan", out)
        self.assertIn("Closed Person", self.run_with_input(inquiries.filter_inquiries_by_status, "3"))
        self.assertIn("Invalid", self.run_with_input(inquiries.filter_inquiries_by_status, "9"))


class TestSearchModule(TempDataTestCase):

    def test_program_and_service_search(self):
        self.assertIn("Cloud DevOps", self.run_with_input(search.search_programs_by_name_or_category, "devops"))
        self.assertIn("PRG003", self.run_with_input(search.search_programs_by_category, "cloud"))
        self.assertIn("Cloud Hosting", self.run_with_input(search.search_services_by_name_or_category, "cloud"))
        self.assertIn("SVC003", self.run_with_input(search.search_services_by_category, "mobile"))

    def test_inquiry_search(self):
        self.assertIn("Rohan", self.run_with_input(search.search_inquiries, "rohan.sharma"))
        self.assertIn("No matching", self.run_with_input(search.search_inquiries, "zzz"))

    def test_filter_records_by_status(self):
        self.assertIn("PRG001", self.run_with_input(search.filter_records_by_status, "1", "1"))
        self.assertIn("No services found", self.run_with_input(search.filter_records_by_status, "2", "2"))
        self.assertIn("INQ001", self.run_with_input(search.filter_records_by_status, "3", "1"))
        self.assertIn("Invalid record type", self.run_with_input(search.filter_records_by_status, "9"))

    def test_search_menu_invalid_choice(self):
        out = self.run_with_input(search.search_menu, "0", "x", "7")
        self.assertEqual(out.count("Invalid choice"), 2)


class TestReports(TempDataTestCase):

    def test_counts_match_json(self):
        self.run_with_input(inquiries.add_inquiry, "A", "a@example.com", "S", "M", "3")
        self.run_with_input(programs.update_program, "PRG001", "", "", "", "2")
        out = self.run_with_input(reports.show_business_summary)
        self.assertIn("Total Programs : %d" % len(self.read_json("programs.json")), out)
        self.assertIn("Total Services : %d" % len(self.read_json("services.json")), out)
        self.assertIn("Total Inquiries: %d" % len(self.read_json("inquiries.json")), out)
        self.assertIn("Inactive : 1", out)
        self.assertIn("Closed      : 1", out)

    def test_category_and_status_reports(self):
        out = self.run_with_input(reports.show_category_reports)
        self.assertIn("Software Development: 2", out)
        self.assertIn("Infrastructure: 1", out)
        out = self.run_with_input(reports.show_inquiry_status_report)
        self.assertIn("Open: 1", out)

    def test_reports_with_no_data(self):
        for name in ("programs.json", "services.json", "inquiries.json"):
            storage.save_data(name, [])
        self.assertIn("Total Programs : 0", self.run_with_input(reports.show_business_summary))
        self.assertIn("No data found", self.run_with_input(reports.show_category_reports))

    def test_report_menu_invalid_choice(self):
        out = self.run_with_input(reports.report_menu, "x", "4")
        self.assertIn("Invalid choice", out)


class TestMainMenu(TempDataTestCase):

    def test_invalid_main_choices_then_exit(self):
        import main
        out = self.run_with_input(main.main, "9", "", "abc", "6")
        self.assertEqual(out.count("Invalid choice"), 3)
        self.assertIn("Goodbye", out)


if __name__ == "__main__":
    unittest.main()