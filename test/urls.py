from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from . import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GongGong Data API",
        default_version="v1",
        description="공공데이터를 프론트와 통신하기위한 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(name="nooreong", email="nooreong@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("test1", views.GetSeoulMunicipalArtMuseum),
    path("test2", views.test2),
    path("test3", views.test3),
    path("test4", views.test4),
    path("geocode", views.geocode_test),
    path(
        "SeoulMunicipalArtMuseumList/",
        SeoulMunicipalArtMuseumList.as_view(),
        name="seoul_municipal_art_museum_list",
    ),
    path(
        "SeoulisArtMuseumList/",
        SeoulisArtMuseumList.as_view(),
        name="seoul_is_art_museum_list",
    ),
]
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
