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
        fields = ["REF_ID", "X_COORD", "Y_COORD", "ADDR", "NAME", "TYPE"]
