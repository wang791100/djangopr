# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from models import PurchaseType,Purchase
import requests
import json

from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from models import jiangpin, User
from django.http import JsonResponse


# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'index.html', {})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(username=username, password=password)
        if user_obj:
            print(username, password)
            request.session['username'] = request.POST.get('username')
            auth.login(request, user_obj)
            return redirect('/')
        else:
            print('error')
            msg = '账号或密码不正确请重新输入'
            return render(request, 'login.html',
                          {'msg': msg})  ##return HttpResponse(json.dumps({'code': 403, 'status': '用户名密码错误！'}))
    return render(request, 'login.html', {})


def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect('/')


def zhuce(request):
    if request.method == 'POST':
        username = request.POST.get('zc_username')
        password = request.POST.get('zc_password')
        phone = request.POST.get('zc_phone')
        email = request.POST.get('zc_email')
        if username == '':
            msg = '请输入用户名密码'
            return render(request, 'zhuce.html', {'msg': msg})
        elif password == '':
            msg = '请输入用户名密码'
            return render(request, 'zhuce.html', {'msg': msg})
        elif phone == '':
            msg = '请输入联系方式'
            return render(request, 'zhuce.html', {'msg': msg})
        elif email == '':
            msg = '请输入电子邮件'
            return render(request, 'zhuce.html', {'msg': msg})
        user = User.objects.filter(username=username)
        if user:
            msg = '已存在用户'
            return render(request, 'zhuce.html', {'msg': msg})
        else:
            User.objects.create(username=username, password=make_password(password), phone=phone, email=email, count=10,
                                time=1)
            msg = '注册成功..自动登录中'
            user_obj = authenticate(username=username, password=password)
            request.session['username'] = request.POST.get('username')
            auth.login(request, user_obj)
            return render(request, 'zhuce.html', {'msg': msg, 'pass': 1})
    return render(request, 'zhuce.html', {})


def error(request):
    return render(request, 'error.html', {})


@csrf_exempt
def home(request):
    # api_request = requests.get('https://api.github.com/users?since=0')
    # api = json.loads(api_request.content)
    return render(request, 'home.html', {})


@login_required(login_url='/error/')
def choujiang(request):
    count = request.user.count
    if request.method == 'POST':
        jpdc = request.body
        name = json.loads(jpdc)['JP']
        print(name)
        count = request.user.count
        # if count < 10:
        #     return HttpResponse(json.dumps({'code': 30001}))
        if len(name.split(',')) != 1:
            for i in name.split(','):
                us = request.user
                jp = jiangpin()
                jp.user = us
                jp.name = i
                jp.save()
                count -= 1
                us = User.objects.get(username=request.user.username)
                us.count = count
                us.save()
        else:
            us = request.user
            jp = jiangpin()
            jp.user = us
            jp.name = name
            jp.save()
            count -= 1
            us = User.objects.get(username=request.user.username)
            us.count = count
            us.save()
        count = request.user.count
        return render(request, 'choujiang.html', {'count': count})
    else:
        return render(request, 'choujiang.html', {'count': count})


@csrf_exempt
def user(request):
    user = request.POST["user"]
    user_request = requests.get('https://api.github.com/' + user)
    api_user = json.loads(user_request.content)
    return render(request, 'user.html', {'user': api_user})


@login_required(login_url='/error/')
def chongzhi(request):
    time = request.user.time
    if request.method == 'POST':
        time = request.user.time
        if time != 0 or request.user.username == 'chengyuanyan':
            count_json = request.body
            count = json.loads(count_json)['count']
            us = User.objects.get(username=request.user.username)
            us.count += count
            us.time -= 1
            us.save()

        return render(request, 'chongzhi.html', {'time': time})

    return render(request, 'chongzhi.html', {"time": time})


def manage(request):
    return render(request, 'manage.html', {})


def loadinfo(request):
    context = {}
    context['types'] = PurchaseType.objects.all()
    return context

def lists(request,page=1):
    goods = Purchase.objects.all()

    #分页
    paginator = Paginator(goods,per_page=9)
    try:
        goods = paginator.page(page)  # 获取指定页的商品记录
    except PageNotAnInteger:
        # 如果请求的页面不是证书,返回第一页.
        goods = paginator.page(1)
    except EmptyPage:
        # 如果请求的页面不在合法的页面范围内,返回结果的最后一页.
        goods = paginator.page(paginator.num_pages)
    except InvalidPage:
        # 如果请求的页面不存在,重定向页面.
        raise Http404('请求的页面不存在')
        # return HttpResponse('找不到页面的内容')


    return render(request,'list.html',context={'goods':goods,'paginator':paginator})

def detail(request,gid):
    context = loadinfo(request)
    ob = Purchase.objects.get(id=gid)
    ob.clicknum += 1
    ob.save()
    context['goods'] = ob

    return render(request,'detail.html',context)