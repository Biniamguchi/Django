from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
import random
import string


def random_word(n):
    return get_random_string(length=n)
    # return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

# Create your views here.
def index(request):
    # try:
    #     request.session['tries']
    # except KeyError:
    #     request.session['tries'] = 0
    if "tries" not in request.session:
        request.session ["tries"] = 0
    else:
        request.session["tries"] 

    return render(request, "users/index.html")

def generate(request):
    request.session['tries'] += 1  
    request.session['word'] = get_random_string(length=14)
    return redirect('/')

def reset(request):
    del request.session['tries']
    del request.session['word']
    return redirect('/')

