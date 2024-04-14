from django.shortcuts import render
from django.http import JsonResponse
from gonggongapp.settings import API_KEY
from .models import *

# Create your views here.
import requests
from bs4 import BeautifulSoup
from .models import SeoulMunicipalArtMuseum


def test1(request):
    api_key = API_KEY
    api_url = SeoulMunicipalArtMuseum.get_api_url(api_key, 1, 1000)
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        # 데이터를 모델에 저장
        exhibitions = data.get("ListExhibitionOfSeoulMOAInfo", {}).get("row", [])
        for exhibition_data in exhibitions:
            # 중복 데이터 확인
            if not SeoulMunicipalArtMuseum.objects.filter(
                DP_EX_NO=exhibition_data.get("DP_EX_NO", "")
            ).exists():
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


# 서울은미술관 현황
def test2(request):
    api_key = API_KEY
    api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/ListExhibitionOfSeoulMOAInfo/1/20"
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)


# 서울시립미술관 교육 정보 (교육 프로그램, 교육 기간 대략 1 달 정도)
def test3(request):
    api_key = ""
    api_url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/ListEducationOfSeoulMOAInfo/1/5/"
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({"error_message": error_message}, status=500)
