from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import BookingCreateSerializer, BookingListSerializer
from ..models import Booking
from ..services.booking_service import create_booking, cancel_booking
from ..tasks import send_booking_confirmation

class MyEndpointView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            print(f"🔥 ИДЕТ БРОНЬ: юзер_id={request.user.id}, ресурс_id={serializer.validated_data.get('resource_id')}")
            booking = create_booking(user_id=request.user.id, **serializer.validated_data)
            send_booking_confirmation.delay(booking.id)
            return Response(
                {"message": "Бронирование создано", "id": booking.id},
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"🔥 РЕАЛЬНАЯ ОШИБКА: {repr(e)}")  # <--- Добавь эту строчку
            return Response({"error": "Что-то пошло не так на сервере"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookingListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        bookings = Booking.objects.select_related(
            "user",
            "resource"
        ).all()

        serializer = BookingListSerializer(
            bookings,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        user_id = request.user.id
        try:
            cancel_booking(pk, user_id)
            return Response({"message": "Бронь отменена"})
        except Booking.DoesNotExist:
            return Response({"error": "Бронь не найдена"}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



