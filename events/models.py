from django.db import models
from django.conf import settings


class EventCategory(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'
        CANCELLED = 'CANCELLED', 'Cancelled'

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )

    venue_name = models.CharField(
    max_length=200,
    blank=True,
    default=''
    )

    venue = models.ForeignKey(
    'venues.Venue',
    on_delete=models.PROTECT,
    related_name='events',
    null=True,
    blank=True
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    capacity = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField()

    ticket_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    image = models.ImageField(
        upload_to='event_images/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
