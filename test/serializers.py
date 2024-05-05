from rest_framework import serializers
from .models import *


class SeoulMunicipalArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulMunicipalArtMuseum
        fields = [
            "id",
            "DP_EX_NO",
            "DP_NAME",
            "DP_SUBNAME",
            "DP_PLACE",
            "DP_START",
            "DP_END",
            "DP_MAIN_IMG",
        ]


class SeoulMunicipalArtMuseumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulMunicipalArtMuseum
        exclude = ["DP_SPONSOR"]


class SeoulisArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulisArtMuseum
        fields = ["id", "GA_KNAME", "GA_ADDR1", "GA_ADDR2"]


class SeoulisArtMuseumDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulisArtMuseum
        fields = ["id", "GA_KNAME", "GA_INS_DATE", "GA_ADDR1", "GA_ADDR2", "GA_DETAIL"]


class LandMarkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandMark
        # fields = "__all__"
        exclude = ["startDate", "endDate"]


class LandMarkFavoriteListSerializer(serializers.ModelSerializer):
    LANDMARK = LandMarkListSerializer(many=False, read_only=True)
    USER = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = LandmarkFavorite
        fields = ["LANDMARK", "USER", "CREATED_AT"]


class LandMarkFavoritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandmarkFavorite
        fields = ["LANDMARK"]


class CultureEventDetail(serializers.ModelSerializer):
    class Meta:
        model = CultureEvent
        fields = "__all__"


class SearchHistorySerializer(serializers.ModelSerializer):
    LANDMARK = LandMarkListSerializer(many=False, read_only=True)

    class Meta:
        model = SearchHistory
        fields = ["LANDMARK", "CREATED_AT", "LAST_SEARCHED_AT"]
