from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Role(models.TextChoices):
        ATTENDEE = 'ATTENDEE', 'Attendee'
        ORGANIZER = 'ORGANIZER', 'Organizer'
        ADMIN = 'ADMIN', 'Administrator'

    email = models.EmailField(unique=True)

    role = models.CharField(max_length=20,
        choices=Role.choices,
        default=Role.ATTENDEE
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email