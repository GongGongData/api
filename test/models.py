from django.db import models


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
    def get_api_url(api_key: str, start_index=1, end_index=20):
        return f"http://openapi.seoul.go.kr:8088/{api_key}/json/ListExhibitionOfSeoulMOAInfo/{start_index}/{end_index}/"

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
    def get_api_url(api_key: str, start_index=1, end_index=30):
        return f"http://openapi.seoul.go.kr:8088/{api_key}/json/tvGonggongArt/{start_index}/{end_index}/"

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

    def __str__(self):
        return self.NAME
