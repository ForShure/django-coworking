from rest_framework import serializers
from ..models import Booking


class BookingCreateSerializer(serializers.Serializer):
    resource_id = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

class BookingListSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(
        source='resource.name',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'user_id',
            'resource_name',
            'start_time',
            'end_time',
            'status'
        ]

