from django.urls import path

from . import views

urlpatterns = [
    path("museum-test", views.make_museum_test),
    path("culture-event", views.make_event_test),

    path("landmark", views.landmark),
]
