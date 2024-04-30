import json

import googlemaps, requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from gonggongapp.settings import SEOUL_API_KEY, GOOGLE_API_KEY
from bs4 import BeautifulSoup
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.schemas import ManualSchema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    api_url = SeoulisArtMuseum.get_api_url(api_key, 1, 30)
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
    api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalEventInfo/1/5/%20/창작뮤지컬/2023"

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


def cultureEvent(request):
    all_success = True
    api_key = SEOUL_API_KEY
    culture_event_api_url_base = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalEventInfo/"

    event_page_size = 1000
    event_total_pages = 5

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
                ref_id = landmark.get("TITLE")
                if not CultureEvent.objects.filter(REF_ID=ref_id).exists():
                    x_coord = landmark.get("LOT")
                    y_coord = landmark.get("LAT")

                    if "°" in x_coord or x_coord == "" or "°" in y_coord or y_coord == "":
                        coords = get_geocode(landmark.get("ORG_NAME"))

                        x_coord_float = coords[0]
                        y_coord_float = coords[1]
                    else:
                        x_coord_float = float(x_coord)
                        y_coord_float = float(y_coord)

                    CultureEvent.objects.create(
                        REF_ID=ref_id,
                        CODENAME=landmark.get("CODENAME", ""),
                        GUNAME=landmark.get("GUNAME", ""),
                        TITLE=landmark.get("TITLE", ""),
                        DATE=landmark.get("DATE", ""),
                        PLACE=landmark.get("PLACE", ""),
                        ORG_NAME=landmark.get("ORG_NAME", ""),
                        USE_TRGT=landmark.get("USE_TRGT", ""),
                        USE_FEE=landmark.get("USE_FEE", ""),
                        PLAYER=landmark.get("PLAYER", ""),
                        PROGRAM=landmark.get("PROGRAM", ""),
                        ETC_DESC=landmark.get("ETC_DESC", ""),
                        ORG_LINK=landmark.get("ORG_LINK", ""),
                        MAIN_IMG=landmark.get("MAIN_IMG", ""),
                        RGSTDATE=landmark.get("RGSTDATE", ""),
                        TICKET=landmark.get("TICKET", ""),
                        STRTDATE=landmark.get("STRTDATE", ""),
                        END_DATE=landmark.get("END_DATE", ""),
                        THEMECODE=landmark.get("THEMECODE", ""),
                        LOT=x_coord_float,
                        LAT=y_coord_float,
                        IS_FREE=landmark.get("IS_FREE", ""),
                        HMPG_ADDR=landmark.get("HMPG_ADDR", ""),
                    )
                pass
        else:
            all_success = False
            error_message = f"Failed to fetch culture event data."
            return JsonResponse({"error_message": error_message}, status=500)
    if all_success:
        return JsonResponse({"message": "All data saved successfully."})


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
                    TITLE=landmark.get("GA_ADDR2", ""),
                    IMG="",
                    SUBJECT="미술품",
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
                    TITLE=landmark.get("FAC_NAME", ""),
                    IMG=landmark.get("MAIN_IMG", ""),
                    SUBJECT=landmark.get("SUBJCODE", ""),
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
                ref_id = landmark.get("TITLE")
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
                        ADDR=landmark.get("GUNAME", "") + " " + landmark.get("PLACE", ""),
                        NAME=landmark.get("TITLE"),
                        X_COORD=x_coord_float,
                        Y_COORD=y_coord_float,
                        TYPE="문화행사",
                        TITLE=landmark.get("PLACE", ""),
                        IMG=landmark.get("MAIN_IMG", ""),
                        SUBJECT=landmark.get("CODENAME", ""),
                        startDate=landmark.get("STRTDATE"),
                        endDate=landmark.get("END_DATE"),
                    )
        else:
            all_success = False
            error_message = f"Failed to fetch culture event data."
            return JsonResponse({"error_message": error_message}, status=500)

    if all_success:
        return JsonResponse({"message": "All data saved successfully."})


class LandMarkList(APIView):
    @swagger_auto_schema(
        operation_summary="전체 랜드마크 위도 경도 반환(중복제거 수행)",
    )
    def get(self, requets):
        # 데이터베이스로부터 중복을 제거한 좌표 쌍 가져오기
        unique_coordinates = LandMark.objects.values_list("X_COORD", "Y_COORD").distinct()

        # 중복을 제거한 객체들을 담을 리스트 생성
        unique_landmarks = []

        # 중복을 제거한 좌표 쌍을 기반으로 객체들 가져오기
        for x_coord, y_coord in unique_coordinates:
            landmark = LandMark.objects.filter(X_COORD=x_coord, Y_COORD=y_coord).first()
            if landmark:
                unique_landmarks.append(landmark)

        # Serializer를 사용하여 객체들을 직렬화
        serializer = LandMarkListSerializer(unique_landmarks, many=True)
        return Response(serializer.data)


