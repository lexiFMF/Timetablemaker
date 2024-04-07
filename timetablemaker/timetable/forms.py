from django import forms
from .models import Timetable, Requirement
from datetime import datetime, timedelta
from django.forms.widgets import SelectDateWidget, TimeInput
from django.forms.widgets import DateTimeInput


class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ['name', 'location', 'open_time', 'workday_len', 'int1', 'work1', 'int2', 'work2', 'int3', 'work3', 'work4']

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'class': 'form-control'})
        # Add additional attributes or customizations as needed

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }