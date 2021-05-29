import requests
from django.shortcuts import render

from rest_framework.decorators import api_view
from  rest_framework.response import Response

from .serializers import userInfoSerializer
from AppHome.models import AmazeWarriorsOrders, AmazeUsersOrders, UserInfo


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
        serializer = userInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response("Success")
    except:    
        return Response("Failure")


@login_required
@api_view(['POST'])
def boxOpenRequest(request, deliveryId):
    try:
        amazeWarriorObj = AmazeWarriorsOrders.objects.get(id = deliveryId)
        
        assignedClient = UserInfo.objects.get(userInstance = amazeWarriorObj.userInstance)

        adafruitToken = assignedClient.adafruitToken
        adafruitUserName = assignedClient.adafruitUserName

        '''
        url = 'https://io.adafruit.com/api/v2/'+adafruitUserName+'/feeds/open/data'
        dataObj = {"value":"open"} # Put value which you want to store
        requests.post(url, data = dataObj, headers = {"X-AIO-Key": adafruitToken})
        '''

        amazeWarriorObj.userInstance.orderStatus= "Delivered"
        amazeWarriorObj.userInstance.save()

        return Response("Success")
    except:
        return Response("Failure")    

   