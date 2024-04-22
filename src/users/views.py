from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth 
from django.core.handlers.wsgi import WSGIRequest

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

 
def register(request:WSGIRequest):
	match request.method:
		case "POST":
			form = UserCreationForm(request.POST)

			if form.is_valid():
				form.save()
				login(request, form.instance)
				return redirect('home')
			else:
				for message in form.error_messages.values():
					messages.info(request, message)
					status=400
		case "GET":
			form = UserCreationForm()
			status=200

	return render(request, "register.html", {"form":form}, status=status)
 
def login_page(request):
	match request.method:
		case "POST":
			username = request.POST.get("username")
			password = request.POST.get("password")

			user = authenticate(request, username = username, password = password)

			if user is not None:
				login(request, user)
				return redirect("home")
			else:
				messages.info(request, "Username and/or password is incorrect")
				status=400

		case 'GET':
			status=200

	return render (request, "login.html", status=status)


def logout_button(request):
	logout(request)
	return redirect("login")

def delete_user(request):
	request.user.delete()
	return redirect("login")