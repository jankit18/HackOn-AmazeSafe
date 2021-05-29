from rest_framework import serializers
from AppHome.models import UserInfo


class userInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

