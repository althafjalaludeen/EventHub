from django.contrib import admin
from .models import Event, EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
    'id',
    'title',
    'organizer',
    'category',
    'start_date',
    'capacity',
    'available_seats',
    'status',
)

    list_filter = ('status', 'category', 'start_date')

    search_fields = ('title', 'venue', 'organizer__email')

    ordering = ('-created_at',)