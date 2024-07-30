from django import forms
from . models import User, StaffProfile, DriverProfile, UserProfile, AdminProfile, trips
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class UserForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Password"}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Confirm Password"}))
	class Meta:
		model = User
		fields = ["username","License"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Username",
			}),
		"License":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter ID",
			}),
		}

 
class updateprofileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","License","first_name","last_name","email","upfe"]
		widgets = {
		"first_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"First Name",
			}),
		"last_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Last Name",
			}),
		"email":forms.EmailInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter your Email ID",
			}),
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"User ID",
			}),
		"License":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter your License ID",
			"readonly":True,
			}),
		}


class adminupdateprofileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","first_name","last_name","email","upfe"]
		widgets = {
		"first_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"First Name",
			}),
		"last_name":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Last Name",
			}),
		"email":forms.EmailInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter your Email ID",
			}),
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"User ID",
			}),
		}


class DriverprofileForm(forms.ModelForm):
	class Meta:
		model = DriverProfile
		fields = ["age","gender","Availability","expr"]
		widgets = {
		"age":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your age",
			}),
		"gender":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"Availability":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"expr":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter your Experience",
			}),
		}


class StaffprofileForm(forms.ModelForm):
	class Meta:
		model = StaffProfile
		fields = ["age","gender",'Availability','expr','contact','salary']
		widgets = {
		"age":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your age",
			}),
		"gender":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"Availability":forms.Select(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your Availability",
			}),
		"expr":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your Experience",
			}),
		"contact":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your Contact",
			}),
		"salary":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Your Salary",
			"readonly":True,
			}),
		}


class UserprofileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ["age","address","gender","contact"]
		widgets = {
		"age":forms.NumberInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Enter Your age",
		}),
		"gender":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"address":forms.TextInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your Address",
			}),
		"contact":forms.NumberInput(attrs={
			"class":"form-control my-2",
			"placeholder":"Enter Your Contact",
			}),
		}


class AdminprofileForm(forms.ModelForm):
	class Meta:
		model = AdminProfile
		fields = ["age","gender"]
		widgets = {
		"age":forms.NumberInput(attrs={
		"class":"form-control my-2",
		"placeholder":"Enter Your age",
		}),
		"gender":forms.Select(attrs={
			"class":"form-control my-2",
			})
		}


class adminroleupdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","License","role_type"]
		widgets = {
		"username":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readonly":True,
			}),
		"License":forms.TextInput(attrs={
			"class":"form-control my-2",
			"readonly":True,
			}),
		"role_type":forms.NumberInput(attrs={
			"class":"form-control my-2",
			})
		}


class ChgPwdForm(PasswordChangeForm):
	old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Old Password"}))
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter New Password"}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control my-2","placeholder":"Enter Confirm New Password"}))
	class Meta:
		model = User
		fields = ["old_password","new_password1","new_password2"]

class tripsform(forms.ModelForm):
	class Meta:
		model = trips
		fields = ["Departure", "Destination"]
		widgets = {
		"Departure":forms.Select(attrs={
			"class":"form-control my-2",
			}),
		"Destination":forms.Select(attrs={
			"class":"form-control my-2",
			})
		}

class admintripsform(forms.ModelForm):
	class Meta:
		model = trips
		fields = ["status", "Drivername"]
		widgets = {
			"status":forms.Select(attrs={
				"class":"form-control my-2"
				}),
			"Drivername":forms.TextInput(attrs={
				"class":"form-control my-2",
				"placeholder":"Enter the Driver_Username Correctly"
				})
		}