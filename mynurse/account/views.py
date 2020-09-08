from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMessage
from django.core.mail.backends import smtp
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg.utils import swagger_auto_schema

from .serializers import UserSerializer
from .permissions import IsMeOrReadOnly
from .models import User, EmailCheck

from newsletters.models import Tag, NewsLetter

from django.contrib.auth.hashers import check_password
from django.contrib.auth import settings

import random
import json
import codecs

EMAIL_MESSAGE = '마들렌은 읽고싶은 뉴스레터를 추천해줘요.\n 책 읽기 대신 뉴스레터 읽기의 시대, 마들렌과 함께 시작해봐요.\n 이메일 인증번호: '
# Create your views here.
@api_view(['POST'])
def get_user(request, format=None):
    username = request.data['username']
    queryset = User.objects.all()
    try:
        user = get_object_or_404(queryset, username=username)
        tags = []

        for tag in user.like_tags.all():
            image = str(tag.image)
            if image[0] != '/':
                image = '/' + image
            tags.append({
                'tag_pk'    : tag.id,
                'tag_name'  : tag.name,
                'tag_image' : request.build_absolute_uri('/media' + image)
            })
        subscribes = []

        for sub in user.subscribes.all():
            newsletter_tags = []
            for tag in sub.tags.all():
                image = str(tag.image)
                if image[0] != '/':
                    image = '/' + image
                newsletter_tags.append({
                    'tag_pk'    : tag.id,
                    'tag_name'  : tag.name,
                    'tag_image' : request.build_absolute_uri('/media' + image)
                })
            image = str(sub.image)
            if image[0] != '/':
                image = '/' + image
            subscribes.append({
                'newsletter_pk'         : sub.id,
                'newsletter_name'       : sub.newsletter_name,
                'newsletter_image'      : request.build_absolute_uri('/media' + image),
                'register_url'          : sub.register_url,
                'newsletter_explain'    : sub.explain,
                'newsletter_tags'       : newsletter_tags
            })
        user_info = {
            'pk'        : user.id,
            'username'  : user.username,
            'birth'     : user.birth,
            'gender'    : user.gender,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'like_tags' : tags,
            'subscribes': subscribes
        }
    except:
        status = 'E00'
        message = 'user info fail'
        value = ''
        response = {
            'status'    : status,
            'message'   : message,
            'value'     : value
        }
        return Response(response)

    response = {
        'status'    : 'S00',
        'message'   : 'user info success',
        'value'     : user_info
    }
    return Response(response)

@api_view(['POST'])
def create_user(request, format=None):
    try:
        username = request.data['username']
        try: 
            user = User.objects.get(username=username)
            response = {
                'status'    : 'E00',
                'message'   : 'Username Already Exist',
                'value'     : username
            }
            return Response(response)
        except:
            pass
        password = request.data['password']
        birth = request.data['birth']
        gender = request.data['gender']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        # User.objects.create_user(username=username, password=password, birth=birth, gender=gender, first_name=first_name, last_name=last_name)
    
        user = User(
            username=username,
            birth=birth,
            gender=gender,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
    
        status = 'S00'
        message = 'User Create Success'
        value = ''

    except:
        status = 'E00'
        message = 'User NOT Created'
        value = ''
    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    return Response(response)

@api_view(['POST'])
def update_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username,password=password)
    if user is None:
        response = {
            'stutus'    : 'E00',
            'message'   : 'Wrong username or password',
            'value'     : ''
        }
        return Response(response)
    try:
        birth = request.data['birth']
        user.birth = birth
    except:
        pass
    try:
        gender = request.data['gender']
        user.gender = gender
    except:
        pass
    try:
        first_name = request.data['first_name']
        user.first_name = first_name
    except:
        pass
    try:
        last_name = request.data['last_name']
        user.last_name = last_name
    except:
        pass
    try:
        new_password = request.data['new_password']
        user.set_password(new_password)
        user.save()
    except:
        pass
    response = {
        'status'    : 'S00',
        'message'   : 'User UPDATE Success',
        'value'     : {
            'username'      : user.username,
            'password'      : user.password,
            'gender'        : user.gender,
            'birth'         : user.birth,
            'first_name'    : user.first_name,
            'last_name'     : user.last_name
        }
    }
    return Response(response)

@api_view(['POST'])
def find_username(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    birth = request.data['birth']

    try:
        user = User.objects.get(first_name=first_name, last_name=last_name, birth=birth)
    
        status = 'S00'
        message = '유저 아이디입니다.'
        value = user.username
    except:
        status = 'E00'
        message = '잘못된 사용자 정보입니다.'
        value  = ''

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def change_password(request):
    username = request.data['username']
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    new_password = request.data['new_password']
    
    try:
        user = User.objects.get(username=username)

        user.set_password(new_password)
        user.save()

        status = 'S00'
        message = 'PUT User Password'
        value = ''
    except:
        status = 'E00'
        message = 'FAIL PUT User Password'
        value = ''

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : ''
    }

    return Response(response)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = [permissions.AllowAny, IsMeOrReadOnly, ]

