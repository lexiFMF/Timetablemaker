from django.shortcuts import render, redirect, get_object_or_404
from .models import Requirement, Timetable
from user.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TimetableForm, RequirementForm
from django.contrib.auth.decorators import user_passes_test
from django import forms
from datetime import datetime, date, timedelta
# Create your views here.
def is_manager(user):
    return user.is_authenticated and user.is_manager

def vector_view(request):
	vector_output = Requirement.objects.all()

	if request.user.is_authenticated:
		# If user is authenticated, set the name to the username
		timetables = Timetable.objects.filter(user=request.user)
	else:
		timetables = []

	context = {'vector_output': vector_output, 'timetables':timetables}
	return render(request, 'requirement.html', context)



@login_required
def edit_timetable(request, timetable_id):
    timetable = get_object_or_404(Timetable, id=timetable_id, user=request.user)
    
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            return redirect('Dashboard')  # Redirect to the dashboard or another page
    else:
        form = TimetableForm(instance=timetable)
    
    return render(request, 'edit_timetable.html', {'form': form})


@user_passes_test(is_manager)
def create_requirement(request):
    if request.method == 'POST':
        form = RequirementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dashboard')  # Redirect to the homepage or another page
    else:
        form = RequirementForm()
    return render(request, 'create_requirement.html', {'form': form})


@login_required
def timetable_view(request):
    user_profile = request.user
    today = datetime.now().date()
    week_dates = [today + timedelta(days=i) for i in range(7)]

    if request.method == 'POST':
        print(request.POST)
        start_times = request.POST.getlist('start_time')
        end_times = request.POST.getlist('end_time')

        for date, start_time, end_time in zip(week_dates, start_times, end_times):
            existing_entry = Timetable.objects.filter(user=request.user, date=date)
            timetable, created = Timetable.objects.get_or_create(user=user_profile, date=date)
            form_data = {
                'date': date,
                'start_time': start_time,
                'end_time': end_time,
            }
            form = TimetableForm(form_data, instance=timetable)
            if form.is_valid() and form_data.get('start_time') and form_data.get('end_time'):
                form.save()
            else:
                timetable.delete()
        return redirect('Dashboard')


    forms = []
    for date in week_dates:  # example for a week
        try:
            timetable = Timetable.objects.get(user=request.user, date=date)
        except Timetable.DoesNotExist:
            timetable = Timetable(user=request.user, date=date)

        forms.append(TimetableForm(instance=timetable))

    context = {
        'week_dates': week_dates,
        'forms': forms,
    }
    return render(request, 'edit_timetable.html', context)










