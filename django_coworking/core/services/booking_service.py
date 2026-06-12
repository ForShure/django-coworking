import datetime

from django.utils import timezone
from django.db.models import Q
from ..models import Booking, Resource, BookingStatus
from django.contrib.auth import get_user_model

User = get_user_model()

def create_booking(user_id: int, resource_id: int, start_time: datetime, end_time: datetime) -> Booking:

    if start_time >= end_time:
        raise ValueError("Start time must be before end time")

    if start_time < timezone.now():
        raise ValueError("Start time must be in the future")

    user = User.objects.get(id=user_id)
    resource = Resource.objects.get(id=resource_id)

    overlapping_bookings = (Booking.objects
    .filter(
        resource_id=resource_id
    )
    .filter(
        Q(start_time__lt=end_time) &
        Q(end_time__gt=start_time) &
        Q(status__in=[BookingStatus.PENDING, BookingStatus.PAID])
    ))

    if overlapping_bookings.exists():
        raise ValueError("Время занято")

    booking = Booking.objects.create(
        user=user,
        resource=resource,
        start_time=start_time,
        end_time=end_time,
        status=BookingStatus.PENDING,
    )
    return booking


def cancel_booking(booking_id: int, user_id: int) -> Booking:
    booking = Booking.objects.get(id=booking_id)

    if booking.user.id != user_id:
        raise PermissionError("Это не ваша бронь")

    if booking.status == BookingStatus.CANCELLED:
        raise ValueError("Status cannot be cancelled")
    if booking.start_time < timezone.now():
        raise ValueError("Start time must be in the future")

    booking.status = BookingStatus.CANCELLED
    booking.save()
    return booking

