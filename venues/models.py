from django.db import models
from django.conf import settings

class Venue(models.Model):

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    capacity = models.PositiveIntegerField()

    contact_number = models.CharField(max_length=15)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='venues'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
