from gonggongapp.settings import SEOUL_API_KEY


class GonggongApi:
    @staticmethod
    def museum_detail_url(ref_id):
        return f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/tvGonggongArt/1/1/{ref_id.replace(' ', '_')}"

    @staticmethod
    def space_detail_url(ref_id):
        return f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/culturalSpaceInfo/1/1/{ref_id}"

    @staticmethod
    def museum_list_url(start_index=1, end_index=30):
        return f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/tvGonggongArt/{start_index}/{end_index}/"

    @staticmethod
    def space_list_url(start_index=1, end_index=1000):
        return f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/culturalSpaceInfo/{start_index}/{end_index}/"

    @staticmethod
    def event_list_url(start_index=1, end_index=1000):
        return f"http://openapi.seoul.go.kr:8088/{SEOUL_API_KEY}/json/culturalEventInfo/{start_index}/{end_index}/"
