from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Event, EventCategory
from .serializers import EventSerializer, EventCategorySerializer
from django.db.models import ProtectedError


class EventListCreateView(APIView):

    def get_permissions(self):

        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get(self, request):

        if request.user.is_authenticated and request.user.role == 'ORGANIZER':

            events = Event.objects.filter(
                models.Q(status='PUBLISHED') |
                models.Q(organizer=request.user)
            ).distinct()

        else:

            events = Event.objects.filter(status='PUBLISHED')

        search = request.query_params.get('search')

        category = request.query_params.get('category')

        venue = request.query_params.get('venue')

        status = request.query_params.get('status')

        upcoming = request.query_params.get('upcoming')

        if search:
            events = events.filter(title__icontains=search)

        if category:
            events = events.filter(category_id=category)

        if venue:
            events = events.filter(venue__name__icontains=venue)

        if status and request.user.is_authenticated and request.user.role == 'ORGANIZER':
            events = events.filter(status=status)

        if upcoming == 'true':
            events = events.filter(start_date__gte=timezone.now())

        serializer_instance = EventSerializer(events, many=True)

        return Response(data=serializer_instance.data, status=200)

    def post(self, request):

        if request.user.role != 'ORGANIZER':
            return Response(
                {"Message": "Only organizers can create events."},
                status=403
            )

        serializer_instance = EventSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer_instance.is_valid():

            serializer_instance.save(
                organizer=request.user,
                available_seats=serializer_instance.validated_data['capacity']
            )

            return Response(data={
                "Message": "Event Created Successfully..!",
                "Event Details": serializer_instance.data
            }, status=201)

        return Response(
            data=serializer_instance.errors,
            status=400
        )


class EventDetailView(APIView):

    permission_classes = [permissions.AllowAny]

    def get_object(self, event_id):

        return get_object_or_404(Event, id=event_id)

    def get(self, request, event_id):

        event = self.get_object(event_id)

        if event.status != 'PUBLISHED':

            if not request.user.is_authenticated or event.organizer != request.user:
                return Response(
                    {"Message": "Event not found."},
                    status=404
                )

        serializer_instance = EventSerializer(event)

        return Response(data=serializer_instance.data, status=200)

    def put(self, request, event_id):

        if not request.user.is_authenticated:
            return Response(
                {"Message": "Authentication required."},
                status=401
            )

        event = self.get_object(event_id)

        if event.organizer != request.user:
            return Response(
                {"Message": "You cannot update another organizer's event."},
                status=403
            )

        serializer_instance = EventSerializer(
            event,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Event Updated Successfully..!",
                "Event Details": serializer_instance.data
            }, status=200)

        return Response(
            data=serializer_instance.errors,
            status=400
        )

    def delete(self, request, event_id):

        if not request.user.is_authenticated:
            return Response(
                {"Message": "Authentication required."},
                status=401
            )

        event = get_object_or_404(Event, id=event_id)

        if event.organizer != request.user:
            return Response(
                {"Message": "You cannot delete another organizer's event."},
                status=403
            )

        try:
            event.delete()

        except ProtectedError:
            return Response(
                {"Message": "This event cannot be deleted because registrations exist."},
                status=400
            )

        return Response(
            {"Message": "Event deleted successfully."},
            status=200
        )


class EventCategoryListCreateView(APIView):

    def get_permissions(self):

        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get(self, request):

        categories = EventCategory.objects.all()

        serializer_instance = EventCategorySerializer(
            categories,
            many=True
        )

        return Response(data=serializer_instance.data, status=200)

    def post(self, request):

        if request.user.role != 'ORGANIZER':
            return Response(
                {"Message": "Only organizers can create categories."},
                status=403
            )

        serializer_instance = EventCategorySerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Category Created Successfully..!",
                "Category Details": serializer_instance.data
            }, status=201)

        return Response(data=serializer_instance.errors, status=400)


class EventCategoryDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, category_id):

        if request.user.role != 'ORGANIZER':
            return Response(
                {"Message": "Only organizers can update categories."},
                status=403
            )

        category = get_object_or_404(EventCategory, id=category_id)

        serializer_instance = EventCategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Category Updated Successfully..!",
                "Category Details": serializer_instance.data
            }, status=200)

        return Response(data=serializer_instance.errors, status=400)

    def delete(self, request, category_id):

        if request.user.role != 'ORGANIZER':
            return Response(
                {"Message": "Only organizers can delete categories."},
                status=403
            )

        category = get_object_or_404(EventCategory, id=category_id)

        category.delete()

        return Response(
            {"Message": "Category Deleted Successfully..!"},
            status=200
        )
