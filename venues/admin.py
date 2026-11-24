from django.contrib import admin
from .models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'organizer',
        'city',
        'state',
        'capacity',
        'created_at',
    )

    list_filter = ('city', 'state')

    search_fields = (
        'name',
        'city',
        'organizer__email',
    )

    ordering = ('-created_at',)