from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from . import views
from .views import *

urlpatterns = [
    path("test1", views.GetSeoulMunicipalArtMuseum),
    path("test2", views.test2),
    path("test3", views.test3),
    path("test4", views.test4),
    path("landmark", views.landmark),
    path("geocode", views.geocode_test),
    path(
        "LandMarkList/",
        LandMarkList.as_view(),
        name="LandMarkList",
    ),
    path(
        "LandMarkAtPos/",
        LandMarkAtPos.as_view(),
        name="LandMarkAtPos",
    ),
    path(
        "SeoulMunicipalArtMuseumList/",
        SeoulMunicipalArtMuseumList.as_view(),
        name="seoul_municipal_art_museum",
    ),
    path(
        "SeoulMunicipalArtMuseumDetail<int:pk>/",
        SeoulMunicipalArtMuseumDetail.as_view(),
        name="seoul_municipal_art_museum_detail",
    ),
    path(
        "SeoulisArtMuseumList/",
        SeoulisArtMuseumList.as_view(),
        name="seoul_is_art_museum_list",
    ),
    path(
        "SeoulisArtMuseumDetail<int:pk>/",
        SeoulisArtMuseumDetail.as_view(),
        name="seoul_is_art_museum_detail",
    ),
]
