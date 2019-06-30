import json
import logging
from abc import ABC, abstractmethod
from urllib import error, request

logger = logging.getLogger(__name__)


class GeocodingService(ABC):
    @abstractmethod
    def geocode(self, address: str):
        pass

    # TODO: Add LRU cache with expiry to handle duplicate client requests, etc (Key is full service URL)
    @staticmethod
    def _do_request(url: str):
        req = request.Request(url)
        try:
            r = request.urlopen(req)
            if r.getcode() != 200:
                logging.info(str(r))
                return None
        except error.HTTPError as e:
            logging.warning(e)
            # Downstream service HTTPError should be transparent to client
            return None

        return json.load(r)
