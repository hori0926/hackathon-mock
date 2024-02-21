from django.db import models
from .constants import DifficultyChoice


class Client(models.Model):
    """クライアント"""
    class Meta:
        verbose_name = 'クライアント'
        verbose_name_plural = 'クライアント'

    id = models.AutoField(primary_key=True) # クライアントID
    #以下プレイヤーから見える情報
    name = models.CharField(max_length=30, unique=True) # クライアント名
    description = models.TextField(blank=True, null=True) # クライアント説明
    created_at = models.DateTimeField(auto_now_add=True) # 作成日時
    age = models.IntegerField(unique=False) # クライアント年齢
    occupation = models.CharField(max_length=30, unique=False) # クライアント職業
    position = models.CharField(max_length=30, unique=False) # クライアント役職
    #以下プレイヤーからは見えない情報
    hobby = models.CharField(max_length=30, unique=False) # クライアント趣味
    # もっと追加したい情報があれば追加してください
    

class PlaySetting(models.Model):
    """プレイ設定"""
    class Meta:
        verbose_name = 'プレイ設定'
        verbose_name_plural = 'プレイ設定'

    id = models.AutoField(primary_key=True) # プレイ設定ID
    name = models.CharField(max_length=30, unique=True) # プレイ設定名
    description = models.TextField(blank=True, null=True) # プレイ設定説明
    created_at = models.DateTimeField(auto_now_add=True) # 作成日時
    client = models.ForeignKey(Client, on_delete=models.CASCADE) # クライアント
    difficulty = models.IntegerField(choices=DifficultyChoice.choices) # 難易度
    
