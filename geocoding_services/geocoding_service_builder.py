import json
import logging

from .google_geocoding_service import GoogleGeocodingService
from .here_geocoding_service import HereGeocodingService

logger = logging.getLogger(__name__)

CREDENTIALS_FILE = "geoservice_credentials.json"


class GeocodingServiceBuilder:
    @staticmethod
    def build_geocoding_services():
        services = {}

        try:
            with open(CREDENTIALS_FILE) as credentials_file:
                data = json.load(credentials_file)
                services["here"] = HereGeocodingService(
                    app_id=data["here"]["appId"], app_code=data["here"]["appCode"]
                )
                services["google"] = GoogleGeocodingService(
                    api_key=data["google"]["apiKey"]
                )
        except (KeyError, OSError) as e:
            logger.error("Credentials file is missing or format is incorrect?\n%s" % e)
            return None

        return services
