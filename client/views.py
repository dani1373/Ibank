from django.shortcuts import render


def client_login(request):
  return render(request, 'login.html')


def index(request):
  return render(request, 'index.html')


def listh(request):
  return render(request, 'list.html')


def form(request):
  return render(request, 'form.html')
