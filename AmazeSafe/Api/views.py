from django.shortcuts import render

from rest_framework.decorators import api_view
from  rest_framework.response import Response

from .serializers import xyz

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
