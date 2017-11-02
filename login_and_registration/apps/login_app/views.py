from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Travel, Join
from django.contrib import messages

def index(req):
	
	return render(req, "login_app/index.html")

def register(req):
	valid = User.userManager.register(
		req.POST['name'],
		req.POST['username'],
		req.POST['password'],
		req.POST['confirm'],
	)
	if valid[0]:
		req.session["user"] = {
			"id": valid[1].id,
			"username": valid[1].username
		}
		return redirect('/')

	else:
		for error in valid[1]:
			messages.add_message(req, messages.ERROR, error)
	return redirect('/')
def login(req):
	valid = User.userManager.login(
		req.POST['username'],
		req.POST['password']
	)
	if valid[0]:
		req.session["user"] = {
			"id": valid[1].id,
			"name": valid[1].name
		}
		return redirect('/travels')
	else:
		for error in valid[1]:
			messages.add_message(req, messages.ERROR, error)
	return redirect('/')

def logout(req):
	req.session.clear()
	messages.add_message(req, messages.INFO, "You have been logged out.", extra_tags='logout')
	return redirect('/')

# def home(req):
# 	return render(req, "login_app/travels.html")
	

def travels(req):

	if 'user' not in req.session:
		return redirect('/')
	if req.method == 'GET':
		# return render(req, "login_app/travels.html", {"travels": Travel.objects.all()})
		context = {
			"travels": Join.objects.filter(user_id=req.session["user"]["id"]),
			"allTravels": Travel.objects.all()
		}
		return render(req, "login_app/travels.html", context)
	elif req.method == 'POST':
		destination = req.POST['destination']
		description = req.POST['description']
		travel_date_from = req.POST['travel_date_from']
		travel_date_to= req.POST['travel_date_to']
		
		errors = Travel.objects.journey(destination, description, travel_date_from,travel_date_to,req.session["user"]["id"])
		
		if type(errors) == list:
			for error in errors:
				messages.add_message(req, messages.ERROR, error)
			return redirect('/travels/new')
		else:
			Join.objects.create(user_id=req.session["user"]["id"], travel_id=errors.id)
			

			return redirect('/travels')
	# return render(req, "login_app/travels.html", {"travels": Travel.objects.all()})

def new_travel(req):
	if 'user' not in req.session:
		return redirect('/')
	return render(req, "login_app/new_travel.html")


def create(req, id):
	# travel  = Travel.objects.get(id=id)

	# return render(req, "login_app/trip.html", {"travel":travel} )

	if 'user' not in req.session:
		return redirect('/')
	if req.method == 'GET':
		travel = Travel.objects.get(id=id)
		return render(req, "login_app/trip.html", {"travel":travel} )
		
		# return render(req, "login_app/trip.html", {"travel": travel, "voted": voted, "results": results})
	elif req.method == 'POST':
		Trip.tripManager.trip(
			int(req.POST["selection"]),
			req.session["user"]["id"],
			int(id)
		)

		# return redirect("/travels")

def join(req, id):
	# if 'user' not in req.session:
	# 	return redirect('/')
	# if req.method == 'GET':
	# 	travel = Travel.objects.get(id=id)
	# 	return render(req, "login_app/trip.html", {"travel":travel} )
	# 	return redirect("/travels")

	if req.method == 'GET':
		Join.objects.create(user_id=req.session["user"]["id"], travel_id=id)
		return redirect("/travels")

def leave(req, id):
    travel = Travel.objects.get(id=id)
    travel.save()
    user = User.objects.get(id=req.session['user_id'])
    travel.users.remove(user)
    if not travel.users.all():
        travel.delete()
    return redirect('/travels')