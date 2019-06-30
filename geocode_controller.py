import logging

from connexion import request
from flask import abort

from geocoding_services.geocoding_service_builder import GeocodingServiceBuilder

logger = logging.getLogger(__name__)

SERVICES = GeocodingServiceBuilder.build_geocoding_services()


def get(address: str):
    """
    This function responds to a request for /v1/geocode
    :param address:  address to use for the geocode request
    :return:        json geocode result if available
    """
    if not address:
        abort(400, "The address parameter was provided but is empty.")
    if not SERVICES:
        abort(500)

    force_service = request.args.get("force_service")
    geocoding_service = SERVICES.get(force_service)
    geocode_result = None

    # Flask returns 500 on Exception and logs the error automatically - no need for explicit handling in the general case
    # http://flask.pocoo.org/docs/1.0/errorhandling/
    if geocoding_service is not None:
        geocode_result = geocoding_service.geocode(address)
    else:
        for service in SERVICES.values():
            geocode_result = service.geocode(address)
            if geocode_result is not None:
                break

    if geocode_result is None:
        return {"results": []}

    return {"results": geocode_result}
