from rest_framework import serializers
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue

        fields = [
            'id',
            'name',
            'description',
            'address',
            'city',
            'state',
            'pincode',
            'capacity',
            'contact_number',
            'organizer',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'organizer',
            'created_at',
            'updated_at',
        ]

    def validate_capacity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Venue capacity must be greater than zero."
            )

        return value