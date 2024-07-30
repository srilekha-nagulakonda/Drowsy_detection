from django.shortcuts import render, redirect
from . forms import UserForm, StaffprofileForm, DriverprofileForm, UserprofileForm, AdminprofileForm, adminroleupdateForm, updateprofileForm, adminupdateprofileForm, ChgPwdForm, tripsform, admintripsform
from . models import User, DriverProfile, StaffProfile, UserProfile, AdminProfile, trips, data_status, data_submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def register(request):
    if request.method == "POST":
        s = UserForm(request.POST)
        if s.is_valid():
            h = s.save(commit=False)
            messages.success(request,f"{h.username} User Created Successfully")
            h.save()
            return redirect('/login')
    s = UserForm()
    return render(request,"register.html",{'p':s})

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def updateprofile(request):
    ut = User.objects.get(id=request.user.id)
    if request.user.role_type == 0:
        s = UserProfile.objects.all()
        w = []
        for i in s:
            w.append(i.Users_id)
        if request.user.id not in w:
            if request.method == "POST":
                Stf = UserprofileForm(request.POST)
                Stf1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Stf.is_valid() and Stf1.is_valid():
                    q = Stf.save(commit=False)
                    q.status = 1
                    q.Users_id = request.user.id
                    q.save()
                    Stf1.save()
                    messages.success(request,"Profile Created Successful")
                    return redirect('/profile')
            Stf = UserprofileForm()
            Stf1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'g':Stf,'u':Stf1})
        else:
            ku = UserProfile.objects.get(Users_id=request.user.id)
            if request.method == "POST":
                Stf = UserprofileForm(request.POST,instance=ku)
                Stf1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Stf.is_valid():
                    Stf.save()
                    Stf1.save()
                    messages.info(request,'Profile Updated Successfully')
                    return redirect('/profile')
            Stf = UserprofileForm(instance=ku)
            Stf1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'hn':Stf,'u':Stf1})
    elif request.user.role_type == 1:
        x = DriverProfile.objects.all()
        mx = []
        for i in x:
            mx.append(i.Driver_id)
        if request.user.id not in mx:
            if request.method == "POST":
                Drv = DriverprofileForm(request.POST)
                Drv1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Drv.is_valid() and Drv1.is_valid():
                    t = Drv.save(commit=False)
                    t.status = 1
                    t.Driver_id = request.user.id
                    t.save()
                    Drv1.save()
                    messages.info(request,"Profile Created Successfully")
                    return redirect('/profile')
            Drv = DriverprofileForm()
            Drv1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'g':Drv,'u':Drv1})
        else:
            z = DriverProfile.objects.get(Driver_id=request.user.id)
            if request.method == "POST":
                Drv = DriverprofileForm(request.POST,instance=z)
                Drv1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Drv.is_valid() and Drv1.is_valid():
                    Drv.save()
                    Drv1.save()
                    messages.warning(request,"Profile Updated Successfully")
                    return redirect('/profile')
            Drv = DriverprofileForm(instance=z)
            Drv1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'hn':Drv,'u':Drv1})
    elif request.user.role_type == 2:
        s = StaffProfile.objects.all()
        w = []
        for i in s:
            w.append(i.Staff_id)
        if request.user.id not in w:
            if request.method == "POST":
                Stf = StaffprofileForm(request.POST)
                Stf1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Stf.is_valid() and Stf1.is_valid():
                    q = Stf.save(commit=False)
                    q.status = 1
                    q.Staff_id = request.user.id
                    q.save()
                    Stf1.save()
                    messages.success(request,"Profile Created Successful")
                    return redirect('/profile')
            Stf = StaffprofileForm()
            Stf1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'g':Stf,'u':Stf1})
        else:
            ku = StaffProfile.objects.get(Staff_id=request.user.id)
            if request.method == "POST":
                Stf = StaffprofileForm(request.POST,instance=ku)
                Stf1 = updateprofileForm(request.POST,request.FILES,instance=ut)
                if Stf.is_valid():
                    Stf.save()
                    Stf1.save()
                    messages.info(request,'Profile Updated Successfully')
                    return redirect('/profile')
            Stf = StaffprofileForm(instance=ku)
            Stf1 = updateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'hn':Stf,'u':Stf1})
    elif request.user.role_type == 3:
        x = AdminProfile.objects.all()
        mx = []
        for i in x:
            mx.append(i.Admin_id)
        if request.user.id not in mx:
            if request.method == "POST":
                Ad = AdminprofileForm(request.POST)
                Ad1 = adminupdateprofileForm(request.POST,request.FILES,instance=ut)
                if Ad.is_valid() and Ad1.is_valid():
                    t = Ad.save(commit=False)
                    t.status = 1
                    t.Admin_id = request.user.id
                    t.save()
                    Ad1.save()
                    messages.info(request,"Profile Created Successfully")
                    return redirect('/profile')
            Ad = AdminprofileForm()
            Ad1 = adminupdateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'g':Ad,'u':Ad1})
        else:
            z = AdminProfile.objects.get(Admin_id=request.user.id)
            if request.method == "POST":
                Ad = AdminprofileForm(request.POST,instance=z)
                Ad1 = adminupdateprofileForm(request.POST,request.FILES,instance=ut)
                if Ad.is_valid() and Ad1.is_valid():
                    Ad.save()
                    Ad1.save()
                    messages.warning(request,"Profile Updated Successfully")
                    return redirect('/profile')
            Ad = AdminprofileForm(instance=z)
            Ad1 = adminupdateprofileForm(instance=ut)
            return render(request,'updateprofile.html',{'hn':Ad,'u':Ad1})
    else:
        pass

@login_required
def adduser(request):
	g = User.objects.filter(is_superuser=0)
	if request.method == "POST":
		m = UserForm(request.POST)
		if m.is_valid():
			m.save()
			return redirect('/adduser')
	m = UserForm()
	return render(request,'adlist.html',{'k':m,'p':g})

@login_required
def aduserupdate(request,j):
	p = User.objects.get(id=j)
	if request.method == "POST":
		n = adminroleupdateForm(request.POST,instance=p)
		print(n)
		if n.is_valid():
			n.save()
			return redirect('/adduser')
	n = adminroleupdateForm(instance=p)
	return render(request,'adsupd.html',{'nk':n})

@login_required
def changepwd(request):
	if request.method == "POST":
		b = ChgPwdForm(user=request.user,data=request.POST)
		if b.is_valid():
			b.save()
			return redirect('/login')
	b = ChgPwdForm(user=request.user)
	return render(request,'changepwd.html',{'c':b})


@login_required
def viewtrips(request):
    ku = User.objects.get(id=request.user.id)
    if request.method == "POST":
        m = tripsform(request.POST)
        if m.is_valid():
            trip_instance = m.save(commit=False)
            trip_instance.Username = ku.username
            trip_instance.Trip_status = 0
            trip_instance.save()
            return redirect('/viewtrips')
    
    m = tripsform()
    y = trips.objects.all()
    return render(request, 'viewtrips.html', {'x': m, 'y': y})

@login_required
def edit_trip(request,j):
    p = trips.objects.get(Trip_ID=j)
    if request.method == "POST":
        n = admintripsform(request.POST,instance=p)
        n.Booking_Status = 1
        print(n)
        if n.is_valid():
            n.save()
            return redirect('/viewtrips')
    n = admintripsform(instance=p)
    return render(request,'view_trips.html',{'nk':n})

def completed(request):
    p = data_submit.objects.all()
    return render(request,'completed.html',{'k':p})