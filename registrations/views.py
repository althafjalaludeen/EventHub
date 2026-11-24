from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from events.models import Event
from .models import Registration
from .serializers import RegistrationSerializer
from django.utils import timezone


class RegistrationListCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        if request.user.role != 'ATTENDEE':
            return Response(
                {"Message": "Only attendees can view registrations."},
                status=status.HTTP_403_FORBIDDEN
            )

        registrations = Registration.objects.filter(
            attendee=request.user
        )

        serializer = RegistrationSerializer(
            registrations,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        if request.user.role != 'ATTENDEE':
            return Response(
                {"Message": "Only attendees can register for events."},
                status=status.HTTP_403_FORBIDDEN
            )

        event_id = request.data.get('event')

        if not event_id:
            return Response(
                {"Message": "Event ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():

            event = get_object_or_404(
                Event.objects.select_for_update(),
                id=event_id
            )

            if event.status != 'PUBLISHED':
                return Response(
                    {"Message": "This event is not available for registration."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if event.start_date <= timezone.now():
                return Response(
                    {"Message": "Registration for this event is closed."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if event.available_seats <= 0:
                return Response(
                    {"Message": "No seats available."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            registration = Registration.objects.filter(
                attendee=request.user,
                event=event
            ).first()

            if registration:

                if registration.status == 'BOOKED':
                    return Response(
                        {"Message": "You have already registered for this event."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                registration.status = 'BOOKED'
                registration.save()

            else:

                registration = Registration.objects.create(
                    attendee=request.user,
                    event=event
                )

            event.available_seats -= 1
            event.save(update_fields=['available_seats'])

        serializer = RegistrationSerializer(registration)

        return Response(
            {
                "Message": "Event registration successful.",
                "Registration": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class RegistrationDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, registration_id):

        if request.user.role != 'ATTENDEE':
            return Response(
                {"Message": "Only attendees can cancel registrations."},
                status=status.HTTP_403_FORBIDDEN
            )

        with transaction.atomic():

            registration = get_object_or_404(
                Registration.objects.select_for_update(),
                id=registration_id,
                attendee=request.user
            )

            if registration.status == 'CANCELLED':
                return Response(
                    {"Message": "Registration already cancelled."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            event = Event.objects.select_for_update().get(
                id=registration.event_id
            )

            registration.status = 'CANCELLED'
            registration.save(update_fields=['status'])

            event.available_seats += 1
            event.save(update_fields=['available_seats'])

        return Response(
            {"Message": "Registration cancelled successfully."},
            status=status.HTTP_200_OK
        )