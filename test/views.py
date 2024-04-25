import googlemaps, requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from gonggongapp.settings import SEOUL_API_KEY, GOOGLE_API_KEY
from bs4 import BeautifulSoup
from datetime import datetime

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


def get_geocode(address):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    geocode_result = gmaps.geocode(address, region="kr", language="ko")
    if geocode_result and len(geocode_result) > 0:
        location = geocode_result[0].get("geometry", {}).get("location", {})
        if location:
            lat = location.get("lat")
            lng = location.get("lng")
            return lat, lng
    return None, None


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
    # url import
    museum_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tvGonggongArt/1/30/"
    culture_place_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalSpaceInfo/1/1000/"

    event_page_size = 1000
    event_total_pages = 5
    culture_event_api_url_base = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalEventInfo/"

    museum_response = requests.get(museum_api_url)
    culture_place_response = requests.get(culture_place_api_url)

    all_success = True  # 모든 요청이 성공했는지 여부를 추적하는 플래그 변수

    # 서울은미술관
    if museum_response.status_code == 200:
        data = museum_response.json()
        # 데이터를 모델에 저장
        landmarks = data.get("tvGonggongArt", {}).get("row", [])
        for landmark in landmarks:
            # 중복 데이터 확인
            if not LandMark.objects.filter(NAME=landmark.get("GA_KNAME", "")).exists():
                coords = get_geocode(landmark.get("GA_ADDR1"))
                LandMark.objects.create(
                    REF_ID=landmark.get("GA_KNAME").replace(" ", "_"),
                    ADDR=landmark.get("GA_ADDR1") + " " + landmark.get("GA_ADDR2"),
                    NAME=landmark.get("GA_KNAME"),
                    X_COORD=coords[0],
                    Y_COORD=coords[1],
                    TYPE="서울은미술관",
                    startDate=None,
                    endDate=None,
                )
        pass
    else:
        all_success = False
        error_message = "Failed to fetch seoul is museum data."
        return JsonResponse({"error_message": error_message}, status=500)
        # 문화공간
    if culture_place_response.status_code == 200:
        data = culture_place_response.json()
        # 데이터를 모델에 저장
        landmarks = data.get("culturalSpaceInfo", {}).get("row", [])
        for landmark in landmarks:
            # 중복 데이터 확인
            if not LandMark.objects.filter(REF_ID=landmark.get("NUM", "")).exists():
                x_coord = landmark.get("X_COORD")
                y_coord = landmark.get("Y_COORD")
                if x_coord and y_coord:
                    x_coord_float = float(x_coord)
                    y_coord_float = float(y_coord)
                else:
                    coords = get_geocode(landmark.get("ADDR"))
                    x_coord_float = coords[0]
                    y_coord_float = coords[1]

                LandMark.objects.create(
                    REF_ID=landmark.get("NUM"),
                    ADDR=landmark.get("ADDR"),
                    NAME=landmark.get("FAC_NAME"),
                    X_COORD=x_coord_float,
                    Y_COORD=y_coord_float,
                    TYPE="문화공간",
                    startDate=None,
                    endDate=None,
                )
        pass
    else:
        all_success = False
        error_message = "Failed to fetch culture place data."
        return JsonResponse({"error_message": error_message}, status=500)
    # 문화행사
    for page in range(1, event_total_pages + 1):
        start_index = (page - 1) * event_page_size + 1
        end_index = page * event_page_size
        culture_event_api_url = culture_event_api_url_base + f"{start_index}/{end_index}/"
        culture_event_response = requests.get(culture_event_api_url)

        if culture_event_response.status_code == 200:
            data = culture_event_response.json()
            # 데이터를 모델에 저장
            landmarks = data.get("culturalEventInfo", {}).get("row", [])
            for landmark in landmarks:
                # 중복 데이터 확인
                ref_id = f"%20/{landmark.get('TITLE')}/{landmark.get('STARTDATE')}"
                if not LandMark.objects.filter(REF_ID=ref_id).exists():
                    x_coord = landmark.get("LOT")
                    y_coord = landmark.get("LAT")

                    if "°" in x_coord or x_coord == "" or "°" in y_coord or y_coord == "":
                        coords = get_geocode(landmark.get("ORG_NAME"))

                        x_coord_float = coords[0]
                        y_coord_float = coords[1]
                    else:
                        x_coord_float = float(x_coord)
                        y_coord_float = float(y_coord)

                    LandMark.objects.create(
                        REF_ID=ref_id,
                        ADDR=landmark.get("GUNAME") + " " + landmark.get("PLACE"),
                        NAME=landmark.get("TITLE"),
                        X_COORD=x_coord_float,
                        Y_COORD=y_coord_float,
                        TYPE="문화행사",
                        startDate=landmark.get("STARTDATE"),
                        endDate=landmark.get("END_DATE"),
                    )
        else:
            all_success = False
            error_message = f"Failed to fetch culture event data."
            return JsonResponse({"error_message": error_message}, status=500)

    if all_success:
        return JsonResponse({"message": "All data saved successfully."})


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
