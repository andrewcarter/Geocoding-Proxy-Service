import logging
from urllib.parse import urlencode

from .geocoding_service import GeocodingService

logger = logging.getLogger(__name__)

BASE_URL = "https://geocoder.api.here.com/6.2/geocode.json?"


class HereGeocodingService(GeocodingService):
    def __init__(self, app_id: str, app_code: str):
        self.app_id = app_id
        self.app_code = app_code

    def geocode(self, address: str):
        url = BASE_URL + urlencode(
            {"app_id": self.app_id, "app_code": self.app_code, "searchtext": address}
        )
        logger.debug(url)
        data = self._do_request(url)

        try:
            # see: https://developer.here.com/documentation/geocoder/topics/reading-geocoding-response.html
            if data is None or len(data["Response"]["View"]) == 0:
                return None

            geocode_result = []
            for result in data["Response"]["View"][0]["Result"]:
                geocode_result.append(
                    {
                        "formatted_address": result["Location"]["Address"]["Label"],
                        "latitude": result["Location"]["DisplayPosition"]["Latitude"],
                        "longitude": result["Location"]["DisplayPosition"]["Longitude"],
                        "service_provider": "Here",
                    }
                )
            return geocode_result
        except KeyError as e:
            logger.error(
                "KeyError while parsing JSON, HERE schema has changed?:\n%s" % e
            )
            return None
