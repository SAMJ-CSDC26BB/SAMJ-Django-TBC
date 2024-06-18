from django.test import TestCase
from django.urls import reverse
import logging

class RestEndpointTestCase(TestCase):
    #does not work
    def test_rest_endpoint_with_number(self):
        number = "+436776310644"
        url = reverse('restEndpoint')  # Replace 'rest_endpoint' with the actual URL name of your REST endpoint
        response = self.client.get(url, {'number': number})
        self.assertEqual(response.GET.get('number', ''), 200)
        logging.info("TEST response -> " + response.GET.get('number', ''))

