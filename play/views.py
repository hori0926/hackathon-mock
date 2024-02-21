from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from play.models import PlaySetting, Client

# Create your views here.
#　ここにやること書いてく
#　django-channelのインストール
#　redisのインストール
#　django-channelの設定 routing consumer等



class Setting(APIView):
    PlaySetting.objects.create(
        difficulty=1,
        client=Client.objects.get(pk=1)
    )