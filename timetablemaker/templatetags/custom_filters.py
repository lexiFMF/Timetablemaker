from django import template

register = template.Library()

@register.filter(name='add_one')
def add_one(value):
    return value + 1


@register.filter(name='add_id')
def add_id(field, counter):
    return field.as_widget(attrs={'id': f'id_{field.name}_{counter}'})