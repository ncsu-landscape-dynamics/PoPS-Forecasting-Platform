import os

from django import template


register = template.Library()

@register.simple_tag
def get_staff_approved(value, queryset):
    output = []
    if queryset:
        for cs in queryset:
            if cs.staff_approved:
                output.append(cs)
    return output

@register.simple_tag
def get_user_created(value, queryset):
    output = []
    if queryset:
        for cs in queryset:
            if cs.created_by==value:
                output.append(cs)
    return output

