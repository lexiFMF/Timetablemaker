from django.db import models
from organisation.models import Location
from user.models import UserProfile
import numpy as np

# Create your models here.

def create_vector(start_time, end_time):
	start_hour = start_time.hour  # Get the hour from the start time
	end_hour = end_time.hour  # Get the hour from the end time

	l = [i for i in range(min(start_hour, end_hour), max(start_hour, end_hour))]
	

	if start_hour < end_hour:
		vector = [0] * 24
		for i in range(len(l)):
			vector[l[i]] = 1
	else:
		vector = [1] * 24
		for i in range(len(l)):
			vector[l[i]] = 0

	return vector


class Requirement(models.Model):
	name = models.CharField(max_length=255)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	open_time = models.IntegerField(default=8)
	workday_len = models.IntegerField(default=16)
	int1 = models.IntegerField(default=1)
	work1 = models.IntegerField(default=2)
	int2 = models.IntegerField(default=7)
	work2 = models.IntegerField(default=4)
	int3 = models.IntegerField(default=6)
	work3 = models.IntegerField(default=5)
	work4 = models.IntegerField(default=3)


	def __str__(self):
		return self.name

	def req_vector(self):
		vector = []

		for i in range(self.int1):
			vector.append(self.work1)
		for i in range(self.int2):
			vector.append(self.work2)
		for i in range(self.int3):
			vector.append(self.work3)
		for i in range(self.workday_len - (self.int3 + self.int2 + self.int1)):
			vector.append(self.work4)
		for i in range(len(vector), 24):
			vector.append(0)
	
		self.open_time = self.open_time % len(vector)  # Normalize n to be within the range of the list length
	
		return vector[-(self.open_time - 1):] + vector[:-(self.open_time - 1)]

			



class Timetable(models.Model):
	user = models.ForeignKey(UserProfile, related_name='timetables', on_delete=models.CASCADE, null=True)
	date = models.DateField()
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)
	class Meta:
		"""
		Meta class to add constraints and options for the Timetable model.
		"""
		# Define unique_together constraint to ensure each user can have only one timetable object per date
		unique_together = [['user', 'date']]

	def __str__(self):
		return self.user.username + str(self.date)

	def work_vector(self):
		vector = create_vector(self.start_time, self.end_time)
		return vector

	def availability(self):
		return str(self.start_time.hour) + ' - ' + str(self.end_time.hour)

class Will_Work(models.Model):
	user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	date = models.DateField()
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)

	class Meta:
		"""
		Meta class to add constraints and options for the Timetable model.
		"""
		# Define unique_together constraint to ensure each user can have only one timetable object per date
		unique_together = [['user', 'date']]

	def __str__(self):
		return self.user.username + str(self.date)

	@classmethod
	def create_or_update(cls, user, date, start_time, end_time):
		"""
		Create or update a timetable object for the given user and date with start and end time data.

		Args:
		- user: User object.
		- date: Date for the timetable object.
		- start_time: Start time for the timetable object.
		- end_time: End time for the timetable object.

		Returns:
		- Timetable object.
		"""
		# Get existing timetable object or create a new one
		timetable_obj, created = cls.objects.get_or_create(user=user, date=date)

		# Update start and end time data
		timetable_obj.start_time = start_time
		timetable_obj.end_time = end_time
		timetable_obj.save()  # Save the updated timetable object

		return timetable_obj




