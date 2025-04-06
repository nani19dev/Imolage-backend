import unittest
from unittest.mock import patch
from django.test import TestCase
from datetime import date, datetime, timedelta
from .models import Contract

class ContractTest(TestCase):

    def setUp(self):
        # Assuming today is 2023-11-20
        today_str = "2024-12-1"
        # Convert the string to a datetime object
        self.today = datetime.strptime(today_str, "%Y-%m-%d").date()
        self.rent = 1000

    def test_calculate_duration_no_days(self):
        """Test calculate_duration for today's start date"""
        start_date = self.today
        contract = Contract(start_date=start_date, rent=self.rent)
        duration = contract.calculate_duration()
        self.assertEqual(duration, 0)

    def test_calculate_duration_past_start(self):
        """Test calculate_duration for a start date in the past"""
        start_date = self.today - timedelta(days=30)
        contract = Contract(start_date=start_date, rent=self.rent)
        duration = contract.calculate_duration()
        self.assertEqual(duration, 1)
    
    def test_calculate_duration_future_start(self):
        """Test calculate_duration for a start date in the future"""
        future_date = self.today + timedelta(days=61)
        contract = Contract(start_date=future_date, rent=self.rent)
        duration = contract.calculate_duration()
        self.assertEqual(duration, 0)

    def test_current_rent_due_no_days(self):
        """Test current_rent_due for today's start date"""
        start_date = self.today
        contract = Contract(start_date=start_date, rent=self.rent)
        rent_due = contract.current_rent_due()
        self.assertEqual(rent_due, 0)
    
    def test_current_rent_due_past_start(self):
        """Test current_rent_due for a start date in the past"""
        start_date = self.today - timedelta(days=30)
        contract = Contract(start_date=start_date, rent=self.rent)
        rent_due = contract.current_rent_due()
        self.assertEqual(rent_due, 1000)  # 1 month(30 days) * 1000 rent

    def test_current_balance_zero_payment(self):
        """Test current_balance with no payment"""
        start_date = self.today - timedelta(days=10)
        contract = Contract(start_date=start_date, rent=self.rent)
        balance = contract.current_balance()
        self.assertEqual(balance, 1000)  # 1 month(10 days) * 1000 rent

    def test_current_balance_partial_payment(self):
        """Test current_balance with partial payment"""
        start_date = self.today - timedelta(days=15)
        payment = 500
        contract = Contract(start_date=start_date, rent=self.rent, current_rent_payed=payment)
        balance = contract.current_balance()
        self.assertEqual(balance, 500)  # 1 month(15 days) * 1000 rent - 500 payment

    def test_current_balance_full_payment(self):
        """Test current_balance with full payment"""
        start_date = self.today - timedelta(days=15)
        payment = 1000
        contract = Contract(start_date=start_date, rent=self.rent, current_rent_payed=payment)
        balance = contract.current_balance()
        self.assertEqual(balance, 0)  # No balance due

if __name__ == '__main__':
    unittest.main()