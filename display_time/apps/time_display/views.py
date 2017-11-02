from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime


# def index(request):
#     response = "Hello, I am your first request!"
#     return HttpResponse(response)

def test(request):
    response = "Hello, I am your first test!"
    return HttpResponse(response)


def index(request):
  context = {
  "time": strftime("%b %d, %Y %I:%M %p", gmtime())
  }
  return render(request,'time_display/index.html', context)

def yourMethodFromUrls(request):
  context = {
  "first_name":"Paul"
  }
  return render(request,'time_display/index.html', context)