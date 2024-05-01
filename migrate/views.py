import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render

from map.geocode import get_geocode
from test.gonggong_api import GonggongApi
from test.models import *


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


# Create your views here.
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
