from django.db import models
from django.conf import settings

class BookingStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"
    CANCELLED = "CANCELLED", "Cancelled"

class Resource(models.Model):
    RESOURCE_TYPES = (
        ("open_space", "Open Space"),
        ("meeting_room", "Meeting Room"),
    )

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)

    def __str__(self):
        return f"{self.name} ({self.type})"

class MeetingRoom(models.Model):
    resource = models.OneToOneField(
        Resource,
        on_delete=models.CASCADE,
        related_name="meeting_room"
    )

    capacity = models.IntegerField()
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)

    def __str__(self):
        return f"MeetingRoom: {self.resource.name}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="bookings")

    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)

    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource.name} | {self.start_time} - {self.end_time}"