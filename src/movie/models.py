from random import sample
from datetime import timedelta
from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

# Genres for movies and shows
class Genres(models.Model):
	choices = (
			('action', 'Action'),
			('comedy', 'Comedy'),
			('drama', 'Drama'),
			('fantasy', 'Fantasy'),
			('horror', 'Horror'),
			('mystery', 'Mystery'),
			('romance', 'Romance'),
			('thriller', 'Thriller'),
		)

	genre = models.CharField(unique=True, max_length=20, null="True", choices=choices)

	def __str__(self):
		return self.genre


# Database model for a movie or a show
class MovieShow(models.Model):

	CATEGORY = [
		('Movie', 'Movie'),
		('Show', 'Show')
	]

	MPAA = [
		('G', 'G rated'),
		('PG', 'PG rated'),
		('PG-13', 'PG-13 rated'),
		('R', 'R rated'), 
		('NC-17', 'NC-17 rated')
	]


	title = models.CharField(max_length=50, unique=True)
	release_date = models.DateField()
	poster = models.ImageField(upload_to='posters/', blank=True)
	description = models.TextField(max_length=100_000)
	category = models.CharField(max_length=50, null=True, choices=CATEGORY)
	genres = models.ManyToManyField(Genres, blank=True)
	director = models.CharField(max_length=50, unique=False, null=False, default='Unknown')
	age_rating = models.CharField(max_length=10, null=False, choices=MPAA)
	runtime = models.DurationField(blank=False, default=timedelta)
	creator = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, null=True)


	def save(self, *args, **kwargs):
		'''
		This method will crop all images before uploading it
		'''
		super().save(*args, **kwargs)
		if self.poster:
			image = Image.open(self.poster.path)
			width, height = image.size
			standard_height = 600
			standard_width = 400

			if width == standard_width and height == standard_height:
				image.save(self.poster.path)

			elif width > standard_width and height > standard_height or width < standard_width and height < standard_height: 
				new_image = image.resize((standard_width, standard_height), resample=1)
				new_image.save(self.poster.path)


	def get_absolute_url(self):
		return f'/titles/{self.title}/'


	def __str__(self):
		return self.title


RATING_CHOICES = [
	(1, '1'),
	(2, '2'),
	(3, '3'),
	(4, '4'),
	(5, '5'),
	(6, '6'),
	(7, '7'),
	(8, '8'),
	(9, '9'),
	(10, '10')
]


class Review(models.Model):

	rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
	headline = models.CharField(max_length=100, blank=True)
	review_text = models.CharField(max_length=2500, blank=True)
	target = models.ForeignKey(MovieShow, blank=False, on_delete=models.CASCADE)
	author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
	creation_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.author.username
