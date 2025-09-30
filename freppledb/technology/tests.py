"""
This file demonstrates writing tests using the unittest module. 

You can execute the tests with the command:
  frepplectl test my_app
"""

from django.test import TestCase

class SimpleTest(TestCase):
  def test_basic_addition(self):
    """
    Tests that 1 + 1 always equals 2.
    """
    self.assertEqual(1 + 1, 2)
