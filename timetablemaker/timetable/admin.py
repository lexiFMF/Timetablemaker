from django.contrib import admin
from datetime import date

from .models import Timetable, Requirement, Will_Work
# Register your models here.

admin.site.register(Requirement)
admin.site.register(Will_Work)


def change_to_today(modeladmin, request, queryset):
    queryset.update(date=date.today())
change_to_today.short_description = 'Update date to today'


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
	list_display = ['user', 'date', 'start_time', 'end_time']
	actions = [change_to_today]