@api_view(['POST'])
def mail(request):
    try:
        email = request.data['username']
        print(type(email))
        if email == '':
            response = {
                'status' : 'E00',
                'message' : 'Email is Empty',
                'value' : ''
            }
            return Response(response)
    except:
        response = {
            'status': 'E00',
            'message' : 'there is no username field',
            'value' : ''
        }
        return Response(response)
        
    email_auth = random.randint(100000,999999)
    print(email_auth)
    try:    
        check = EmailCheck.objects.get(email=email)
        check.delete()
    except:
        pass
    
    check = EmailCheck.objects.create(email=email, check_number=str(email_auth))    
    '''
    print(render(None, 'message.html', {'email_auth':email_auth}).content)

    msg = EmailMessage(
        subject='[마들렌] 인증 메일입니다.',
        #body = codecs.open('./account/message.html').read(),
        body = 'message.html',
        from_email = 'hahoh0013@gmail.com',
        to = [email],
    )
    # msg.attach_file('./media/madeleine/logo.png')
    msg.content_subtype = "html"
    msg.send()
    '''
    try:
        print(email)
        send_mail(
            subject='[마들렌] 인증 메일입니다.',
            message=EMAIL_MESSAGE + str(email_auth),
            from_email='hahoh0013@gmail.com',
            recipient_list=[email,],
        )
        status = 'S00'
        message = 'Mail Success'
        value = ''
    except:
        status = 'E00'
        message = 'Mail Fail'
        value = ''
    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    
    return Response(response)

@api_view(['POST'])
def confirm_mail(request):
    username = request.data['username']
    try:
        check = EmailCheck.objects.get(email=username)
    except:
        response = {
            'status'    : 'E00',
            'message'   : '잘못된 사용자 입니다.',
            'value'     : ''
        }
        return Response(response)
        
    email_check = request.data['email_check']
    print(check.check_number, email_check)

    if check.check_number != email_check:
        status = 'E00'
        message = '잘못된 인증번호입니다.'
        value = ''
    else :
        status = 'S00'
        message = '이메일 인증 성공'
        value = ''
        check.delete()

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def profile(request):
    try:
        user = User.objects.get(username=request)
        status = 'S00'
        message = 'login success'
        value = {
            'pk' : user.id,
            'username'  : user.username,
            'birth'     : user.birth,
            'gender'    : user.gender,
            'first_name': user.first_name,
            'last_name' : user.last_name
        }
    except:
        status = 'E00'
        message = 'login error'
        value = ''

    response = {
        'status' : status,
        'message' : message,
        'value' : value
    }
    
    return Response(response)


@api_view(['POST'])
def login_view(request):
    username = request.data['username']
    password = request.data['password']
    
    # user = authenticate(username=username, password=password)
    try:
        user = User.objects.get(username=username)
    except:
        response = {
            'status'    : 'E00',
            'message'   : '잘못된 아이디 또는 비밀번호입니다.',
            'value'     : {
                'pk' : -1,
                'username'  : '',
                'birth'     : '',
                'gender'    : True,
                'first_name': '',
                'last_name' : ''
            }
        }
        return Response(response)

    if user.check_password(password):
        login(request, user)
        status = 'S00'
        message = 'login success'
        value = {
            'pk' : user.id,
            'username'  : user.username,
            'birth'     : user.birth,
            'gender'    : user.gender,
            'first_name': user.first_name,
            'last_name' : user.last_name
        }
    else:
        status = 'E00'
        message = '잘못된 아이디 또는 비밀번호입니다.'
        value = {
            'pk' : -1,
            'username'  : '',
            'birth'     : '',
            'gender'    : True,
            'first_name': '',
            'last_name' : ''
        }

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def register_like_tags(request):
    username = request.data['username']

    user = User.objects.get(username=username) 
    try:
        user.like_tags.clear()
    except:
        pass
    print(request.data['tags'])
    try:
        tags = json.loads(request.data['tags'])
        print(tags)
        #tag_queryset = Tag.objects.all()
        for tag in tags['value']:
            t = Tag.objects.get(id=tag)
            user.like_tags.add(t)
        status = 'S00'
        message = 'Register Like Tag Success'
        value = ''
    except:
        status = 'E00'
        message = 'Wrong Tags'
        value = ''

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    return Response(response)

@api_view(['POST'])
def delete_like_tags(request):
    username = request.data['username']
    targets = json.loads(request.data['delete_tags'])['value']

    user = User.objects.get(username=username)
    for target in targets:
        tag = Tag.objects.get(id=target)
        user.like_tags.remove(tag)
    response = {
        'status'    : 'S00',
        'message'   : 'Delete Like Tags',
        'value'     : ''
    }
    return Response(response)



