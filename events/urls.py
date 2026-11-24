from django.urls import path
from .views import (
    EventListCreateView,
    EventDetailView,
    EventCategoryListCreateView,
    EventCategoryDetailView
)

urlpatterns = [

    path('', EventListCreateView.as_view(), name='event-list-create'),

    path('categories/', EventCategoryListCreateView.as_view(), name='category-list-create'),

    path('<int:event_id>/', EventDetailView.as_view(), name='event-detail'),

    path('categories/<int:category_id>/', EventCategoryDetailView.as_view(), name='category-detail'),

]