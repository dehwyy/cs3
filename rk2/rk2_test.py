import unittest
from rk2 import Microprocessor, Computer, MicroprocessorComputer, task_b1, task_b2, task_b3

class TestRK2(unittest.TestCase):
    def setUp(self):
        self.computers = [
            Computer(1, "Comp A"),
            Computer(2, "Comp B"),
            Computer(3, "Comp C (Empty)")
        ]

        self.microprocessors = [
            Microprocessor(1, "Proc-100X", 3.5, 1),
            Microprocessor(2, "Proc-200", 4.0, 1),
            Microprocessor(3, "Proc-300X", 2.5, 2),
        ]

        self.links = [
            MicroprocessorComputer(1, 1),
            MicroprocessorComputer(1, 2),
            MicroprocessorComputer(2, 3),
        ]

    def test_task_b1(self):
        expected = [
            ("Proc-100X", 3.5, "Comp A"),
            ("Proc-200", 4.0, "Comp A"),
            ("Proc-300X", 2.5, "Comp B")
        ]
        result = task_b1(self.microprocessors, self.computers)
        self.assertEqual(result, expected)

    def test_task_b2(self):
        expected = [
            ("Comp B", 1),
            ("Comp A", 2)
        ]
        result = task_b2(self.microprocessors, self.computers)
        self.assertEqual(result, expected)

    def test_task_b3(self):
        expected = [
            ("Proc-100X", "Comp A"),
            ("Proc-300X", "Comp B")
        ]
        result = task_b3(self.microprocessors, self.computers, self.links)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
