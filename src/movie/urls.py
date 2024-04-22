from django.urls import path
from .views import search, add, title

urlpatterns = [
	path('search/', search, name = "search"),
	path('add/', add, name="add"),
	path('<str:title>/', title, name="title"),

]
