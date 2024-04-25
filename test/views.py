import googlemaps, requests
from django.shortcuts import render
from django.http import JsonResponse
from gonggongapp.settings import SEOUL_API_KEY, GOOGLE_API_KEY
from bs4 import BeautifulSoup

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

# Create your views here.

from .serializers import *
from .models import *


# 서울시립미술관 전시 정보 (국문)
def GetSeoulMunicipalArtMuseum(request):
    api_key = SEOUL_API_KEY
    api_url = SeoulMunicipalArtMuseum.get_api_url(api_key, 1, 1000)
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # 데이터를 모델에 저장
        exhibitions = data.get("ListExhibitionOfSeoulMOAInfo", {}).get("row", [])
        for exhibition_data in exhibitions:
            # 중복 데이터 확인
            if not SeoulMunicipalArtMuseum.objects.filter(DP_EX_NO=exhibition_data.get("DP_EX_NO", "")).exists():
                # HTML 태그를 제거하여 텍스트 정리
                dp_info = exhibition_data.get("DP_INFO", "")
                soup = BeautifulSoup(dp_info, "html.parser")
                clean_text = soup.get_text()

                # SeoulMunicipalArtMuseum 모델의 각 필드에 맞게 데이터를 추출하여 모델 인스턴스 생성 및 저장
                exhibition = SeoulMunicipalArtMuseum.of(exhibition_data, clean_text)
                exhibition.save()
        return JsonResponse({"message": "Exhibitions saved successfully."})
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)


def geocode_test(request):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    result = []
    # all = SeoulMunicipalArtMuseum.objects.all()
    # for elem in all:
    #     result.append(elem.get("DP_PLACE"))
    first = SeoulMunicipalArtMuseum.objects.first()
    geocode_result = gmaps.geocode(first.DP_PLACE, region="kr", language="ko")
    return JsonResponse({"place": first.DP_PLACE, "result": geocode_result}, status=200)


# 서울은 미술관 현황
def test2(request):
    api_key = SEOUL_API_KEY
    api_url = SeoulisArtMuseum.get_api_url(api_key, 1, 1)
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        exhibitions = data.get("tvGonggongArt", {}).get("row", [])
        for exhibition_data in exhibitions:
            # 중복 데이터 확인
            if not SeoulisArtMuseum.objects.filter(GA_KNAME=exhibition_data.get("GA_KNAME", "")).exists():
                exhibition = SeoulisArtMuseum.of(exhibition_data)
                exhibition.save()
        return JsonResponse({"message": "SeoulisArtMuseum data saved successfully."})
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)


# 서울은미술관 Detail API
def test3(request):
    api_key = SEOUL_API_KEY
    api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalEventInfo/1/5/%20/오페라 갈라"

    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)


# 서울시 공영주차장
def test4(request):
    api_key = SEOUL_API_KEY
    api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/GetParkInfo/1/5/"
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)


def landmark(request):
    api_key = SEOUL_API_KEY
    # 서울은미술관
    museum_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tvGonggongArt/1/30/"
    museum_response = requests.get(museum_api_url)
    culture_place_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalSpaceInfo/1/1000/"
    culture_place_response = requests.get(culture_place_api_url)

    if museum_response.status_code == 200 and culture_place_response.status_code == 200:
        if museum_response.status_code == 200:
            data = museum_response.json()
            # 데이터를 모델에 저장
            landmarks = data.get("tvGonggongArt", {}).get("row", [])
            for landmark in landmarks:
                # 중복 데이터 확인
                if not LandMark.objects.filter(NAME=landmark.get("GA_KNAME", "")).exists():
                    LandMark.objects.create(
                        REF_ID=landmark.get("GA_KNAME").replace(" ", "_"),
                        ADDR=landmark.get("GA_ADDR1") + " " + landmark.get("GA_ADDR2"),
                        NAME=landmark.get("GA_KNAME"),
                        X_COORD=40.7128,  # 예시 위도
                        Y_COORD=-74.0060,  # 예시 경도
                        TYPE="서울은미술관",
                        startDate=None,
                        endDate=None,
                    )

        if culture_place_response.status_code == 200:
            data = culture_place_response.json()
            # 데이터를 모델에 저장
            landmarks = data.get("culturalSpaceInfo", {}).get("row", [])
            for landmark in landmarks:
                # 중복 데이터 확인
                if not LandMark.objects.filter(REF_ID=landmark.get("NUM", "")).exists():
                    x_coord = landmark.get("X_COORD")
                    y_coord = landmark.get("Y_COORD")
                    if x_coord:
                        x_coord_float = float(x_coord)
                    else:
                        x_coord_float = 12.23312  # 임시 위도 -> geocode변환 필요
                    if y_coord:
                        y_coord_float = float(y_coord)
                    else:
                        y_coord_float = 12.23312  # 임시 경도 -> geocode변환 필요

                    LandMark.objects.create(
                        REF_ID=landmark.get("NUM"),
                        ADDR=landmark.get("ADDR"),
                        NAME=landmark.get("FAC_NAME"),
                        X_COORD=x_coord_float,  # 예시 위도
                        Y_COORD=y_coord_float,  # 예시 경도
                        TYPE="문화공간",
                        startDate=None,
                        endDate=None,
                    )
        return JsonResponse({"message": "Landmarks saved successfully."})
    else:
        error_message = f"Failed to fetch data."
        return JsonResponse({"error_message": error_message}, status=500)


class SeoulMunicipalArtMuseumList(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request):
        info_list = SeoulMunicipalArtMuseum.objects.all()
        serializer = SeoulMunicipalArtMuseumSerializer(info_list, many=True)
        return Response(serializer.data)


class SeoulMunicipalArtMuseumDetail(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, pk):
        try:
            detail_info = SeoulMunicipalArtMuseum.objects.get(id=pk)
            serializer = SeoulMunicipalArtMuseumDetailSerializer(detail_info)
            return Response(serializer.data)
        except SeoulMunicipalArtMuseum.DoesNotExist:
            return Response({"message": "Info does not found"}, status=404)


class SeoulisArtMuseumList(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request):
        info_list = SeoulisArtMuseum.objects.all()
        serializer = SeoulisArtMuseumSerializer(info_list, many=True)
        return Response(serializer.data)


class SeoulisArtMuseumDetail(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, pk):
        try:
            detail_info = SeoulisArtMuseum.objects.get(id=pk)
            serializer = SeoulisArtMuseumDetailSerializer(detail_info)
            return Response(serializer.data)
        except SeoulisArtMuseum.DoesNotExist:
            return Response({"message": "Info does not found"}, status=404)
