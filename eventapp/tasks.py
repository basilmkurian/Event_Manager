# events/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event, Registration

@shared_task
def send_event_reminders():
    now = timezone.now()
    upcoming_events = Event.objects.filter(start_time__gt=now, start_time__lt=now + timezone.timedelta(hours=24))

    for event in upcoming_events:
        registrations = Registration.objects.filter(event=event)
        for registration in registrations:
            send_mail(
                subject=f'Reminder: Upcoming Event {event.name}',
                message=f'Dear {registration.user.username},\n\nThis is a reminder that the event "{event.name}" is happening on {event.start_time.strftime("%Y-%m-%d %H:%M")}.\n\nBest regards,\nEvent Management Team',
                from_email='basilmkurian.bmk.official@gmail.com',
                recipient_list=[registration.user.email],
                fail_silently=False,
            )
