from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.http import HttpResponse
from django.db import models
from django.db.models import Count
from .forms import MovieShowForm, ReviewForm
from .models import MovieShow, Review, Genres


def to_home(request):
	return redirect('/home')

def home(request):
	most_common = Review.objects.values("target").annotate(count=Count('target')).order_by("-count")
	results = MovieShow.objects.none()
	i = 0
	while i <= 6:
		try: 
			results |= MovieShow.objects.filter(pk=most_common[i]['target'])
			i += 1
		except IndexError:
			break

	return render(request, 'home.html', {'results' : results})

# this function will add new movie or show to the site 
def add(request:WSGIRequest):
	if not request.user.is_authenticated:
		return render(request, 'must_be_logged_in.html', status=403)
	match request.method:
		case 'GET':
			genres = Genres.objects.all()
			form = MovieShowForm()
			status = 200
		case 'POST':
			form = MovieShowForm(request.POST, request.FILES,  request.user)
			form.instance.creator = request.user
			if form.is_valid():
				movie:MovieShow = form.save()
				return redirect(movie)
			else:
				genres = Genres.objects.all()
				status = 400

	return render(request,'add_title.html', {'genres':genres,'form':form}, status=status)

def title(request, title):
	match request.method:
		case 'GET':
			try:
				movie = MovieShow.objects.get(title=title)
				reviews = Review.objects.filter(target=movie.id).order_by("creation_time").reverse()
				context = {
					"movie": movie,
					"reviews": reviews
				}
				status=200
			
			except MovieShow.DoesNotExist:
				return render(request, 'not_found.html', status=404)

		case 'POST':
			if not request.user.is_authenticated:
				return render(request, 'must_be_logged_in.html', status=403)

			try:
				movie = MovieShow.objects.get(title=title)
			except MovieShow.DoesNotExist:
				return render(request, 'not_found.html', status=404)

			form = ReviewForm(request.POST or None)
			if form.is_valid():
				form.instance.target = MovieShow.objects.get(title=title)
				form.instance.author = request.user
				form.save()

				reviews = Review.objects.filter(target=movie.id).order_by("creation_time").reverse()

				context = {
					"movie": movie,
					"reviews": reviews,
				}
				status=201
				
			else:
				return HttpResponse(status=400)

	return render(request, 'title.html', context, status=status)

def search(request):
	if request.method == "GET":
		search_input = request.GET.get("search")
		category_input = request.GET.getlist("category_option")
		genre_input = request.GET.getlist("genre_option")

		genres = Genres.objects.all()

		if not search_input and not category_input and not genre_input:
			return render (request, "search.html", {"categories":( item[1] for item in  MovieShow.CATEGORY) , "genres":genres})

		if 'Movie' in category_input and 'Show' in category_input or category_input == []:
			results = MovieShow.objects.filter(title__contains=search_input)
		elif 'Movie' in category_input and 'Show' not in category_input:
			results = MovieShow.objects.filter(title__contains=search_input).exclude(category='Show')
		else:
			results = MovieShow.objects.filter(title__contains=search_input).exclude(category='Movie')
	
		if genre_input != []:
			results = results.filter(genres__genre__in = genre_input).distinct()

		return render (request, "search.html", {'categories':( item[1] for item in  MovieShow.CATEGORY), 'genres':genres, 'search_input':search_input, 'results':results})