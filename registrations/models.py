import uuid
from django.db import models
from django.conf import settings


class Registration(models.Model):

    class Status(models.TextChoices):
        BOOKED = 'BOOKED', 'Booked'
        CANCELLED = 'CANCELLED', 'Cancelled'

    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='registrations'
    )

    ticket_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.BOOKED
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.username} - {self.event.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['attendee', 'event'],
                name='unique_attendee_event'
            )
        ]