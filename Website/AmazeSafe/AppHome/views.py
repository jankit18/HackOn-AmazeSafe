from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import userInfo, AmazeUsersOrders, AmazeWarriorsOrders

def loginHome(request):
    return render(request, 'index.html')

@login_required
def distinguishUser(request):
    userObj = User.objects.filter(userId=request.user)
    if len(userObj)==0:
        return render(request,'choicePage.html')
    else:
        if userObj.userMode == 'D':
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
                "outforDeliveryOrders": data
            }
            
            return render(request,'amazeWarriorPage.html',context)   
        elif userObj.userMode == 'U':
            orderObj = AmazeUsersOrders.objects.filter(userInstance = request.user)
            oFD = []
            delivered = []
            Fdeliveries = []

            for i in warriorOrdersObj:
            
                data ={
                    "name" : i.orderName,
                    "contact" : i.contact,
                    "status" : i.orderStatus,
                }

                if (y.orderStatus=="Delivered"):
                    delivered.push(data)
                elif (y.orderStatus=="OutForDelivery"):  
                    oFD.push(data)
                else:
                    Fdeliveries.push(data)    
                x.push(data)

            context = {
                "ofd" : oFD,
                "d" : delivered,
                "fd" : Fdeliveries
            }
            return render(request,'amazeUserPage.html',context)