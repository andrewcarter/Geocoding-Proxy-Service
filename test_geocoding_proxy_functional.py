import json
import unittest

from server import create_app


class GeocodingProxyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.app.test_client

    def test_geocode_valid(self):
        res = self.client().get("/v1/geocode?address=waldo")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreater(len(data["results"]), 0)
        for result in data["results"]:
            self.assertIsNotNone(result["latitude"])
            self.assertIsNotNone(result["longitude"])
            self.assertIsNotNone(result["formatted_address"])
            self.assertIsNotNone(result["service_provider"])

    def test_geocode_no_params(self):
        res = self.client().get("/v1/geocode?")
        self.assertEqual(res.status_code, 400)

    def test_geocode_empty_address(self):
        res = self.client().get("/v1/geocode?address=")
        self.assertEqual(res.status_code, 400)

    def test_geocode_unknown_address(self):
        res = self.client().get(
            "/v1/geocode?address=ThisIsProbablyABadAddress...FooBar42"
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(len(data["results"]) == 0)

    def test_geocode_bad_verb(self):
        res = self.client().post("/v1/geocode?address=waldo")
        self.assertEqual(res.status_code, 405)

    def test_geocode_force_service_here(self):
        res = self.client().get("/v1/geocode?address=waldo&force_service=here")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreater(len(data["results"]), 0)
        for result in data["results"]:
            self.assertEqual(result["service_provider"], "Here")

    def test_geocode_force_service_google(self):
        res = self.client().get("/v1/geocode?address=waldo&force_service=google")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertGreater(len(data["results"]), 0)
        for result in data["results"]:
            self.assertEqual(result["service_provider"], "Google")

    def test_geocode_force_service_empty(self):
        res = self.client().get("/v1/geocode?address=waldo&force_service=")
        self.assertEqual(res.status_code, 400)

    def test_geocode_force_service_bad_option(self):
        res = self.client().get("/v1/geocode?address=waldo&force_service=foobar")
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
