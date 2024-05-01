import googlemaps
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from gonggongapp.settings import GOOGLE_API_KEY
from .gonggong_api import GonggongApi

from .models import *
from .serializers import *


# Create your views here.


# 서울시립미술관 전시 정보 (국문)
def GetSeoulMunicipalArtMuseum(request):
    api_url = GonggongApi.museum_list_url(1, 1000)
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
def make_museum_test(request):
    api_url = GonggongApi.museum_list_url(1, 30)
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


def make_event_test(request):
    all_success = True

    event_page_size = 1000
    event_total_pages = 5

    for page in range(1, event_total_pages + 1):
        start_index = (page - 1) * event_page_size + 1
        end_index = page * event_page_size

        culture_event_api_url = GonggongApi.event_list_url(start_index, end_index)
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
    error_messages = []

    museum_api_url = GonggongApi.museum_list_url()
    museum_response = requests.get(museum_api_url)

    ##### 서울은미술관 #####
    if museum_response.status_code != 200:
        error_messages.append("Failed to fetch seoul is museum data.")
    else:
        data = museum_response.json()
        # 데이터를 모델에 저장
        museums = data.get("tvGonggongArt", {}).get("row", [])
        for museum in museums:
            ref_id = museum.get("GA_KNAME", "")
            # 중복 데이터 확인
            if not LandMark.objects.filter(NAME=ref_id).exists():
                coords = get_geocode(museum.get("GA_ADDR1"))
                LandMark.objects.create(
                    REF_ID=ref_id,
                    ADDR=museum.get("GA_ADDR1") + " " + museum.get("GA_ADDR2"),
                    NAME=museum.get("GA_KNAME"),
                    X_COORD=coords[0],
                    Y_COORD=coords[1],
                    TYPE=LandmarkType.MUSEUM.value,
                    TITLE=museum.get("GA_ADDR2", ""),
                    IMG="",
                    SUBJECT="미술품",
                    startDate=None,
                    endDate=None,
                )

    ##### 문화공간 #####
    culture_place_api_url = GonggongApi.space_list_url()
    culture_place_response = requests.get(culture_place_api_url)

    if culture_place_response.status_code != 200:
        error_messages.append("Failed to fetch culture place data.")
    else:
        data = culture_place_response.json()
        spaces = data.get("culturalSpaceInfo", {}).get("row", [])
        for space in spaces:
            ref_id = space.get("NUM", "")

            # 중복 데이터 확인
            if not LandMark.objects.filter(REF_ID=ref_id).exists():
                x_coord = space.get("X_COORD")
                y_coord = space.get("Y_COORD")
                if x_coord and y_coord:
                    x_coord_float = float(x_coord)
                    y_coord_float = float(y_coord)
                else:
                    coords = get_geocode(space.get("ADDR"))
                    x_coord_float = coords[0]
                    y_coord_float = coords[1]

                LandMark.objects.create(
                    REF_ID=ref_id,
                    ADDR=space.get("ADDR"),
                    NAME=space.get("FAC_NAME"),
                    X_COORD=x_coord_float,
                    Y_COORD=y_coord_float,
                    TYPE=LandmarkType.SPACE.value,
                    TITLE=space.get("FAC_NAME", ""),
                    IMG=space.get("MAIN_IMG", ""),
                    SUBJECT=space.get("SUBJCODE", ""),
                    startDate=None,
                    endDate=None,
                )

    ##### 문화행사 #####
    page_size = 1000

    response_for_count = requests.get(GonggongApi.event_list_url(1, 5))
    total_count = response_for_count.json().get("culturalEventInfo", {}).get("list_total_count", [])

    for start_index in range(1, total_count, page_size):
        end_index = start_index + page_size - 1

        culture_event_api_url = GonggongApi.event_list_url(start_index, end_index)
        culture_event_response = requests.get(culture_event_api_url)

        if culture_event_response.status_code != 200:
            error_messages.append(f"Failed to fetch culture event data[{start_index}:{end_index}].")
        else:
            data = culture_event_response.json()
            events = data.get("culturalEventInfo", {}).get("row", [])
            for event in events:
                ref_id = event.get("TITLE")
                # 중복 데이터 확인
                if not LandMark.objects.filter(REF_ID=ref_id).exists():
                    x_coord = event.get("LOT")
                    y_coord = event.get("LAT")

                    if "°" in x_coord or x_coord == "" or "°" in y_coord or y_coord == "":
                        coords = get_geocode(event.get("ORG_NAME"))

                        x_coord_float = coords[0]
                        y_coord_float = coords[1]
                    else:
                        x_coord_float = float(x_coord)
                        y_coord_float = float(y_coord)

                    LandMark.objects.create(
                        REF_ID=ref_id,
                        ADDR=event.get("GUNAME", "") + " " + event.get("PLACE", ""),
                        NAME=event.get("TITLE"),
                        X_COORD=x_coord_float,
                        Y_COORD=y_coord_float,
                        TYPE=LandmarkType.EVENT.value,
                        TITLE=event.get("PLACE", ""),
                        IMG=event.get("MAIN_IMG", ""),
                        SUBJECT=event.get("CODENAME", ""),
                        startDate=event.get("STRTDATE"),
                        endDate=event.get("END_DATE"),
                    )

    return JsonResponse({
        "message": "Data saved successfully.",
        "error_messages": error_messages
    })


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

        landmarks_at_pos = LandMark.objects.filter(X_COORD=x_coord, Y_COORD=y_coord)

        space = landmarks_at_pos.filter(TYPE=LandmarkType.SPACE.value).first()
        art_n_museum = landmarks_at_pos.filter(TYPE__in=[LandmarkType.MUSEUM.value, LandmarkType.EVENT.value])

        return JsonResponse({
            "SPACE": LandMarkListSerializer(space, many=False).data if space else None,
            "LIST": LandMarkListSerializer(art_n_museum, many=True).data,
        })


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

        if ref_id is None or type is None:
            # ref_id type 주어지지 않은 경우 에러 응답 반환
            return Response({"error": "ref_id and type parameters are required"}, status=400)
        # 서울은미술관
        if type == LandmarkType.MUSEUM.value:

            museum_api_url = GonggongApi.museum_detail_url(ref_id)
            museum_response = requests.get(museum_api_url)
            if museum_response.status_code == 200:
                museum_data = museum_response.json()["tvGonggongArt"]["row"][0]
                return Response(museum_data)
        # 문화공간
        if type == LandmarkType.SPACE.value:
            space_api_url = GonggongApi.space_detail_url(ref_id)
            space_response = requests.get(space_api_url)
            if space_response.status_code == 200:
                culture_space_data = space_response.json()["culturalSpaceInfo"]["row"][0]
                return Response(culture_space_data)
        # 문화행사
        if type == LandmarkType.EVENT.value:
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
