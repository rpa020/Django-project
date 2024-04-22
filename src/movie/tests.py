from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import MovieShow, Genres, Review
from .forms import MovieShowForm
from datetime import timedelta, date
from urllib.parse import unquote
from base64 import b64decode
from os import remove
from os.path import exists


testfilm = {
	'title':'Test Movie',
	'release_date':'2020-04-07',
	'description':'Awesome movie!',
	'category':'Movie',
	'director':'George Dicaprio',
	'age_rating':'G',
	'runtime':timedelta(hours=2,minutes=30),

}

testfilm1 = {
	'title':'Test Sequel',
	'release_date':'2021-05-31',
	'description':'Awesome follow up!',
	'category':'Movie',
	'director':'George Dicaprio',
	'age_rating':'G',
	'runtime':timedelta(hours=2,minutes=30),
}

testshow = {
	'title':'Test Show',
	'release_date':'2019-12-23',
	'description':'Boring show...',
	'category':'Show',
	'director':'Taika Shyamalan',
	'age_rating':'PG-13',
	'runtime':timedelta(hours=2,minutes=30),
}

testshow1 = {
	'title':'Test Series',
	'release_date':'1992-12-23',
	'description':'Amasing series!',
	'category':'Show',
	'director':'Rian Abrams',
	'age_rating':'PG-13',
	'runtime':timedelta(hours=2,minutes=30),
}

reviews = [
	{
		'rating':9,
		'headline':'Great film',
		'review_text':'I liked it',
	},
	{
		'rating':8,
		'headline':'Pretty good',
		'review_text':'I liked it',
	},
	{
		'rating':2,
		'headline':'Horrible',
		'review_text':'Not my personal cup of tea',
	},
]

class HomeTest(TestCase):
	'''
	Test for the home page
	'''
	def setUpTestData():
		user = User.objects.create(username='user')
		
		title = MovieShow.objects.create(**testfilm)
		for review in reviews:
			Review.objects.create(target=title, author=user, **review)
		
		title = MovieShow.objects.create(**testfilm1)
		for review in reviews:
			Review.objects.create(target=title, author=user, **review)
		
		title = MovieShow.objects.create(**testshow)
		for review in reviews:
			Review.objects.create(target=title, author=user, **review)
		
		title = MovieShow.objects.create(**testshow1)
		for review in reviews:
			Review.objects.create(target=title, author=user, **review)

	def setUp(self):
		self.url = reverse('home')
		self.client = Client()

	def test_redirect_home(self):
		'''
		GET request to `/` should redirect to home
		'''
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, self.url)

	def test_home_page(self):
		'''
		Very simple test that checks for the project logo in the home page
		'''
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)

		templatesused = [template.name for template in response.templates]
		self.assertIn('home.html', templatesused)
		self.assertIn('topnav.html', templatesused)
		self.assertIn('base.html', templatesused)

class AddTest(TestCase):

	@classmethod
	def setUpTestData(self):
		self.user = User.objects.create()
	
	def setUp(self):
		self.client = Client()
		self.client.force_login(self.user)
		self.add_url = reverse('add')

	def test_unauth_add(self):
		self.client.logout()
		response = self.client.get(self.add_url)

		self.assertEqual(response.status_code, 403)

		templatesused = [template.name for template in response.templates]
		self.assertIn('base.html', templatesused)
		self.assertIn('must_be_logged_in.html', templatesused)

	def test_add_page(self):
		response = self.client.get(self.add_url)

		self.assertEqual(response.status_code, 200)
		self.assertInHTML(MovieShowForm().as_p(), response.content.decode('utf-8'))

	def test_add(self):
		
		response = self.client.post(self.add_url, data=testfilm)
		with open('z', 'w') as f:
			f.write(response.content.decode('utf-8'))

		instance = MovieShow.objects.filter(title=testfilm['title'])[0]

		self.assertIsNotNone(instance)

		instancetemplate = testfilm.copy()

		instancetemplate['release_date'] = date.fromisoformat(instancetemplate['release_date'])

		self.assertDictContainsSubset(instancetemplate, model_to_dict(instance))

	def test_invalid_add(self):
		invalidfilm = testfilm.copy()

		invalidfilm['title'] = ''

		response = self.client.post(self.add_url, data=invalidfilm)

		for field in invalidfilm.values():
			if isinstance(field, timedelta):
				field = '2:30:00'
			self.assertIn(field, response.content.decode('utf-8'))

		self.assertIn('This field is required.', response.content.decode('utf-8'))

	def test_add_redirect(self):
		response = self.client.post(self.add_url, data=testfilm1)
		instance = MovieShow.objects.filter(title=testfilm1['title'])[0]

		self.assertEqual(response.status_code, 302)
		self.assertEqual(unquote(response.url), instance.get_absolute_url())

