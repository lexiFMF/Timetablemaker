from django import forms
from .models import Day
from timetable.models import Requirement

class DayForm(forms.ModelForm):
    requirement = forms.ModelChoiceField(queryset=Requirement.objects.all(), label='Requirement', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Day
        fields = ['requirement', 'date']