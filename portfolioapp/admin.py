from django.contrib import admin

from .models import Show


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('date', 'venue', 'city', 'state', 'ticket_url')
    list_filter = ('state',)
    ordering = ('date',)
