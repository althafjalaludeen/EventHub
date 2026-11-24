from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration

        fields = [
            'id',
            'attendee',
            'event',
            'ticket_number',
            'status',
            'registered_at',
        ]

        read_only_fields = [
            'id',
            'attendee',
            'ticket_number',
            'status',
            'registered_at',
        ]