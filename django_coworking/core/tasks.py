import time

from celery import shared_task

@shared_task
def send_booking_confirmation(booking_id):
    time.sleep(5)
    print(f"Уведомление для брони {booking_id} отправлено!")