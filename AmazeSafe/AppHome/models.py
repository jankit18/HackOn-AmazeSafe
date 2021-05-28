from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model):
    userId =  models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    userMode = models.CharField(max_length=1) 

    def __str__(self):
        return self.name+" "+str(self.user_id)


class AmazeUsersOrders(models.Models):
    userId = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    orderName = models.CharField(max_length = 500)
    orderAddress = models.CharField(max_length = 1000)
    orderCost = models.FloatField()
    orderStatus = models.CharField(max_length = 100)
    orderOtp = models.IntegerField()
    contact = models.IntegerField()

    def __str__(self):
        return "Order Name:" + self.orderName + ", user id: " + str(self.user_id)


class AmazeWarriorsOrders(models.Model):
    userId = models.ForeignKey( User, null = True, on_delete = models.SET_NULL)
    orderId = models.ForeignKey(AmazeUsersOrders, null = True, on_delete = models.SET_NULL)
    