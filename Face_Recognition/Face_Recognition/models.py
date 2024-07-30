from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
	rt = [
		(0,'User'),
		(1,'Driver'),
		(2,'Staff'),
		(3,'admin'),
	]
	License = models.CharField(max_length=20)
	role_type = models.IntegerField(default=0)
	upfe = models.ImageField(upload_to='Profiles/',default='sample.png')
	
class DriverProfile(models.Model):
	g = [
		("k","Select Your Gender"),
		('M',"Male"),
		("F","Female")
		]
	Av = [
		("Ava","Select your Availability"),
		("Mrng","Morning Shift:7:00 AM to 3:00 PM"),
		("Day","Day Shift:10:00 AM to 6:00 PM"),
		("Eve","Evening Shift:3:00 PM to 11:00 PM"),
		("Night","Night Shift:11:00 PM to 7:00 AM")
	]
	age = models.IntegerField()
	gender = models.CharField(max_length=5,default='k',choices=g)
	Availability = models.CharField(max_length=5,default='Ava',choices=Av)
	expr = models.IntegerField()
	Driver = models.OneToOneField(User,on_delete=models.CASCADE)
	status = models.BooleanField(default=0)

class StaffProfile(models.Model):
	sg = [
		("h","Select Your Gender"),
		('M',"Male"),
		("F","Female")
	]
	Av = [
		("Ava","Select your Availability"),
		("Mrng","Morning Shift:7:00 AM to 3:00 PM"),
		("Day","Day Shift:10:00 AM to 6:00 PM"),
		("Eve","Evening Shift:3:00 PM to 11:00 PM"),
		("Night","Night Shift:11:00 PM to 7:00 AM")
	]
	age = models.IntegerField()
	gender = models.CharField(max_length=5,default='k',choices=sg)
	Availability = models.CharField(max_length=50,default='Ava',choices=Av)
	expr = models.IntegerField()
	contact = models.IntegerField()
	salary = models.IntegerField(default=20000)
	Staff = models.OneToOneField(User,on_delete=models.CASCADE)
	status = models.BooleanField(default=0)

class UserProfile(models.Model):
	g = [
		("k","Select your Gender"),
		("M","Male"),
		("F","Female")
	]
	age = models.IntegerField()
	gender = models.CharField(max_length=5,default='k',choices=g)
	contact = models.IntegerField()
	address = models.CharField(max_length=50)
	Users = models.OneToOneField(User,on_delete=models.CASCADE)
	status = models.BooleanField(default=0)

class AdminProfile(models.Model):
	g = [
		("k","Select your Gender"),
		("M","Male"),
		("F","Female")
	]
	age = models.IntegerField()
	gender = models.CharField(max_length=5,default='k',choices=g)
	Admin = models.OneToOneField(User,on_delete=models.CASCADE)
	status = models.BooleanField(default=0)

class trips(models.Model):
    x = [
        ("k", "Select your Departure"),
        ("H", "Hyderabad"),
        ("M", "Mumbai"),
        ("D", "Delhi"),
        ("K", "Kolkata"),
    ]
    xy = [
        ("k", "Select your Destination"),
        ("H", "Hyderabad"),
        ("M", "Mumbai"),
        ("D", "Delhi"),
        ("K", "Kolkata"),
    ]
    k = [
	    ('0',"Pending"),
	    ('1',"Declined"),
	    ('2',"Accepted"),
	    ('3',"Completed")
    ]
    Trip_ID = models.AutoField(primary_key=True)
    Booking_Status = models.IntegerField(default=0)
    Departure = models.CharField(max_length=5, default='k', choices=x)
    Destination = models.CharField(max_length=5, default='k', choices=xy)
    Username = models.CharField(default=0, max_length=50)
    Drivername = models.CharField(max_length=50)
    status = models.CharField(default='0', choices=k, max_length=50)


class data_status(models.Model):
	Trip_ID = models.IntegerField()
	Timestamp = models.IntegerField()
	Eye_Hull = models.IntegerField()
	Lip_Hull = models.IntegerField()

class data_submit(models.Model):
	Trip_ID = models.IntegerField()
	Timestamp = models.IntegerField()
	Blink = models.IntegerField()
	Yawn = models.IntegerField()
