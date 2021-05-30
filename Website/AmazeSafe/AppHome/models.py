from django.db import models
from django.contrib.auth.models import User
import datetime


# User informtion model to store the user credentials and mode
# Amaze-User : User at Amazon (userMode: U)
# Amaze-Warrior : Delivery Person at Amazon  (userMode: D)

class UserInfo(models.Model):
    userInstance =  models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    userMode = models.CharField(max_length=1) 
    adafruitToken = models.CharField(max_length = 1000,default = "")
    adafruitUserName = models.CharField(max_length = 1000,default = "")

    def __str__(self):
        return self.adafruitUserName+" "+str(self.userMode)



# Amaze-user and order relation model
# Having One-Many relation with User

class AmazeUsersOrders(models.Model):
    d = datetime.date(1997, 10, 19)
    userInstance = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    orderId = models.IntegerField(default=0)
    orderDate = models.DateField(default=d)
    orderName = models.CharField(max_length = 500)
    orderAddress = models.CharField(max_length = 1000)
    orderCost = models.FloatField()
    orderStatus = models.CharField(max_length = 100)
    orderOtp = models.IntegerField()
    contact = models.IntegerField()


    def __str__(self):
        return "Order Name:" + self.orderName + ", contact: " + str(self.contact)


# Amaze-warrior and order relation model
# Having One-To-One relation between Order id and Product id
# and One-Many relation with User

class AmazeWarriorsOrders(models.Model):
    userInstance = models.ForeignKey( User, null = True, on_delete = models.SET_NULL)
    orderId = models.OneToOneField(AmazeUsersOrders, null = True, on_delete = models.SET_NULL)

    def __str__(self):
        return str(self.orderId.contact)
    