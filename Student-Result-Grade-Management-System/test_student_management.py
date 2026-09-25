import unittest

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


if __name__ == "__main__":
    unittest.main()
