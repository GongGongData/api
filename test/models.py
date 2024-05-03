from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.
class SeoulMunicipalArtMuseum(models.Model):
    DP_EX_NO = models.IntegerField()
    DP_SEQ = models.IntegerField()
    DP_NAME = models.CharField(max_length=1000)
    DP_SUBNAME = models.CharField(max_length=1000, blank=True)
    DP_PLACE = models.CharField(max_length=1000)
    DP_START = models.DateField()
    DP_END = models.DateField()
    DP_HOMEPAGE = models.URLField(blank=True)
    DP_EVENT = models.CharField(max_length=1000, blank=True)
    DP_SPONSOR = models.CharField(max_length=1000)
    DP_VIEWTIME = models.CharField(max_length=1000, blank=True)
    DP_VIEWCHARGE = models.CharField(max_length=1000, blank=True)
    DP_ART_PART = models.TextField()
    DP_ART_CNT = models.CharField(max_length=1000)
    DP_ARTIST = models.CharField(max_length=1000)
    DP_VIEWPOINT = models.TextField(blank=True)
    DP_INFO = models.TextField()
    DP_MAIN_IMG = models.URLField()
    DP_LNK = models.URLField()
    DP_DATE = models.DateField()

    @staticmethod
    def of(json_data, clean_text):
        return SeoulMunicipalArtMuseum(
            DP_EX_NO=json_data.get("DP_EX_NO", ""),
            DP_SEQ=json_data.get("DP_SEQ", ""),
            DP_NAME=json_data.get("DP_NAME", ""),
            DP_SUBNAME=json_data.get("DP_SUBNAME", ""),
            DP_PLACE=json_data.get("DP_PLACE", ""),
            DP_START=json_data.get("DP_START", ""),
            DP_END=json_data.get("DP_END", ""),
            DP_HOMEPAGE=json_data.get("DP_HOMEPAGE", ""),
            DP_EVENT=json_data.get("DP_EVENT", ""),
            DP_SPONSOR=json_data.get("DP_SPONSOR", ""),
            DP_VIEWTIME=json_data.get("DP_VIEWTIME", ""),
            DP_VIEWCHARGE=json_data.get("DP_VIEWCHARGE", ""),
            DP_ART_PART=json_data.get("DP_ART_PART", ""),
            DP_ART_CNT=json_data.get("DP_ART_CNT", ""),
            DP_ARTIST=json_data.get("DP_ARTIST", ""),
            DP_VIEWPOINT=json_data.get("DP_VIEWPOINT", ""),
            DP_INFO=clean_text,
            DP_MAIN_IMG=json_data.get("DP_MAIN_IMG", ""),
            DP_LNK=json_data.get("DP_LNK", ""),
            DP_DATE=json_data.get("DP_DATE", ""),
        )

    def __str__(self):
        return self.DP_NAME


class SeoulisArtMuseum(models.Model):
    GA_KNAME = models.CharField(max_length=300)
    GA_INS_DATE = models.CharField(max_length=300)
    CODE_N1_NAME = models.CharField(max_length=1000)
    CODE_N2_NAME = models.CharField(max_length=1000)
    CODE_N3_NAME = models.CharField(max_length=1000)
    GA_ADDR1 = models.CharField(max_length=1000)
    GA_ADDR2 = models.CharField(max_length=1000, blank=True)
    GA_DETAIL = models.TextField()
    CODE_A1 = models.CharField(max_length=1000, blank=True)

    @staticmethod
    def of(json_data):
        return SeoulisArtMuseum(
            GA_KNAME=json_data.get("GA_KNAME"),
            GA_INS_DATE=json_data.get("GA_INS_DATE"),
            CODE_N1_NAME=json_data.get("CODE_N1_NAME"),
            CODE_N2_NAME=json_data.get("CODE_N2_NAME"),
            CODE_N3_NAME=json_data.get("CODE_N3_NAME"),
            GA_ADDR1=json_data.get("GA_ADDR1"),
            GA_ADDR2=json_data.get("GA_ADDR2"),
            GA_DETAIL=json_data.get("GA_DETAIL"),
            CODE_A1=json_data.get("CODE_A1"),
        )

    def __str__(self):
        return self.GA_KNAME


class LandmarkType(Enum):
    MUSEUM = "서울은미술관"
    SPACE = "문화공간"
    EVENT = "문화행사"


class LandMark(models.Model):
    REF_ID = models.CharField(max_length=300)
    ADDR = models.CharField(max_length=500)
    NAME = models.CharField(max_length=500)
    X_COORD = models.FloatField(default=0.0, null=True)
    Y_COORD = models.FloatField(default=0.0, null=True)
    TYPE = models.CharField(max_length=300)
    TITLE = models.CharField(max_length=300, default="")
    IMG = models.URLField(default="")
    SUBJECT = models.CharField(max_length=300, default="")
    startDate = models.CharField(max_length=500, null=True)
    endDate = models.CharField(max_length=500, null=True)

    @staticmethod
    def Q_search(search_word):
        return (
            Q(ADDR__icontains=search_word)
            | Q(NAME__icontains=search_word)
            | Q(TITLE__icontains=search_word)
            | Q(SUBJECT__icontains=search_word)
        )

    def __str__(self):
        return self.NAME


class CultureEvent(models.Model):
    REF_ID = models.CharField(max_length=300, default="")
    CODENAME = models.CharField(max_length=300)
    GUNAME = models.CharField(max_length=300)
    TITLE = models.CharField(max_length=300)
    DATE = models.CharField(max_length=300)
    PLACE = models.CharField(max_length=300)
    ORG_NAME = models.CharField(max_length=300)
    USE_TRGT = models.CharField(max_length=300)
    USE_FEE = models.TextField()
    PLAYER = models.TextField()
    PROGRAM = models.TextField()
    ETC_DESC = models.TextField()
    ORG_LINK = models.CharField(max_length=1500, default="")
    MAIN_IMG = models.URLField(default="")
    RGSTDATE = models.CharField(max_length=300)
    TICKET = models.CharField(max_length=300)
    STRTDATE = models.CharField(max_length=300)
    END_DATE = models.CharField(max_length=300)
    THEMECODE = models.CharField(max_length=300)
    LOT = models.FloatField(default=0.0, null=True)
    LAT = models.FloatField(default=0.0, null=True)
    IS_FREE = models.CharField(max_length=300)
    HMPG_ADDR = models.URLField(default="")

    def __str__(self):
        return self.TITLE


class LandmarkFavorite(models.Model):
    LANDMARK = models.ForeignKey(LandMark, on_delete=models.CASCADE, related_name="favorites")
    USER = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    CREATED_AT = models.DateTimeField(auto_now_add=True)
