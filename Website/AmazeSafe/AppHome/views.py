from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserInfo, AmazeUsersOrders, AmazeWarriorsOrders
from django.utils.safestring import SafeString
import requests
import json


# fuction receive request for login Page 
def loginHome(request):
    return render(request, 'index.html')


# fuction receive request for distinguishing page
# perform dinstinct action based on Usermode 
@login_required
def distinguishUser(request):
    userObj = UserInfo.objects.filter(userInstance=request.user)
    if len(userObj)==0:
        context={
            "userInstance": request.user
        }
        return render(request,'choicePage.html',context)
    else:
        if userObj[0].userMode == 'D':
            return     redirect('amazeWarrior')
        elif userObj[0].userMode == 'U':
           return      redirect('amazeUser')
        
            
# fuction receive request for Amaze-Warrior Page 
# show different different states of order assigned to him/her

@login_required
def warriorRequest(request):
    warriorOrdersObj = AmazeWarriorsOrders.objects.filter(userInstance = request.user)
    x = []
    z = []
    print(warriorOrdersObj)
    for i in warriorOrdersObj:
        print(i)
        y = i.orderId
        print(y)
        if(y.orderStatus=="OutForDelivery"):
            data ={
                "address" : y.orderAddress,
                "contact" : y.contact,
                "status" : y.orderStatus,
                "deliveryId": i.id,
                "orderDate":str(y.orderDate)
            }
            x.append(data)
        elif (y.orderStatus=="Delivered"): 
            data ={
                "address" : y.orderAddress,
                "contact" : y.contact,
                "status" : y.orderStatus,
                "deliveryId": i.id,
                "orderDate":str(y.orderDate)
            }
            z.append(data)

    context = {
        "outForDeliveries":SafeString(x),
        "previousDeliveries": SafeString(z)
    }
    
    return render(request,'amazeWarriorPage.html',context) 


# fuction receive request for Aamze-User Page
#  show different different states of order purchased by him/her


@login_required
def clientRequest(request):      
    clientOrdersObj = AmazeUsersOrders.objects.filter(userInstance = request.user)
    ordersInBox = []
    outForDeliveries = []
    incomingDeliveries = []
    previousDeliveries = []

    for i in clientOrdersObj:
    
        data ={
            "orderId": i.orderId,
            "orderName" : i.orderName,
            "orderCost": i.orderCost,
            "contact" : i.contact,
            "orderStatus" : i.orderStatus,
            "orderDate": str(i.orderDate)
        }

        if (i.orderStatus=="InBox"):
            ordersInBox.append(data)
        elif (i.orderStatus=="OutForDelivery"):  
            outForDeliveries.append(data)
        elif (i.orderStatus=="FutureOrder"):
            incomingDeliveries.append(data)   
        else:
            previousDeliveries.append(data)     
        
    context = {
        "ordersInBox" : SafeString(ordersInBox),
        "outForDeliveries" : SafeString(outForDeliveries),
        "incomingDeliveries" : SafeString(incomingDeliveries),
        "previousDeliveries" : SafeString(previousDeliveries)
    }
    return render(request,'amazeUserPage.html',context)

# Function which will receive request after any possible Alert
# show GPS coordinate, SnapShot of the Situation
# also send message to connected neighbour

@login_required
def threatRequest(request): 
    userObj = UserInfo.objects.get(userInstance=request.user)
    ADAFRUIT_IO_USERNAME = userObj.adafruitUserName
    ADAFRUIT_IO_KEY = userObj.adafruitToken

    url = 'https://io.adafruit.com/api/v2/'+ADAFRUIT_IO_USERNAME+'/feeds/send-esp/data/last' 
    x = requests.get(url, headers = {"X-AIO-Key": ADAFRUIT_IO_KEY})
    x = x.json()
    try:
        y =json.loads(x["value"])
        
        context = {
            "imageMatrix": y["IMAGE"],
            "gpsCoordinate": y["GPS"],
            "boxTemperature": y["TEMPERATURE"],
            "alarmStatus": y["ALARM"],
            "lastUpdate": x["updated_at"]
        }
        
        return render(request,'threatPage.html',context)
    except:
        messages.warning(request, 'Cannot Investigate Threat.. Incorrect Credential')  
        return redirect('amazeUser')
          

    
# function to be triggered for User Log-Out

@login_required
def userLogout(request):
    logout(request)
    #messages.success(request, 'You have been Logged Out successfully.')
    return redirect('loginHome')