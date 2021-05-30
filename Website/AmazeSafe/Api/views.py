import requests
from django.shortcuts import render

from rest_framework.decorators import api_view
from  rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from .serializers import userInfoSerializer
from AppHome.models import AmazeWarriorsOrders, AmazeUsersOrders, UserInfo
import json

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'bookDetail':'/bookDetail/',
        'syllabusDetail' : '/syllabusDetail/<int:pk>/',
        'ppDetail' : '/ppDetail/',
        'departSubDetail' : '/departSubDetail/<int:pk>/',
        'subTopicDetail' : '/subTopDetail/<int:pk>/',
        'topVidDetail' : '/'
    }
    return Response(api_urls)


@login_required
@api_view(['POST'])
def registerUserMode(request):
    try:
        print(request.data)
        UserInfo.objects.create(userInstance = request.user, userMode = request.data["userMode"], adafruitToken=request.data["adafruitToken"], adafruitUserName=request.data["adafruitUserName"])
        
        print("Mode Success")
        return Response("Success")
    except:    
        print("Mode failure")
        return Response("Failure")


@login_required
@api_view(['GET'])
def boxOpenRequest(request, deliveryId):
    try:
        amazeWarriorObj = AmazeWarriorsOrders.objects.get(id = deliveryId)
        
        assignedClient = UserInfo.objects.get(userInstance = amazeWarriorObj.userInstance)

        ADAFRUIT_IO_USERNAME = assignedClient.adafruitUserName
        ADAFRUIT_IO_KEY = assignedClient.adafruitToken
        

        url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/receive-esp/data'  #end poin to get last data
        
        d = {"open": True, "sanitize": False,"delivered": True}

        dataObj = {"value": json.dumps(d)}

        x = requests.post(url, json = dataObj, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})

       
        amazeWarriorObj.orderId.orderStatus= "Delivered"
        amazeWarriorObj.orderId.save()

        return Response("Success")
    except:
        return Response("Failure")    


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

        return Response("Success")
    except:
        return Response("Failure")    


@login_required
@api_view(['GET'])
def checkThreat(request):
    try:
        userObj =  UserInfo.objects.get(userInstance = request.user)
        ADAFRUIT_IO_USERNAME = userObj.adafruitUserName
        ADAFRUIT_IO_KEY = userObj.adafruitToken
        

        url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/send-esp/data/last' 
        x = requests.get(url, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})
        x = x.json()
        y =json.loads(x["value"])

        if(y['ALARM']==True):
            print("Alarm: On")
            return Response("1")
        else:
            print("Alarm: Off")
            return Response("0") 
    except:
        return Response("Failure")    

