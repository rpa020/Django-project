from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

class LogInTest(TestCase):

	username='testuser1'
	password='123'
	credentials={'username':username, 'password':password}

	def setUpTestData():
		User.objects.create_user(**LogInTest.credentials)


	def setUp(self):
		self.client = Client()
		self.url = reverse('login')

	def test_login_page(self):
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertIn('login.html', [template.name for template in response.templates])

	def test_login(self):
		response = self.client.post(self.url, self.credentials)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(response.wsgi_request.user.is_authenticated)

	def test_invalid_login(self):
		response = self.client.post(self.url, {'username':self.username, 'password':'abc123'})

		self.assertEqual(response.status_code, 400)

	def test_logout(self):
		self.client.login(**self.credentials)

		response = self.client.get('/logout/')

		self.assertFalse(response.wsgi_request.user.is_authenticated)


class RegisterTest(TestCase):

	username = 'testuser1'
	password = 'AOF09jo!#spNA8PNONDS'

	def setUp(self):
		self.client = Client()
		self.url = reverse('register')

	def test_register_page(self):
		response = self.client.get(self.url)

		self.assertEqual(response.status_code, 200)
		self.assertIn('register.html', [template.name for template in response.templates])

	def test_register(self):
		response = self.client.post(self.url, {'username': self.username, 'password1': self.password, 'password2': self.password})

		self.assertTrue(self.client.login(username=self.username, password=self.password))

	def test_invalid_register(self):
		response = self.client.post(self.url, {'username': self.username, 'password1': self.password, 'password2': 'abc123'})

		self.assertEqual(response.status_code, 400)
		self.assertFalse(self.client.login(username=self.username, password=self.password))
