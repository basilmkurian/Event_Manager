from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from .forms import RegisterForm, EventForm, Event
from .models import Event, Registration
from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def signup(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(response, "signup.html", {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def event_list(request):
    events = Event.objects.all().order_by('-start_time')
    return render(request, 'event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})


@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.capacity > Registration.objects.filter(event=event).count():
        registration = Registration(event=event, user=request.user)
        registration.save()

        # Send a confirmation email
        send_mail(
            subject=f'Registration Confirmation for {event.name}',
            message=f'Thank you for registering for {event.name}. The event is scheduled for {event.start_time.strftime("%Y-%m-%d %H:%M")}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )
        messages.success(request, 'You have registered for the event successfully!')
    else:
        messages.error(request, 'Sorry, this event is full.')
    return redirect('event_list')


@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'my_registrations.html', {'registrations': registrations})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Ensure that only the creator can delete the event
    if event.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this event.")

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'delete_event.html', {'event': event})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Ensure that only the creator can update the event
    if event.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to update this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'update_event.html', {'form': form, 'event': event})


@login_required
def delete_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id)

    # Ensure that only the user who registered can delete the registration
    if registration.user != request.user:
        return HttpResponseForbidden("You are not allowed to cancel this registration.")

    if request.method == 'POST':
        event_name = registration.event.name
        user_email = registration.user.email
        registration.delete()

        # Send a cancellation email
        send_mail(
            subject=f'Your Registration for {event_name} has been Cancelled',
            message=f'Dear {request.user.username},\n\nYou have successfully cancelled your registration for the event "{event_name}".\n\nWe hope to see you at future events!\n\nBest regards,\nEvent Management Team',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        messages.success(request, 'Your registration has been cancelled and you have been notified via email.')
        return redirect('my_registrations')
    
    return render(request, 'delete_registration.html', {'registration': registration})


@login_required
def my_events(request):
    events = Event.objects.filter(created_by=request.user)
    return render(request, 'my_events.html', {'events': events})


@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')
    
@login_required
def view_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)
    return render(request, 'view_registrations.html', {'event': event, 'registrations': registrations})