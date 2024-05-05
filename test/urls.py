from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path(
        "favorite",
        LandMarkFavoriteList.as_view(),
        name="LandMarkFavoriteList",
    ),
    path(
        "LandMarkList/",
        LandMarkList.as_view(),
        name="LandMarkList",
    ),
    path(
        "LandMarkSearch/",
        LandMarkSearch.as_view(),
        name="LandMarkSearch"
    ),
    path(
        "LandMarkAtPos/",
        LandMarkAtPos.as_view(),
        name="LandMarkAtPos",
    ),
    path(
        "LandMarkDetail/",
        LandMarkDetail.as_view(),
        name="LandMarkDetail",
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
    path(
        "search-histories/",
        SearchHistoryList.as_view(),
        name="search_histories",
    )
]
