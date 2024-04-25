from django.test import TestCase


# Testing for specifically views

class HomePageTest(TestCase):

    def test_get_request(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.html")
