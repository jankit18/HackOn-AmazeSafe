from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserInfo, AmazeUsersOrders, AmazeWarriorsOrders

def loginHome(request):
    return render(request, 'index.html')

@login_required
def distinguishUser(request):
    userObj = User.objects.filter(userId=request.user)
    if len(userObj)==0:
        return render(request,'choicePage.html')
    else:
        if userObj.userMode == 'D':
            redirect('warriorRequest')
        elif userObj.userMode == 'U':
            redirect('clientRequest')
            

@login_required
def warriorRequest(request):
    warriorOrdersObj = AmazeWarriorsOrders.objects.filter(userInstance = request.user)
    x = []
    for i in warriorOrdersObj:
        y = i.orderId
        data ={
            "address" : y.orderAddress,
            "contact" : y.contact,
            "status" : y.orderStatus,
            "id": i.id
        }
        x.push(data)

    context = {
        "outforDeliveryOrders":x
    }
    
    return render(request,'amazeWarriorPage.html',context) 



@login_required
def clientRequest(request):      
    clientOrdersObj = AmazeUsersOrders.objects.filter(userInstance = request.user)
    oFD = []
    delivered = []
    Fdeliveries = []

    for i in clientOrdersObj:
    
        data ={
            "name" : i.orderName,
            "contact" : i.contact,
            "status" : i.orderStatus,
        }

        if (i.orderStatus=="Delivered"):
            delivered.push(data)
        elif (i.orderStatus=="OutForDelivery"):  
            oFD.push(data)
        else:
            Fdeliveries.push(data)    
        
    context = {
        "ofd" : oFD,
        "d" : delivered,
        "fd" : Fdeliveries
    }
    return render(request,'amazeUserPage.html',context)