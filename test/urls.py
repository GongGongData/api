from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("test1", views.test1),
    path("test2", views.test2),
    path("test3", views.test3),
    path("test4", views.test4),
    path("geocode", views.geocode_test),
    path(
        "test5/",
        SeoulMunicipalArtMuseumList.as_view(),
        name="seoul_municipal_art_museum_list",
    ),
]
