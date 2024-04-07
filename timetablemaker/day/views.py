from django.shortcuts import render
from .models import Day
from django.http import HttpResponse
from user.models import UserProfile
from django.contrib.auth.decorators import user_passes_test
from .forms import DayForm

from datetime import date
# Create your views here.

def hello_world_view(request):
	if request.user.is_authenticated:
		# If user is authenticated, set the name to the username
		context = {'name': request.user.username}
	else:
		# If user is not authenticated, set a default name or handle as needed
		context = {'name': 'Guest'}
	return render(request, 'hello.html', context)

def workday_view(request):

	selected_date = date.today()
	try:
		# Retrieve Day instance based on the selected date (assuming one-to-one relationship or appropriate filter)
		day_instance = Day.objects.get(date=selected_date)
		schedule_output = day_instance.algo()[0]  # Adjust as per your model design
		df_html = schedule_output.to_html(classes='myDataFrame' ,escape=False, index=False)
		context = {
		'schedule_output': df_html,
		#'users_with_hours': users_with_hours
		}

	except:
		#context = {}
		# Retrieve Day instance based on the selected date (assuming one-to-one relationship or appropriate filter)
		day_instance = Day.objects.get(date=selected_date)
		schedule_output = day_instance.algo()[0]  # Adjust as per your model design
		df_html = schedule_output.to_html(classes='myDataFrame' ,escape=False, index=False)
		context = {
		'schedule_output': df_html,
		#'users_with_hours': users_with_hours
		}

	return render(request, 'workday.html', context)

def is_manager(user):
    return user.is_authenticated and user.is_manager

@user_passes_test(is_manager)
def create_day(request):
    if request.method == 'POST':
        form = DayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage or another page
    else:
        form = DayForm()
    return render(request, 'create_day.html', {'form': form})
