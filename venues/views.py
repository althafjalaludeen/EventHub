from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Venue
from .serializers import VenueSerializer


class VenueListCreateView(APIView):

    def get_permissions(self):

        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get(self, request):

        venues = Venue.objects.all()

        serializer_instance = VenueSerializer(
            venues,
            many=True
        )

        return Response(data=serializer_instance.data, status=200)

    def post(self, request):

        if request.user.role != 'ORGANIZER':
            return Response(
                {"Message": "Only organizers can register venues."},
                status=403
            )

        serializer_instance = VenueSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(organizer=request.user)

            return Response(data={
                "Message": "Venue Registered Successfully..!",
                "Venue Details": serializer_instance.data
            }, status=201)

        return Response(
            data=serializer_instance.errors,
            status=400
        )


class VenueDetailView(APIView):

    permission_classes = [permissions.AllowAny]

    def get_object(self, venue_id):

        return get_object_or_404(Venue, id=venue_id)

    def get(self, request, venue_id):

        venue = self.get_object(venue_id)

        serializer_instance = VenueSerializer(venue)

        return Response(data=serializer_instance.data, status=200)

    def put(self, request, venue_id):

        if not request.user.is_authenticated:
            return Response(
                {"Message": "Authentication required."},
                status=401
            )

        venue = self.get_object(venue_id)

        if venue.organizer != request.user:
            return Response(
                {"Message": "You cannot update another organizer's venue."},
                status=403
            )

        serializer_instance = VenueSerializer(
            venue,
            data=request.data,
            partial=True
        )

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Venue Updated Successfully..!",
                "Venue Details": serializer_instance.data
            }, status=200)

        return Response(
            data=serializer_instance.errors,
            status=400
        )

    def delete(self, request, venue_id):

        if not request.user.is_authenticated:
            return Response(
                {"Message": "Authentication required."},
                status=401
            )

        venue = self.get_object(venue_id)

        if venue.organizer != request.user:
            return Response(
                {"Message": "You cannot delete another organizer's venue."},
                status=403
            )

        venue.delete()

        return Response(
            {"Message": "Venue Deleted Successfully..!"},
            status=200
        )