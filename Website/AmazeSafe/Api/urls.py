from django.urls import path,include
from . import views
urlpatterns = [
     path('',views.apiOverview,name='apiView'),
     path('selectMode/',views.registerUserMode,name='userMode'),
     path('openBox/<int:deliveryId>',views.boxOpenRequest,name='openBox')
]