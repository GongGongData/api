import requests
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .gonggong_api import GonggongApi
from .serializers import *


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


class LandMarkSearch(APIView):
    @swagger_auto_schema(
        operation_summary="검색",
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, description="검색어", type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request):
        search_word = request.query_params.get("search")
        if not search_word:
            return JsonResponse({
                "message": "No Search Word",
            })

        landmarks = LandMark.objects.filter(LandMark.Q_search(search_word))

        return JsonResponse({
            "message": "OK",
            "data": LandMarkListSerializer(landmarks, many=True).data
        })


class LandMarkAtPos(APIView):
    @swagger_auto_schema(
        operation_summary="위도 경도 기반으로 데이터 로드",
        manual_parameters=[
            openapi.Parameter("X_COORD", openapi.IN_QUERY, description="X coordinate", type=openapi.TYPE_NUMBER),
            openapi.Parameter("Y_COORD", openapi.IN_QUERY, description="Y coordinate", type=openapi.TYPE_NUMBER),
            openapi.Parameter("search", openapi.IN_QUERY, description="Y coordinate", type=openapi.TYPE_NUMBER),
        ],
    )
    def get(self, request):
        # 요청으로부터 X_COORD와 Y_COORD 값을 가져오기
        x_coord = request.query_params.get("X_COORD", None)
        y_coord = request.query_params.get("Y_COORD", None)
        search_word = request.query_params.get("search", None)

        if x_coord is None or y_coord is None:
            # X_COORD나 Y_COORD가 주어지지 않은 경우 에러 응답 반환
            return Response({"error": "X_COORD and Y_COORD parameters are required"}, status=400)

        landmarks_at_pos = LandMark.objects.filter(X_COORD=x_coord, Y_COORD=y_coord)

        space = landmarks_at_pos.filter(TYPE=LandmarkType.SPACE.value).first()
        art_n_museum = landmarks_at_pos.filter(TYPE__in=[LandmarkType.MUSEUM.value, LandmarkType.EVENT.value])

        if search_word:
            art_n_museum.filter(LandMark.Q_search(search_word))

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
