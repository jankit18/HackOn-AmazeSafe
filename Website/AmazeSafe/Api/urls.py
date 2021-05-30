from django.urls import path,include
from . import views

# List of all existing api urls end-points of the project

urlpatterns = [
     path('',views.apiOverview,name='apiView'),
     path('selectMode/',views.registerUserMode,name='userMode'),
     path('openBox/<int:deliveryId>',views.boxOpenRequest,name='openBox'),
     path('openSanitize/',views.openSanitizeRequest,name='openSanitize'),
     path('checkThreat/',views.checkThreat,name='checkThreat'),
      path('apiOverview/',views.apiOverview,name='apiOverview')
]
     