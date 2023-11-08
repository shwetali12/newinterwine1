from django.urls import path
from . import views

urlpatterns = [
   
   path('',views.home,name="home"),
   path('home/',views.home,name="home"),
   path('SignUp/',views.SignUp,name="SignUp"),
   path('SignIn',views.SignIn,name="SignIn"),
   path('logout/',views.logoutpage,name='logout'),
   path('create_offer/',views.create_offer,name='create_offer'),
   path('remove/<int:id>',views.remove,name='remove'),
   path('edit/<int:id>',views.edit,name='edit'),
   path('filter_offers/',views.filter_offers,name='filter_offers'),


]