from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login
from timetable.models import Timetable

# Create your views here.
@login_required
def home_view(request):
	if request.user.is_authenticated:
		timetables = Timetable.objects.filter(user=request.user)
	else:
		timetables = None
	return render(request, 'home.html', {'timetables': timetables})

def account_management_view(request):
	if request.method == 'POST':
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your account has been updated successfully!')
			return redirect('account_management')
	else:
		user_form = UserUpdateForm(instance=request.user)
		profile_form = ProfileUpdateForm(instance=request.user)
	
	context = {
		'user_form': user_form,
		'profile_form': profile_form
	}
	
	return render(request, 'account_management.html', context)


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def account_update(request):
	if request.method == 'POST':
		form = CustomUserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('Dashboard')  # Redirect to the same page or another page
	else:
		form = CustomUserUpdateForm(instance=request.user)
	return render(request, 'account_update.html', {'form': form})

def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = CustomUserCreationForm()
	return render(request, 'register.html', {'form': form})

def user_login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('Dashboard')  # Replace 'home' with your home page URL name
	return render(request, 'login.html')