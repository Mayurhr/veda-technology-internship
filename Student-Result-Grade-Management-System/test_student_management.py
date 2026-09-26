import unittest
from unittest.mock import patch

import student_management as sm


class TestCalculations(unittest.TestCase):
    def test_total(self):
        self.assertEqual(sm.calculate_total({"Maths": 80, "Science": 90}), 170)

    def test_percentage(self):
        self.assertEqual(sm.calculate_percentage({"Maths": 80, "Science": 90}), 85)

    def test_percentage_empty(self):
        self.assertEqual(sm.calculate_percentage({}), 0.0)

    def test_grade_boundaries(self):
        cases = {100: "A+", 90: "A+", 89.99: "A", 80: "A", 79: "B", 70: "B",
                 69: "C", 60: "C", 59: "D", 50: "D", 49.99: "F", 0: "F"}
        for percentage, grade in cases.items():
            with self.subTest(percentage=percentage):
                self.assertEqual(sm.calculate_grade(percentage), grade)


class TestValidation(unittest.TestCase):
    def test_valid_marks(self):
        self.assertEqual(sm.validate_marks("85"), 85.0)
        self.assertEqual(sm.validate_marks("0"), 0.0)
        self.assertEqual(sm.validate_marks("100"), 100.0)

    def test_invalid_marks(self):
        for bad in ["abc", "", "-1", "101", "nan", None]:
            with self.subTest(value=bad):
                self.assertIsNone(sm.validate_marks(bad))

    def test_student_id(self):
        self.assertTrue(sm.validate_student_id("S101"))
        self.assertFalse(sm.validate_student_id(""))
        self.assertFalse(sm.validate_student_id("S 1!"))


class TestStudentClass(unittest.TestCase):
    """Tests for the Student class introduced on Day 2."""

    def test_create_student(self):
        marks = {"Maths": 80, "Science": 90, "English": 70, "History": 85, "CS": 95}
        student = sm.Student("S101", "Rahul", marks)
        self.assertEqual(student.id, "S101")
        self.assertEqual(student.name, "Rahul")
        self.assertEqual(student.subjects, ["Maths", "Science", "English", "History", "CS"])
        self.assertEqual(student.total, 420)
        self.assertEqual(student.percentage, 84)
        self.assertEqual(student.grade, "A")

    def test_total_calculation(self):
        student = sm.Student("S1", "A", {"Maths": 50, "Science": 50})
        self.assertEqual(student.total, 100)

    def test_percentage_calculation(self):
        student = sm.Student("S1", "A", {"Maths": 60, "Science": 80})
        self.assertEqual(student.percentage, 70)

    def test_grade_calculation(self):
        student = sm.Student("S1", "A", {"Maths": 95, "Science": 95})
        self.assertEqual(student.grade, "A+")

    def test_update_name(self):
        student = sm.Student("S1", "Old Name", {"Maths": 50})
        student.update_name("New Name")
        self.assertEqual(student.name, "New Name")

    def test_update_marks_recalculates_total_percentage_grade(self):
        student = sm.Student("S1", "A", {"Maths": 40, "Science": 40})
        self.assertEqual(student.grade, "F")
        student.update_marks({"Maths": 95, "Science": 95})
        self.assertEqual(student.total, 190)
        self.assertEqual(student.percentage, 95)
        self.assertEqual(student.grade, "A+")

    def test_marks_dict_is_copied_not_shared(self):
        original_marks = {"Maths": 80}
        student = sm.Student("S1", "A", original_marks)
        original_marks["Maths"] = 0
        self.assertEqual(student.marks["Maths"], 80)


