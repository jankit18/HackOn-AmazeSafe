from django.urls import path,include
from . import views
urlpatterns = [
     path('',views.loginHome, name="loginHome"),
     path('category/',views.distinguishUser, name="selectUser"),
     path('amaze-warrior/',views.warriorRequest, name="amazeWarrior"),
     path('amaze-user/',views.clientRequest, name="amazeUser"),
     path('amaze-user/threat/',views.threatRequest, name="threat"),
]