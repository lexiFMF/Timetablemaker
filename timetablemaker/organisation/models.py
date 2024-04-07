from django.db import models
from user.models import UserProfile

# Create your models here.

class Company(models.Model):
	name = models.CharField(max_length=100)
	owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Location(models.Model):
	name = models.CharField(max_length=100)
	capacity = models.IntegerField()
	company = models.ForeignKey(Company, on_delete=models.CASCADE)

	def __str__(self):
		return self.name