# Test model
class MovieTest(TestCase):

	@classmethod
	def setUpTestData(self):
		self.movie0 = MovieShow.objects.create(**testfilm)
		self.movie1 = MovieShow.objects.create(**testfilm1)

	def setUp(self):
		self.client = Client()

	def test_display_page(self):
		response = self.client.get(f'/titles/{self.movie0}/')

		for name, field in model_to_dict(self.movie0).items():
			if name == 'poster' or name == 'genres':
				continue
			self.assertIn(str(field), response.content.decode('utf-8'))

		response = self.client.get(f'/titles/{self.movie1}/')

		for name, field in model_to_dict(self.movie1).items():
			if name == 'poster' or name == 'genres':
				continue
			self.assertIn(str(field), response.content.decode('utf-8'))

	def test_nonexistant_page(self):
		response = self.client.get('/titles/Does not exist/')

		self.assertEqual(response.status_code, 404)

	def test_poster(self):
		self.client.force_login(User.objects.create())

		poster_show = testshow.copy()
		poster_show['poster'] = SimpleUploadedFile('poster.png', b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUA" + "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO" + "9TXL0Y4OHwAAAABJRU5ErkJggg==") , content_type='png')

		if exists('media/posters/poster.png'): remove('media/posters/poster.png')
		

		response = self.client.post('/titles/add/', poster_show)

		self.assertEqual(response.status_code, 302)

		response = self.client.get(response.url)

		with open('z','wb') as f:
			f.write(response.content)

		self.assertInHTML(f'<img src="/media/posters/poster.png" alt="{poster_show["title"]}" id="poster" >', response.content.decode('utf-8'))

		remove('media/posters/poster.png')
		


class FilterTest(TestCase):

	@classmethod
	def setUpTestData(self):
		drama = Genres.objects.get_or_create(genre="Drama")[0]
		action = Genres.objects.get_or_create(genre="Action")[0]

		movie_drama = MovieShow.objects.create(**testfilm)
		movie_drama.genres.add(drama)
		movie_drama.save()
		movie_action = MovieShow.objects.create(**testfilm1)
		movie_action.genres.add(action)
		movie_action.save()
		show_drama = MovieShow.objects.create(**testshow)
		show_drama.genres.add(drama)
		show_drama.save()
		show_action = MovieShow.objects.create(**testshow1)
		show_action.genres.add(action)
		show_action.save()
		self.movies  = [movie_action,movie_drama]
		self.shows   = [show_action, show_drama]
		self.actions = [movie_action,show_action]
		self.dramas  = [movie_drama, show_drama]

	def setUp(self):
		self.client = Client()
		self.url = reverse('search')

	def test_category(self):
		response = self.client.get(self.url, data={'search':'','category_option':'Show'})
		for show in self.shows:
			self.assertIn(show.title, response.content.decode('utf-8'))

		response = self.client.get(self.url, data={'search':'','category_option':'Movie'})
		for movie in self.movies:
			self.assertIn(movie.title, response.content.decode('utf-8'))

	def test_genres(self):
		response = self.client.get(self.url, data={'search':'','genre_option':'Drama'})
		for drama in self.dramas:
			self.assertIn(drama.title, response.content.decode('utf-8'))
		for action in self.actions:
			self.assertNotIn(action.title, response.content.decode('utf-8'))

		response = self.client.get(self.url, data={'search':'','genre_option':'Action'})
		for action in self.actions:
			self.assertIn(action.title, response.content.decode('utf-8'))
		for drama in self.dramas:
			self.assertNotIn(drama.title, response.content.decode('utf-8'))


# Tets search function
class SearchTest(TestCase):

	def setUp(self):

		self.client = Client()
		self.search_url = reverse('search')
		MovieShow.objects.create(**testfilm)

	def test_search(self):

		# Normal search

		response = self.client.get(self.search_url, {'search' : 'The Movie'})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['search_input'], 'The Movie')

	def test_empty_search(self):
		# Test empty search

		response = self.client.get(self.search_url, {'search' : ''})

		self.assertEqual(response.status_code, 200)
		
		
		self.assertNotIn('search_input', response.context)

	def test_long_search(self):

		# Search with random chars in a too long string
		response = self.client.get(self.search_url, {'search' : 'THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_'})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['search_input'], 'THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_THIS_IS_A_VERY_LONG_FILM_TITLE_')


class ReviewTest(TestCase):
	@classmethod
	def setUpTestData(self):
		self.user = User.objects.create()
		self.title = MovieShow.objects.create(**testfilm)

	def setUp(self):
		self.client = Client()
		self.client.force_login(self.user)
		self.url = self.title.get_absolute_url()

	def test_unauth_post(self):
		self.client.logout()
		response = self.client.post(self.url, data=reviews[0])
		self.assertEqual(response.status_code, 403)

		self.assertIn('must_be_logged_in.html', [template.name for template in response.templates])

	def test_post_review(self):
		for review in reviews:
			response = self.client.post(self.url, data=review)
			self.assertEqual(response.status_code, 201)

			self.assertIn(review['headline'], response.content.decode('utf-8'))
			self.assertIn(review['review_text'], response.content.decode('utf-8'))

	def test_post_review_on_nonexistant_page(self):
		response = self.client.post('/titles/Does not exist/', data=reviews[0])

		self.assertEqual(response.status_code, 404)
		self.assertIn('not_found.html', [template.name for template in response.templates])

	def test_bad_review(self):
		response = self.client.post(self.url, data={'headline':'haha','review_text':'so funny'})

		self.assertEqual(response.status_code, 400)


	def test_get_reviews(self):
		for review in reviews:
			self.client.post(self.url, data=review)


		response = self.client.get(self.url)
		
		for review in reviews:
			self.assertIn(review['headline'], response.content.decode('utf-8'))
			self.assertIn(review['review_text'], response.content.decode('utf-8'))