class LandMarkAtPos(APIView):
    @swagger_auto_schema(
        operation_summary="위도 경도 기반으로 데이터 로드",
        manual_parameters=[
            openapi.Parameter("X_COORD", openapi.IN_QUERY, description="X coordinate", type=openapi.TYPE_NUMBER),
            openapi.Parameter("Y_COORD", openapi.IN_QUERY, description="Y coordinate", type=openapi.TYPE_NUMBER),
        ],
    )
    def get(self, request):
        # 요청으로부터 X_COORD와 Y_COORD 값을 가져오기
        x_coord = request.query_params.get("X_COORD", None)
        y_coord = request.query_params.get("Y_COORD", None)

        if x_coord is None or y_coord is None:
            # X_COORD나 Y_COORD가 주어지지 않은 경우 에러 응답 반환
            return Response({"error": "X_COORD and Y_COORD parameters are required"}, status=400)

        # 데이터베이스에서 해당하는 좌표에 해당하는 객체들을 가져오기
        landmarks = LandMark.objects.filter(X_COORD=x_coord, Y_COORD=y_coord)
        # 문화공간인 경우만 필터링
        cultural_landmarks = landmarks.filter(TYPE="문화공간")
        data = []
        if cultural_landmarks:
            for landmark in cultural_landmarks:
                # 해당 문화공간의 이벤트 가져오기
                events = CultureEvent.objects.filter(LOT=x_coord, LAT=y_coord)
                museums = landmarks.filter(TYPE="서울은미술관")
                space_data = {
                    "id": landmark.id,
                    "REF_ID": landmark.REF_ID,
                    "ADDR": landmark.ADDR,
                    "NAME": landmark.NAME,
                    "X_COORD": landmark.X_COORD,
                    "Y_COORD": landmark.Y_COORD,
                    "TYPE": landmark.TYPE,
                    "TITLE": landmark.TITLE,
                    "IMG": landmark.IMG,
                    "SUBJECT": landmark.SUBJECT,
                }
                data.append(space_data)
                if events:
                    event_data = {
                        "EVENTS": [
                            {
                                "REF_ID": event.REF_ID,
                                "ADDR": event.PLACE,
                                "NAME": event.TITLE,
                                "X_COORD": event.LOT,
                                "Y_COORD": event.LAT,
                                "TYPE": "문화행사",
                                "IMG": event.MAIN_IMG,
                                "SUBJECT": event.CODENAME,
                                "startDate": event.STRTDATE,
                                "endDate": event.END_DATE,
                            }
                            for event in events
                        ],
                    }
                    data.append(event_data)
                if museums:
                    museum_data = {
                        "MUSEUMS": [
                            {
                                "REF_ID": museum.REF_ID,
                                "ADDR": museum.PLACE,
                                "NAME": museum.TITLE,
                                "X_COORD": museum.LOT,
                                "Y_COORD": museum.LAT,
                                "TYPE": "서울은미술관",
                                "IMG": museum.MAIN_IMG,
                                "SUBJECT": museum.CODENAME,
                                "startDate": museum.STRTDATE,
                                "endDate": museum.END_DATE,
                            }
                            for museum in museums
                        ],
                    }
                    data.append(museum_data)
            return JsonResponse(data, safe=False)
        else:
            serializer = LandMarkListSerializer(landmarks, many=True)
            # 직렬화된 데이터 반환
            return Response(serializer.data)


class LandMarkDetail(APIView):
    @swagger_auto_schema(
        operation_summary="Detail 데이터 로드",
        manual_parameters=[
            openapi.Parameter("REF_ID", openapi.IN_QUERY, description="REF_ID", type=openapi.TYPE_STRING),
            openapi.Parameter("TYPE", openapi.IN_QUERY, description="TYPE", type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        ref_id = request.query_params.get("REF_ID", None)
        type = request.query_params.get("TYPE", None)

        api_key = SEOUL_API_KEY

        if ref_id is None or type is None:
            # ref_id type 주어지지 않은 경우 에러 응답 반환
            return Response({"error": "ref_id and type parameters are required"}, status=400)
        # 서울은미술관
        if ref_id and type == "서울은미술관":
            museum_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/tvGonggongArt/1/1/{ref_id}"
            museum_response = requests.get(museum_api_url)
            if museum_response.status_code == 200:
                museum_data = museum_response.json()["tvGonggongArt"]["row"][0]
                return Response(museum_data)
        # 문화공간
        if ref_id and type == "문화공간":
            culture_place_api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/culturalSpaceInfo/1/1/{ref_id}"
            culture_place_response = requests.get(culture_place_api_url)
            if culture_place_response.status_code == 200:
                culture_space_data = culture_place_response.json()["culturalSpaceInfo"]["row"][0]
                return Response(culture_space_data)
        # 문화행사
        if ref_id and type == "문화행사":
            data = CultureEvent.objects.get(REF_ID=ref_id)
            serializer = CultureEventDetail(data)
            return Response(serializer.data)


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


class LandMarkFavoriteList(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request):
        favorites = LandmarkFavorite.objects.filter(USER_id=request.user.id).select_related("LANDMARK")
        serializer = LandMarkFavoriteListSerializer(favorites, many=True)
        return Response({"message": "Favorites List for user", "favorites": serializer.data})

    ## blog에 엔트리가 여러개, 랜드마크에 즐찾이 여러개

    @csrf_exempt
    @swagger_auto_schema(
        operation_summary="즐겨찾기 등록",
        request_body=LandMarkFavoritePostSerializer,
        responses={201: LandMarkFavoriteListSerializer},
    )
    def post(self, request):
        lm_id = request.data["LANDMARK"]

        # 중복제거
        (LandmarkFavorite.objects.all().filter(LANDMARK_id=lm_id, USER_id=request.user.id).delete())

        # 생성
        landmark_favorite = LandmarkFavorite.objects.create(
            LANDMARK=LandMark.objects.get(pk=lm_id),
            USER=User(pk=request.user.id),
        )

        favorites = LandMarkFavoriteListSerializer(landmark_favorite, many=False).data
        return Response({"message": "Favorites List for user", "favorites": favorites})