@api_view(['POST'])
def get_subscribes(request):
    username = request.data['username']
    
    user = User.objects.get(username=username)
    try:
        subscribes = user.subscribes
    except:
        status = 'E00'
        message = 'NO Subscribe'
        value = ''

        response = {
            'status'    : status,
            'message'   : message,
            'value'     : value
        }

        return Response(response)

    subscribe_list = []
    print(subscribes)
    
    for subscribe in subscribes.all():
        pk = subscribe.id
        newsletter_name = subscribe.newsletter_name
        explain = subscribe.explain
        register_url = subscribe.register_url
        tags = []
        for tag in subscribe.tags.all():
            image = str(tag.image)
            if image[0] != '/':
                image = '/' + image
            tags.append({
                'tag_pk'    : tag.id,
                'tag_name'  : tag.name,
                'tag_image' : request.build_absolute_uri('/media'+image)
            })
        image = str(subscribe.image)
        if image[0] != '/':
            image = '/' + image
        subscribe_list.append({
            'newsletter_pk'         : pk,
            'newsletter_name'       : newsletter_name,
            'newsletter_image'      : request.build_absolute_uri('/media'+image),
            'register_url'          : register_url,
            'newsletter_explain'    : explain,
            'newsletter_tags'       : tags
        })

    status = 'S00'
    message = 'GET Subscribes'
    value = subscribe_list

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def get_tag_recommend(request):
    username = request.data['username']
    user = User.objects.get(username=username)
    # flag = request.data['flag']
    
    try:
        newsletters = NewsLetter.objects.filter(tags__in=user.like_tags.all()).order_by('?')
    except:
        newsletters = NewsLetter.objects.all().order_by('?')
    
    values = []
    for newsletter in newsletters.all():
        tags = []
        for tag in newsletter.tags.all():
            image = str(tag.image)
            if image[0] != '/':
                image = '/' + image
            tags.append({
                'tag_pk'    : tag.id,
                'tag_name'  : tag.name,
                'tag_image' : request.build_absolute_uri('/media' + image)
            })

        image = str(newsletter.image)
        if image[0] != '/':
            image = '/' + image
        value = {
            'newsletter_pk'        : newsletter.id,
            'newsletter_name'   : newsletter.newsletter_name,
            'newsletter_image'  : request.build_absolute_uri('/media' + image),
            'register_url'      : newsletter.register_url,
            'newsletter_explain'   : newsletter.explain,
            'newsletter_tags'      : tags
        }
        values.append(value)
    
    #random.shuffle(values)

    response = {
        'status'    : 'S00',
        'message'   : 'GET Recommand Newsletters',
        'value'     : values
    }
    
    return Response(response)

@api_view(['POST'])
def subscribe_register(request):
    username = request.data['username']

    user = User.objects.get(username=username)

    newsletters = json.loads(request.data['newsletter_pk'])
    values = []
    for letter in newsletters['value']:
        newsletter = NewsLetter.objects.get(id=letter)
        subscribes = user.subscribes.all()
        
        if newsletter in subscribes:
            response = {
                'status'    : 'E00',
                'message'   :    'Already Subscribing',
                'value'     : ''
            }
            return Response(response)
    
        user.subscribes.add(newsletter)
        newsletter.followers += 1
        newsletter.save()
        tags = []
        for tag in newsletter.tags.all():
            image = str(tag.image)
            if image[0] != '/':
                image = '/' + image
            tags.append({
                'tag_pk'    : tag.id,
                'tag_name'  : tag.name,
                'tag_image' : request.build_absolute_uri('/medai' + image)
            })

        image = str(newsletter.image)
        if image[0] != '/':
            image = '/' + image
        values.append({
            'newsletter_pk'         : newsletter.id,
            'newsletter_name'       : newsletter.newsletter_name,
            'newsletter_explain'    : newsletter.explain,
            'newsletter_image'      : request.build_absolute_uri('/media' + image),
            'register_url'          : newsletter.register_url,
            'newsletter_tags'  : tags
        })


    response = {
        'status'    : 'S00',
        'message'   : 'Subscribe Register Success',
        'value'     : values
    }

    return Response(response)

@api_view(['POST'])
def subscribe_remove(request):
    username = request.data['username']
    user = User.objects.get(username=username)

    newsletters = json.loads(request.data['newsletter_pk'])['value']
    try:
        for newsletter in newsletters:
            newsletter = NewsLetter.objects.get(id=newsletter)
            user.subscribes.remove(newsletter)
            newsletter.followers -= 1
            newsletter.save()

        status = 'S00'
        message = 'DELETE Subscribe'
        value = ''
    except:
        status  = 'E00'
        message = 'FAIL'
        value = ''

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    return Response(response)

