from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('main',views.main),
    path('register',views.register),
    path('login',views.login),
    path('travels',views.travels),
    path('logout', views.logout),
    path('travels/add',views.add),
    path('travels/add/addtravel',views.addtravel),
    path('travels/destination/<int:id>',views.destination),
    path('travels/destination/<int:id>/join',views.join),


]