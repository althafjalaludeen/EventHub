from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from accounts.serializers import AttendeeRegistrationSerializer
from accounts.serializers import OrganizerRegistrationSerializer
from accounts.serializers import UserProfileSerializer


class AttendeeRegistrationView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        form_data = request.data

        serializer_instance = AttendeeRegistrationSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Attendee Registered Successfully..!",
                "User Details": serializer_instance.data
            }, status=201)

        else:

            return Response(data=serializer_instance.errors, status=400)


class OrganizerRegistrationView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        form_data = request.data

        serializer_instance = OrganizerRegistrationSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Organizer Registered Successfully..!",
                "User Details": serializer_instance.data
            }, status=201)

        else:

            return Response(data=serializer_instance.errors, status=400)

class UserProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer_instance = UserProfileSerializer(request.user)

        return Response(data=serializer_instance.data, status=200)

    def put(self, request):

        form_data = request.data

        serializer_instance = UserProfileSerializer(
            request.user,
            data=form_data,
            partial=True
        )

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data={
                "Message": "Profile Updated Successfully..!",
                "User Details": serializer_instance.data
            }, status=200)

        else:

            return Response(data=serializer_instance.errors, status=400)