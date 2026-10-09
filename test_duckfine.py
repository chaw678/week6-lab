import unittest
from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.fine = DuckFine("M001")

    def test_charge_returns_a_fee_for_a_late_duck(self):
        self.assertEqual(self.fine.charge(5), 1.50)

    def test_no_fee_when_returned_on_time(self):
        self.assertEqual(self.fine.charge(0), 0.0)

    def test_negative_days_raises(self):
        with self.assertRaises(ValueError):
            self.fine.charge(-1)

    def test_fine_is_capped_at_five_dollars(self):
        self.assertEqual(self.fine.charge(20), 5.00)

    def test_total_owed_accumulates_across_charges(self):
        self.fine.charge(5)
        self.fine.charge(3)
        self.assertEqual(self.fine.total_owed, 2.00)

    def test_deluxe_fine_is_double_the_regular_fine(self):
        self.assertEqual(self.fine.charge(5, deluxe=True), 3.00)


if __name__ == "__main__":
    unittest.main()
