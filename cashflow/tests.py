import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Transaction, Item, Person, Method

class TransactionMethodTests(TestCase):

	def test_was_paid(self):
		paid_transaction = Transaction(item=Item('Item 1'),person=Person('Person 1'),method=Method('Cash'),paid_at=timezone.now())
		self.assertIs(paid_transaction.was_paid(), True)

	def test_was_unpaid(self):
		unpaid_transaction = Transaction(item=Item('Item 1'),person=Person('Person 1'),method=Method('Cash'))
		self.assertIs(unpaid_transaction.was_paid(), False)

	def test_pay(self):
		transaction = Transaction(item=Item('Item 1'),person=Person('Person 1'),method=Method('Cash'))
		transaction.pay()
		self.assertIs(transaction.was_paid(), True)

	def test_paid_transacted_at(self):
		transaction = Transaction(item=Item('Item 1'),person=Person('Person 1'),method=Method('Cash'),paid_at=datetime.datetime(2017, 1, 1))
		self.assertEqual(transaction.transacted_at, transaction.paid_at)

	def test_unpaid_transacted_at(self):
		transaction = Transaction(item=Item('Item 1'),person=Person('Person 1'),method=Method('Cash'))
		self.assertEqual(transaction.transacted_at, transaction.created_at)
