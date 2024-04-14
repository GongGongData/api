from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('test1', views.test1),
    path('test2', views.test2),
    path('test3', views.test3),
    path('geocode', views.geocode_test),
]
