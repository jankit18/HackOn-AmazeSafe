from django.urls import path,include
from . import views
urlpatterns = [
     path('mockTest/',views.landingPage, namme="landingPage")
]