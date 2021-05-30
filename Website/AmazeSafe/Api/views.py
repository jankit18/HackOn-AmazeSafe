# Response and request import
import requests
from django.shortcuts import render
from django.contrib import messages

# restframework imports
from rest_framework.decorators import api_view
from  rest_framework.response import Response

# login decorator import
from django.contrib.auth.decorators import login_required

# serializer class import
from .serializers import userInfoSerializer

# reqired models import 
from AppHome.models import AmazeWarriorsOrders, AmazeUsersOrders, UserInfo

import json


# Function to view all the existing..
# Api end-point available in this project.
# Use to resolve api calls, request type POST

@api_view(['GET'])
def apiOverview(request):

    # Api end-point available in this project
    api_urls = {
        'Select User Mode' : '/selectMode/',
        'Open Box Trigger' : '/penBox/<int:deliveryId>/',
        'Open box and Sanitise' : '/openSanitize/',
        'Check Possible Threat' : '/checkThreat/'
    }
    return Response(api_urls)



# Function to register user as the Amaze-user or Amaze-warrior
# Use to resolve api calls, request type POST

@login_required
@api_view(['POST'])
def registerUserMode(request):

  
    try:
        print(request.data)
        UserInfo.objects.create(userInstance = request.user, userMode = request.data["userMode"], adafruitToken=request.data["adafruitToken"], adafruitUserName=request.data["adafruitUserName"])
        return Response("Success")
    except:    
        print("Mode failure")
        return Response("Failure")
        


 # Function open box of the associated user box, triggred by Delivery Warriors
 # Use to resolve api calls, request type GET

@login_required
@api_view(['GET'])
def boxOpenRequest(request, deliveryId):

    try:
        amazeWarriorObj = AmazeWarriorsOrders.objects.get(id = deliveryId)
        assignedClient = UserInfo.objects.get(userInstance = amazeWarriorObj.userInstance)

        ADAFRUIT_IO_USERNAME = assignedClient.adafruitUserName
        ADAFRUIT_IO_KEY = assignedClient.adafruitToken
        
        url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/receive-esp/data'  #end poin to get last data
        data= {"open": True, "sanitize": False,"delivered": True}

        dataObj = {"value": json.dumps(data)}
        x = requests.post(url, json = dataObj, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})
    
        amazeWarriorObj.orderId.orderStatus= "Delivered"
        amazeWarriorObj.orderId.save()

        return Response("Success")
    except:
        messages.warning(request, 'Unable to open.. Invalid Credential at user end')
        return Response("Failure")    



 # Function to open box of the associated user box, 
 # triggred by amaze-user before collecting parcel
 # Use to resolve api calls, request type GET

@login_required
@api_view(['GET'])
def openSanitizeRequest(request):

    try:
        userObj =  UserInfo.objects.get(userInstance = request.user)
        ADAFRUIT_IO_USERNAME = userObj.adafruitUserName
        ADAFRUIT_IO_KEY = userObj.adafruitToken
        

        url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/receive-esp/data'  #end poin to get last data
        
        d = {"open": True, "sanitize": True,"delivered": False}

        dataObj = {"value": json.dumps(d)}

        x = requests.post(url, json = dataObj, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})
        print(x.status_code)
        if( x.status_code==404):
            messages.warning(request, 'Unable to open.. Invalid Adafruit Username and Key')
            return Response("Failure")    
        else:
            return Response("Success")
    except:
        messages.warning(request, 'Unable to open.. Invalid Adafruit Username and Key')
        return   Response("Failure")   



# Function to check whether there is a threat or not 
# using adafruit api-feed end-point
# Use to resolve api calls, request type GET

@login_required
@api_view(['GET'])
def checkThreat(request):

    # checking whether there is ant threat or not using adafruit feed end point

    try:
        userObj =  UserInfo.objects.get(userInstance = request.user)
        ADAFRUIT_IO_USERNAME = userObj.adafruitUserName
        ADAFRUIT_IO_KEY = userObj.adafruitToken
        

        url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/send-esp/data/last' 
        x = requests.get(url, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})
        x = x.json()
        
        try:
            y =json.loads(x["value"])

            if(y['ALARM']==True):
                print("Alarm: On")
                return Response("1")
            else:
                print("Alarm: Off")
                return Response("0") 
        except:    
            return Response("Failure")     
    except:
        return Response("Failure")    

