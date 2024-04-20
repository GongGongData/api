from rest_framework import serializers
from .models import *


class SeoulMunicipalArtMuseumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeoulMunicipalArtMuseum
        fields = "__all__"
