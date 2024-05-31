from django.test import TestCase
from django.urls import reverse


class TBCViewTest(TestCase):
    def test_tbc_view(self):
        response = self.client.get(reverse('tbc'))
        self.assertEqual(response.status_code, 200)

    def test_tbc_view_template(self):
        response = self.client.get(reverse('tbc'))
        self.assertTemplateUsed(response, 'tbc.html')
