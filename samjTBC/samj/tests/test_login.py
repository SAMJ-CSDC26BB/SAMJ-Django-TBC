from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class LoginViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, './login/login.html')
