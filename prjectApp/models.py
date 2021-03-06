# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import django.utils.timezone as timezone

# Create your models here.


class jiangpin(models.Model):
    name = models.CharField('奖品名称', max_length=30, blank=True, help_text='奖品名称')
    user = models.CharField('获奖者', max_length=20, blank=True, help_text='获奖人')
    date = models.DateTimeField('获奖时间', default=timezone.now)


class User(AbstractUser):
    count = models.IntegerField(verbose_name='抽奖次数', default=10)
    time = models.IntegerField(verbose_name='充值次数', default=1)
    phone = models.CharField(verbose_name='电话号码', max_length=15, null=False, default=12345678910)


class PurchaseType(models.Model):
    """产品类别"""
    name = models.CharField(u'产品类别', max_length=20, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '产品类别'

class Purchase(models.Model):
    """商品信息"""
    name = models.CharField(u'商品名称', max_length=30, blank=True)
    details = models.CharField('商品描述', max_length=50)
    price = models.FloatField('商品价格')
    number = models.IntegerField(verbose_name='剩余数量')
    clicknum = models.IntegerField('用户点击量',default=0)
    picname = models.ImageField(upload_to='static/img',verbose_name='商品图片',blank=True)
    type = models.ManyToManyField(PurchaseType,verbose_name='产品类型')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '商品信息'





class PurchaseColour(models.Model):
    """颜色"""
    colour = models.CharField('颜色', max_length=10, blank=True)
    purchase_colour = models.ManyToManyField(Purchase)


class PurchaseSKU(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    purchase_type = models.ForeignKey(PurchaseType, on_delete=models.CASCADE)
