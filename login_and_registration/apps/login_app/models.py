from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime
class UserManager(models.Manager):
	def register(self, name, username, password, confirm):

		errors = []
		if len(name) < 2:
			errors.append("name must be 2 characters or longer!")
		# elif not re.match('[A-Za-z]+', name['name']):
  #           errors.append("First name must only contain letters!"

		if len(username) < 2:
			errors.append("Username must be 2 characters or longer!")
		elif len(User.userManager.filter(username=username)) > 0:
			errors.append("Username already exists!")

		if len(password) < 8:
			errors.append("Password must be 8 characters or longer!")
		if not password == confirm:
			errors.append("Password must match Confirm Password!")

		if len(errors) > 0:
			return (False, errors)
		else:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			user = User.userManager.create(username=username, name= name, pw_hash=pw_hash)
			return (True, user)

	def login(self, username, password):

		errors = []

		if len(username) < 2:
			errors.append("Username must be 2 characters or longer!")
		if len(password) < 8:
			errors.append("Password must be 8 characters or longer!")

		user = User.userManager.filter(username=username)

		if len(user) == 0:
			errors.append("Username not found!")

		if len(errors) > 0:
			return (False, errors)
		else:
			if bcrypt.checkpw(password.encode(), user[0].pw_hash.encode()):
				return (True, user[0])
			else:
				return (False, ["Incorrect Password!"])

class User(models.Model):
	name =  models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	pw_hash = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	userManager = UserManager()

	def __repr__(self):
		return "<User: {} {} {} >".format(
			# self.name,
			self.username,			
			self.created_at,
			self.updated_at
		)
class TravelManager(models.Manager):
	def journey(self, destination, description, travel_date_from, travel_date_to, creator_id):
		errors = []
		if len(destination) < 1:
			errors.append("Destination field cannot be left blank!")

		if len(description) < 1:
			errors.append("Description field cannot be blank!")

		if len(travel_date_from ) < 1:
			errors.append("Start date fields cannot be blank!")
		elif travel_date_from < str(datetime.now()):
			errors.append("Start date must be in the future!")

		if len(travel_date_to ) < 1:
			errors.append("End date fields cannot be blank!")
		elif travel_date_to < str(datetime.now()):
			errors.append("End date must be in the future!")
		if travel_date_from > travel_date_to:
			errors.append("Start date must be before the end date!")

		if len(errors) > 0:
			return errors
		else:
			return Travel.objects.create(destination=destination, description=description,travel_date_from=travel_date_from, travel_date_to=travel_date_to, creator_id=creator_id)
			# return errors
		
class Travel(models.Model):
	destination = models.CharField(max_length = 255)
	description = models.TextField()
	travel_date_from = models.DateTimeField()
	travel_date_to = models.DateTimeField()	
	creator = models.ForeignKey(User, related_name="Travels")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TravelManager()

	def __repr__(self):
		return "<Travel: {} {} {} {} {} {}>".format(
			self.destination,
			self.description,
			self.travel_date_from,
			self.travel_date_to,
			self.created_at,
			self.updated_at
		)
class Join(models.Model):
	user = models.ForeignKey(User, related_name = "users")
	travel = models.ForeignKey(Travel, related_name = "travels")

	def __repr__(self):
		return "<join {} {}>".format(self.user_id, self.travel_id)		
# class TripManager(models.Manager):
# 	def trip(self, selection, tourist, travel):
# 		if len(trip.tripManager.filter(tourist_id=tourist).filter(travel_id=travel)) == 0:
# 			tourist.tripManager.create(selection=selection, tourist_id=tourist, travel_id=travel)
# 			return True
# 		else:
# 			return False

# class Trip(models.Model):
# 	selection = models.IntegerField(max_length = 255)
# 	tourist = models.ForeignKey(User, related_name="tourists")
# 	travel = models.ForeignKey(Travel, related_name="travels")

# 	tripManager = TripManager()
