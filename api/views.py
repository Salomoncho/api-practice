from django.shortcuts import render, HttpResponse

# Create your views here.

def ApiHome(request):
  return HttpResponse('Hola')