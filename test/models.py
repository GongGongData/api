from django.db import models


# Create your models here.
class SeoulMunicipalArtMuseum(models.Model):
    DP_EX_NO = models.CharField(max_length=10)
    DP_SEQ = models.CharField(max_length=10)
    DP_NAME = models.CharField(max_length=255)
    DP_SUBNAME = models.CharField(max_length=255, blank=True)
    DP_PLACE = models.CharField(max_length=255)
    DP_START = models.DateField()
    DP_END = models.DateField()
    DP_HOMEPAGE = models.URLField(blank=True)
    DP_EVENT = models.CharField(max_length=255, blank=True)
    DP_SPONSOR = models.CharField(max_length=255)
    DP_VIEWTIME = models.CharField(max_length=255, blank=True)
    DP_VIEWCHARGE = models.CharField(max_length=255, blank=True)
    DP_ART_PART = models.TextField()
    DP_ART_CNT = models.CharField(max_length=20)
    DP_ARTIST = models.CharField(max_length=1000)
    DP_VIEWPOINT = models.TextField(blank=True)
    DP_INFO = models.TextField()
    DP_MAIN_IMG = models.URLField()
    DP_LNK = models.URLField()
    DP_DATE = models.DateField()

    def __str__(self):
        return self.DP_NAME
