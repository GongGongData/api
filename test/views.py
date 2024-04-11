from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
import requests
# 서울시립미술관 전시정보
def test1(request):
    api_key = ''
    api_url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/ListExhibitionOfSeoulMOAInfo/1/10/'
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({'error_message': error_message}, status=500)
# 서울시립미술관 교육 정보 (교육 프로그램, 교육 기간 대략 1 달 정도)
def test2(request):
    api_key = ''
    api_url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/tvGonggongArt/1/5/'
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({'error_message': error_message}, status=500)

# 서울은 미술관 현황
def test3(request):
    api_key = ''
    api_url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/ListEducationOfSeoulMOAInfo/1/5/'
    response = requests.get(api_url)

    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        error_message = f"Failed to fetch data. Status code: {response.status_code}"
        return JsonResponse({'error_message': error_message}, status=500)