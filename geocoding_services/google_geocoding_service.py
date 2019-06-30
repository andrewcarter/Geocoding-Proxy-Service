import logging
from urllib.parse import urlencode

from .geocoding_service import GeocodingService

logger = logging.getLogger(__name__)

BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"


class GoogleGeocodingService(GeocodingService):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def geocode(self, address: str):
        url = BASE_URL + urlencode({"key": self.api_key, "address": address})
        logger.debug(url)
        data = self._do_request(url)

        try:
            # see: https://developers.google.com/maps/documentation/geocoding/intro#StatusCodes
            if data is None or data["status"] == "ZERO_RESULTS":
                return None
            elif data["status"] != "OK":
                logger.error(
                    "Unexpected status from Google Geocoding Service:\n%s" % (data)
                )
                return None

            geocode_result = []
            for result in data["results"]:
                geocode_result.append(
                    {
                        "formatted_address": result["formatted_address"],
                        "latitude": result["geometry"]["location"]["lat"],
                        "longitude": result["geometry"]["location"]["lng"],
                        "service_provider": "Google",
                    }
                )
            return geocode_result
        except KeyError as e:
            logger.error(
                "KeyError while parsing JSON, Google schema has changed?:\n%s" % e
            )
            return None
