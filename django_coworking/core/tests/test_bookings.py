import pytest
from rest_framework.test import APIClient
from core.models import Resource, Booking
from django.contrib.auth import get_user_model
from django.test import override_settings


User = get_user_model()

@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_create_booking_success():
    test_client = User.objects.create_user(username="test_boy", password="123")
    test_resource = Resource.objects.create(name="Test Room", type="open_space")

    client = APIClient()
    client.force_authenticate(user=test_client)

    response = client.post(
        '/api/bookings/create/',
        data={
            "resource_id": test_resource.id,
            "start_time": "2026-06-20T10:00:00",
            "end_time": "2026-06-20T12:00:00"
        },
        format='json'
    )

    assert response.status_code == 201
