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


class TestStudentRecords(unittest.TestCase):
    def setUp(self):
        sm.students.clear()

    def test_create_student(self):
        marks = {"Maths": 80, "Science": 90, "English": 70, "History": 85, "CS": 95}
        sm.students["S101"] = sm.build_student("S101", "Rahul", marks)
        s = sm.students["S101"]
        self.assertEqual(s["total"], 420)
        self.assertEqual(s["percentage"], 84)
        self.assertEqual(s["grade"], "A")

    def test_search_existing_and_missing(self):
        sm.students["S101"] = sm.build_student("S101", "Rahul", {"Maths": 50})
        self.assertIsNotNone(sm.search_student("S101"))
        self.assertIsNone(sm.search_student("S999"))


if __name__ == "__main__":
    unittest.main()
