from django import forms
from django.forms import ModelForm
from .models import Genres, RATING_CHOICES, MovieShow, Review 


class MovieShowForm(ModelForm): 
	class Meta: 
		model = MovieShow
		fields = ['title', 'release_date', 'poster', 'description', 'category', 'runtime', 'genres', 'director', 'age_rating']
		widgets = {
			'genres': forms.CheckboxSelectMultiple(),
			'release_date': forms.TextInput(attrs={'class': 'form-control', 'type':'date'})
		}

class ReviewForm(ModelForm):
	class Meta: 
		model = Review
		fields = ('rating', 'headline','review_text')