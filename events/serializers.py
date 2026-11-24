from rest_framework import serializers
from .models import Event, EventCategory


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory

        fields = [
            'id',
            'name',
            'description',
            'created_at',
        ]

        read_only_fields = ['id', 'created_at']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event

        fields = [
            'id',
            'title',
            'description',
            'category',
            'organizer',
            'venue',
            'start_date',
            'end_date',
            'capacity',
            'available_seats',
            'ticket_price',
            'image',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'organizer',
            'available_seats',
            'created_at',
            'updated_at',
        ]

    def validate_venue(self, value):

        request = self.context.get('request')

        if request and value.organizer != request.user:
            raise serializers.ValidationError(
                "You can only select your own venues."
            )

        return value

    def validate_ticket_price(self, value):

        if value < 0:
            raise serializers.ValidationError(
                "Ticket price cannot be negative."
            )

        return value

    def validate(self, data):

        start_date = data.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )

        end_date = data.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        capacity = data.get(
            'capacity',
            getattr(self.instance, 'capacity', None)
        )

        venue = data.get(
            'venue',
            getattr(self.instance, 'venue', None)
        )

        # Validate event dates
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                "End date must be after start date."
            )

        # Validate positive capacity
        if capacity is not None and capacity <= 0:
            raise serializers.ValidationError({
                "capacity": "Event capacity must be greater than zero."
            })

        # Prevent capacity below existing bookings
        if capacity is not None and self.instance:

            booked_seats = (
                self.instance.capacity - self.instance.available_seats
            )

            if capacity < booked_seats:
                raise serializers.ValidationError({
                    "capacity": "Capacity cannot be less than the number of existing bookings."
                })

        # Validate venue capacity
        if venue and capacity > venue.capacity:
            raise serializers.ValidationError({
                "capacity": "Event capacity cannot exceed venue capacity."
            })

        return data