class TestStudentManager(unittest.TestCase):
    """Tests for the StudentManager class introduced on Day 2."""

    def setUp(self):
        self.manager = sm.StudentManager()

    def test_add_and_exists(self):
        self.manager.add("S101", "Rahul", {"Maths": 80})
        self.assertTrue(self.manager.exists("S101"))
        self.assertEqual(len(self.manager), 1)

    def test_get_existing_and_missing(self):
        self.manager.add("S101", "Rahul", {"Maths": 50})
        self.assertIsNotNone(self.manager.get("S101"))
        self.assertIsNone(self.manager.get("S999"))

    def test_all_returns_every_student(self):
        self.manager.add("S101", "Rahul", {"Maths": 50})
        self.manager.add("S102", "Priya", {"Maths": 90})
        ids = sorted(s.id for s in self.manager.all())
        self.assertEqual(ids, ["S101", "S102"])

    def test_performance_stats(self):
        self.manager.add("S101", "Rahul", {"Maths": 50})   # 50%
        self.manager.add("S102", "Priya", {"Maths": 90})   # 90%
        topper, highest, average = self.manager.performance_stats()
        self.assertEqual(topper.name, "Priya")
        self.assertEqual(highest, 90)
        self.assertEqual(average, 70)

    def test_update_student_via_manager(self):
        self.manager.add("S101", "Rahul", {"Maths": 50})
        student = self.manager.get("S101")
        student.update_name("Rahul Sharma")
        student.update_marks({"Maths": 100})
        self.assertEqual(self.manager.get("S101").name, "Rahul Sharma")
        self.assertEqual(self.manager.get("S101").grade, "A+")

    def test_add_duplicate_student_id_raises(self):
        # Day 3: the manager itself refuses a duplicate ID, on top of the
        # CLI's own exists() check, so it can never overwrite a record.
        self.manager.add("S101", "Rahul", {"Maths": 50})
        with self.assertRaises(ValueError):
            self.manager.add("S101", "Someone Else", {"Maths": 10})
        # The original record must be unchanged.
        self.assertEqual(self.manager.get("S101").name, "Rahul")

    def test_performance_stats_on_empty_manager_raises(self):
        # Day 3: calling performance_stats() directly on an empty manager
        # has a clear, documented failure mode instead of crashing with a
        # confusing ZeroDivisionError/ValueError from max()/sum().
        with self.assertRaises(ValueError):
            self.manager.performance_stats()


class TestCLIActions(unittest.TestCase):
    """Tests for the module-level CLI action functions using sm.manager."""

    def setUp(self):
        sm.manager.clear()

    def test_search_student_existing_and_missing(self):
        sm.manager.add("S101", "Rahul", {"Maths": 50})
        self.assertIsNotNone(sm.search_student("S101"))
        self.assertIsNone(sm.search_student("S999"))

    def test_performance_summary_no_students_does_not_raise(self):
        # Should print a message and return, not raise (e.g. ZeroDivisionError).
        sm.performance_summary()

    def test_view_all_students_no_students_does_not_raise(self):
        sm.view_all_students()

    def test_add_student_rejects_duplicate_id(self):
        sm.manager.add("S101", "Rahul", {"Maths": 50})
        # Re-entering the same ID should be rejected before it ever asks
        # for a name, so only one input() call ("Enter Student ID") fires.
        with patch("builtins.input", side_effect=["S101"]):
            sm.add_student()
        self.assertEqual(sm.manager.get("S101").name, "Rahul")  # unchanged
        self.assertEqual(len(sm.manager), 1)

    def test_add_student_rejects_empty_name(self):
        with patch("builtins.input", side_effect=["S200", "  "]):
            sm.add_student()
        self.assertFalse(sm.manager.exists("S200"))

    def test_add_student_rejects_invalid_id(self):
        with patch("builtins.input", side_effect=["S 1!"]):
            sm.add_student()
        self.assertEqual(len(sm.manager), 0)


class TestInputValidationLoops(unittest.TestCase):
    """Marks/subjects (0/100 boundaries, empty & duplicate subjects)."""

    def test_read_marks_accepts_0_and_100_boundaries(self):
        with patch("builtins.input", side_effect=["0", "100"]):
            marks = sm.read_marks(["Maths", "Science"])
        self.assertEqual(marks, {"Maths": 0.0, "Science": 100.0})

    def test_read_marks_rejects_out_of_range_then_accepts(self):
        with patch("builtins.input", side_effect=["-1", "101", "abc", "75"]):
            marks = sm.read_marks(["Maths"])
        self.assertEqual(marks, {"Maths": 75.0})

    def test_read_subjects_rejects_empty_list(self):
        with patch("builtins.input", side_effect=["   ", "Maths,Science"]):
            subjects = sm.read_subjects()
        self.assertEqual(subjects, ["Maths", "Science"])

    def test_read_subjects_rejects_duplicates(self):
        with patch("builtins.input", side_effect=["Maths,maths", "Maths,Science"]):
            subjects = sm.read_subjects()
        self.assertEqual(subjects, ["Maths", "Science"])


class TestMainGracefulExit(unittest.TestCase):
    """Day 3: Ctrl+C / Ctrl+D should exit cleanly, not crash."""

    def test_keyboard_interrupt_is_handled(self):
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            try:
                sm.main()
            except KeyboardInterrupt:
                self.fail("main() should catch KeyboardInterrupt, not propagate it.")

    def test_eof_error_is_handled(self):
        with patch("builtins.input", side_effect=EOFError):
            try:
                sm.main()
            except EOFError:
                self.fail("main() should catch EOFError, not propagate it.")


if __name__ == "__main__":
    unittest.main()
