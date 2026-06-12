from django.urls import path
from .views import MyEndpointView, BookingListView, BookingCancelView

urlpatterns = [
    path('bookings/create/', MyEndpointView.as_view(), name='booking-create'),
    path('bookings/list/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]