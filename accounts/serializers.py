from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class AttendeeRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'phone_number',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number')
        )

        return user

class OrganizerRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'phone_number',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number'),
            role=User.Role.ORGANIZER
        )

        return user

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'role',
        ]

        read_only_fields = ['id', 'email', 'role']