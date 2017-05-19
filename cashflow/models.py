from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Transaction(models.Model):
	def __str__(self):
		return self.item.name + ' (' + str(self.amount) + ') '
	def was_paid(self):
		return self.paid_at is not None
	def pay(self):
		self.paid_at = timezone.now()
	item = models.ForeignKey('Item', on_delete=models.CASCADE)
	person = models.ForeignKey('Person', on_delete=models.CASCADE)
	method = models.ForeignKey('Method', on_delete=models.CASCADE)
	item_value = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	amount = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	total = models.DecimalField(default=1.00, max_digits=6, decimal_places=2)
	comments = models.TextField(blank=True)
	paid_at = models.DateField(null=True, blank=True)
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
	cost_center = models.ForeignKey('CostCenter', on_delete=models.CASCADE)
	value = models.FloatField(default=1.00)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class CostCenter(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)

class Person(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	phone_number = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\(?\d{2}?\)?\d{8,10}$', message="Phone number must be entered in the format: '(11)999999999'. Up to 15 digits allowed.")], blank=True) # validators should be a list
	group = models.ForeignKey('Group', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated

class Group(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True) # set when it's created
	updated_at = models.DateTimeField(auto_now=True) # set every time it's updated
