from django.urls import path
from Face_Recognition import views
from django.contrib.auth import views as ad

urlpatterns = [
	path('',views.home,name="hm"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('register/',views.register,name="register"),
    path('login/',ad.LoginView.as_view(template_name='login.html'),name="login"),
    path('logout/',ad.LogoutView.as_view(template_name='logout.html'),name="logout"),
    path('profile/',views.profile,name="profile"),
	path('update/',views.updateprofile,name="update"),
	path('adduser/',views.adduser,name="adduser"),
	path('aduserupdate/<int:j>/',views.aduserupdate,name="aduserupdate"),
	path('changepwd/',views.changepwd,name="changepwd"),
	path('viewtrips/',views.viewtrips,name="view_trips"),
	path('edit_trip/<int:j>/',views.edit_trip,name="edit_trip"),
	path('completed/',views.completed,name="completed"),
	
]