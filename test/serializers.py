from rest_framework import serializers
from .models import *


class SeoulMunicipalArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulMunicipalArtMuseum
        fields = "__all__"


class SeoulisArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulisArtMuseum
        fields = ["id", "GA_KNAME", "GA_INS_DATE", "GA_ADDR1", "GA_ADDR2", "GA_DETAIL"]
