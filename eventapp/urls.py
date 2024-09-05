from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('create_event/', views.create_event, name='create_event'),
    path('event_list/', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
    path('event/<int:event_id>/update/', views.update_event, name='update_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('registration/<int:registration_id>/delete/', views.delete_registration, name='delete_registration'),
    path('my_events/', views.my_events, name='my_events'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('profile/delete/', views.delete_user, name='delete_user'),
    path('event/<int:event_id>/registrations/', views.view_registrations, name='view_registrations'),

]