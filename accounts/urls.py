from django.urls import path
from .views import AttendeeRegistrationView, OrganizerRegistrationView, UserProfileView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('api/accounts/register/', AttendeeRegistrationView.as_view(), name='attendee-register'),

    path('organizer/register/', OrganizerRegistrationView.as_view(), name='organizer-register'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profile/', UserProfileView.as_view(), name='user-profile'),

]