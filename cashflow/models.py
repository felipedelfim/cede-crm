from django.db import models
from django.utils import timezone

class Transaction(models.Model):
	def __str__(self):
		return self.item.name + ' (' + str(self.amount) + ') '
	def was_paid(self):
		return self.paid_at is not None
	def pay(self):
		self.paid_at = timezone.now()
		self.save()
	item = models.ForeignKey('Item', on_delete=models.CASCADE)
	person = models.ForeignKey('Person', on_delete=models.CASCADE)
	method = models.ForeignKey('Method', on_delete=models.CASCADE)
	amount = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	comments = models.TextField(blank=True)
	paid_at = models.DateTimeField(null=True)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class Method(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class Item(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	value = models.FloatField(default=1.00)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class Person(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	group = models.ForeignKey('Group', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class Group(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
