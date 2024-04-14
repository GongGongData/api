from rest_framework import serializers
from .models import *


class SeoulMunicipalArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulMunicipalArtMuseum
        fields = ["DP_EX_NO", "DP_NAME", "DP_INFO"]
