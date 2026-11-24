from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'attendee',
        'event',
        'ticket_number',
        'status',
        'registered_at',
    )

    list_filter = ('status', 'registered_at')

    search_fields = (
        'attendee__username',
        'attendee__email',
        'event__title',
        'ticket_number',
    )

    readonly_fields = (
        'ticket_number',
        'registered_at',
    )

    ordering = ('-registered_at',)