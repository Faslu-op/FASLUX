from django.urls import path
from .import views
app_name = 'users'
urlpatterns=[
    path('userregister/',views.userRegister,name='UserRegister'),
    # path('login/',views.login,name='Login'),
    path('login/',views.userLogin,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile_form,name='profile'),
    path('profiledetails/',views.profile,name='profiledetails'),


]