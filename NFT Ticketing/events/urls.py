from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="events_home"),
    path("create-event/", views.create_event, name="create_Event"),
    path("deploy-event/", views.deploy_event, name="deploy_Event"),
    path("your-events/", views.your_events, name="your_Event"),
    path("event-page/", views.event_page, name="event_page"),
    path("your-tickets/", views.your_tickets, name="your_tickets"),
    path("ticket-page/", views.ticket_page, name="ticket_page"),
    path("about/", views.about, name="about")    
]
