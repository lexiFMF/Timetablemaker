from django.db import models
from timetable.models import Requirement, Timetable, Will_Work
from user.models import UserProfile
from source import algo
from itertools import combinations
import numpy as np
import pandas as pd
from datetime import datetime


# Create your models here.

def vec_to_time(x):
	start_hour = None
	end_hour = None
	vector = list(x)
	# Handle case where vector starts with 1 (evening start and ends in the morning)
	if 1 in vector:
		if vector[0] == 1:
			# Find the first occurrence of 0 to determine the end hour
			end_hour = vector.index(0)
			
			# The start hour would be 24 hours before the end_hour due to spillage of ones
			start_hour = 23 - vector[::-1].index(0)
			start_time = datetime.strptime(f"{start_hour + 1}:00", "%H:%M")
			end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")
		else:
			# Find the first occurrence of 1 to determine the start hour
			start_hour = vector.index(1)
			
			# Find the last occurrence of 1 to determine the end hour
			end_hour = 23 - vector[::-1].index(1)
			start_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
			end_time = datetime.strptime(f"{end_hour + 1}:00", "%H:%M")
	
		return start_time.hour, end_time.hour
	else:
		return False


def addition_with_ceiling(vectors_combo, ceiling):
	result = [0]*24
	length = len(vectors_combo)

	for vector in vectors_combo:
		for i in range(len(vector)):
			element_sum = result[i] + vector[i]
			result[i] = min(element_sum, ceiling[i])
			if element_sum > ceiling[i]:
				vector[i] = 0

	return np.array(result), vectors_combo


def transform_tuples_to_strings(tuple_list, dash):
	transformed_list = []
	
	for tup in tuple_list:
		x, y = tup  # Unpack tuple
		if dash == True:
			transformed_list.append(f"{x}-{y}")  # Format string as x-y and append to list
		else:
			transformed_list.append(f"{x} {y}")
	return transformed_list


class Day(models.Model):
	date = models.DateField(unique=True)
	requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE, null=True)


	def __str__(self):
		return f"{self.requirement.name} - {self.date}"
		
	def workers(self):
		start_work_date = self.date

		timetables = Timetable.objects.filter(date=start_work_date)
		
		vector_tuples = []
		for timetable in timetables:
			vector = timetable.work_vector()
			user_id = timetable.user # Assuming UserProfile has a OneToOneField to User
			vector_tuples.append((vector, user_id))

		return vector_tuples

	def algo(self):
		sumvec = []
		working = []
		hours = []
		requirement = np.array((self.requirement.req_vector()))
		all_can_work = self.workers()
		for i in range(1, len(all_can_work)):	
			for combo in combinations(all_can_work, i+1):
				times = []
				vectors = [t[0] for t in combo]
				sumvec.append(addition_with_ceiling(vectors, requirement)[0])
				working.append(list(t[1] for t in combo))

				for vector in vectors:
					times.append(vec_to_time(vector))
				hours.append(times)

		dataset = zip(sumvec, working, hours)
		filtered_sum = []
		filtered_working = []
		filtered_hours = []
		for sumvect, working, hours in dataset:
			VI_vec = np.array([0]*24)
			for user in working:
				if user.can_VI:
					timetable = Timetable.objects.get(date=self.date, user=user)
					VI_vec += np.array(timetable.work_vector())
			checkpoint = requirement - VI_vec
			if all(checkpoint[i] != requirement[i] or checkpoint[i] == 0 for i in range(len(checkpoint))):
				filtered_sum.append(sumvect)
				filtered_working.append(working)
				filtered_hours.append(hours)

		minimum = float('inf')
		indexes = []
		for i in range(len(filtered_sum)):
			distance = np.linalg.norm(np.array(filtered_sum[i]) - requirement)
			if distance < minimum:
				minimum = distance
				indexes = []
				indexes.append(i)
			elif distance == minimum:
				indexes.append(i)
		print(indexes)
		working_final = filtered_working[indexes[0]]
		vi_inter = []
		hours_final = transform_tuples_to_strings(list(filtered_hours[indexes[0]]), True)
		availability = []
		for i in working_final:
			timetable = Timetable.objects.get(user=i, date=self.date).availability()
			availability.append(timetable)
			if i.can_VI:
				vi_inter.append('VI')
			else:
				vi_inter.append('')

		data = {
			'Name': transform_tuples_to_strings(zip(working_final, vi_inter), False),
			'Hours': hours_final,
			'Availability': availability
		}
		df = pd.DataFrame(data)
		df['Start'] = df['Hours'].str.split('-').str[0].astype(int)
		df['End'] = df['Hours'].str.split('-').str[1].astype(int)

		smallest_start = df['Start'].min()

		df['AdjustedEnd'] = df.apply(lambda row: row['End'] + 24 if row['End'] < smallest_start else row['End'], axis=1)
		df_sorted = df.sort_values(by=['Start', 'AdjustedEnd'], ascending=[True, True])

		df_to_render = df_sorted.drop(['Start', 'End', 'AdjustedEnd'], axis=1)

		tuples = list(zip(filtered_working[indexes[0]], filtered_hours[indexes[0]]))
		for worker, time in tuples:
			willwork = Will_Work.create_or_update(worker, str(self.date), f"{time[0]}:00", f"{time[1]}:00")
			willwork.save()


		return df_to_render, zip(filtered_working, filtered_hours, filtered_sum)
















