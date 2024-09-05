
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Registration

@receiver(post_save, sender=Registration)
def notify_event_creator(sender, instance, created, **kwargs):
    if created:
        event = instance.event
        creator = event.created_by
        subject = f"New Registration for Your Event: {event.name}"
        message = f"{instance.user.username} has registered for your event '{event.name}'."
        send_mail(
            subject,
            message,
            'basilmkurian.bmk.official@gmail.com',  # Replace with your email
            [creator.email],
            fail_silently=False,
        )
