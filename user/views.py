from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserAuthForm

# Create your views here.
def auth(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		form = UserAuthForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user);
				return redirect("/")
			else:
				form.add_error(None, "Пара логин-пароль не найдена")
	else:
		form = UserAuthForm()
	return render(request, "user_auth.html", {'form': form})

def reg(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			username, email, password, password2 = form.cleaned_data
			user = get_user_model().objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])
			login(request, user)
			return redirect("/")
	else:
		form = UserForm()
	return render(request, "user_reg.html", {'form': form})

@login_required
def user_logout(request):
	logout(request)
	return redirect('/')
