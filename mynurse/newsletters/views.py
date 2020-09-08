# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import NewsLetterSerializer, TagSerializer, EpisodeSerializer
from .models import NewsLetter, Tag, Episode

from unicodedata import normalize
import pandas as pd
from PIL import Image
import json
import os
# Create your views here.
class NewsLetterViewSet(viewsets.ModelViewSet):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer

@api_view(['POST'])
def get_tags(request):
    queryset = Tag.objects.all()

    tags = []

    for query in queryset:
        pk = query.id
        name = query.name
        image = str(query.image)
        if image[0] != '/':
            image = '/' + image
        tags.append({
            'tag_pk'    : pk,
            'tag_name'  : name,
            'tag_image' : request.build_absolute_uri('/media' + image)
        })

    response = {
        'status'    : 'S00',
        'message'   : 'Success GET Tags',
        'value'     : tags
    }

    return Response(response)

@api_view(['POST'])
def search(request):
    query = request.data['query']
    if query == '':
        response = {
            'status'    : 'E00',
            'message'   : 'Empty Query',
            'value'     : ''
        }
        return Response(response)

    result_newsletters = []
    result_tags = []
    result_episodes = []
    
    try:
        newsletters = NewsLetter.objects.filter(newsletter_name__contains=query)
        tags = Tag.objects.filter(name__contains=query)
        episodes = Episode.objects.filter(title__contains=query)
    except:
        response = {
            'status'    : 'E00',
            'message'   : 'Empty Query',
            'value'     : ''
        }
        return Response(response)

    for tag in tags.all():
        image = str(tag.image)
        if image[0] != '/':
            image = '/' + image
        result_tags.append({
            'tag_pk'    : tag.id,
            'tag_name'  : tag.name,
            'tag_image' : request.build_absolute_uri('/media'+image)
        })

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
        result_newsletters.append({
            'newsletter_pk'         : newsletter.pk,
            'newsletter_name'       : newsletter.newsletter_name,
            'newsletter_image'      : request.build_absolute_uri('/media' + image),
            'newsletter_explain'    : newsletter.explain,
            'register_url'          : newsletter.register_url,
            'newsletter_tags'                  : tags
        })
    for episode in episodes:
        result_episodes.append({
            'episode_pk'        : episode.id,
            'newsletter_pk'     : episode.newsletter.id,
            'episode_title'     : episode.title,
            'episode_date'      : episode.date,
            'episode_url'       : episode.episode_url
        })
    
    response = {
        'status'    : 'S00',
        'message'   : 'Search Result',
        'value'     : {
            'newsletters'   : result_newsletters,
            'tags'          : result_tags,
            'episodes'      : result_episodes
        }
    }

    return Response(response)

@api_view(['POST'])
def get_newsletter_from_tag(request):
    tag = request.data['tag']
    tag = Tag.objects.get(id=tag)
    values = []
    newsletters = NewsLetter.objects.filter(tags=tag)
    
    for newsletter in newsletters:
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

        values.append({
            'newsletter_pk'             : newsletter.id,
            'newsletter_name'           : newsletter.newsletter_name,
            'newsletter_image'          : request.build_absolute_uri('/media' + image),
            'register_url'              : newsletter.register_url,
            'newsletter_explain'        : newsletter.explain,
            'newsletter_tags'           : tags
        })

    response = {
        'status'    : 'S00',
        'message'   : 'Newsletters have tag',
        'value'     : values
    }

    return Response(response)

@api_view(['POST'])
def get_newsletter(request):
    newsletter_pk = request.data['newsletter_pk']
    
    try:
        newsletter = NewsLetter.objects.get(id=newsletter_pk)    
        tags = []
        for tag in newsletter.tags.all():
            image = str(tag.image)
            if image[0] != '/':
                image = '/' + image
            tags.append({
                'tag_pk'    : tag.id,
                'tag_name'  : tag.name,
                'tag_image' : request.build_absolute_uri('/media'+image)
            })
        image = str(newsletter.image)
        if image[0] != '/':
            image = '/' + image
        status = 'S00'
        message = 'GET Newsletter Success'
        value = {
            'newsletter_pk'     : newsletter.id,
            'newsletter_name'   : newsletter.newsletter_name,
            'register_url'      : newsletter.register_url,
            'newsletter_explain': newsletter.explain,
            'newsletter_image'  : request.build_absolute_uri('/media'+image),
            'newsletter_tags'   : tags,
            'followers'         : newsletter.followers
        }
    except:
        status = 'E00'
        message = 'Wrong Newsletter ID'
        value = newsletter_pk
    
    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    return Response(response)

@api_view(['POST'])
def post_newsletter(request):
    newsletter_name = request.data['newsletter_name']
    newsletter_explain = request.data['newsletter_explain']
    newsletter_image = request.data['newsletter_image']
    newsletter_tags = json.loads(request.data['newsletter_tags'])['value']
    register_url = request.data['register_url']

    tags = []
    for t in newsletter_tags:
        t = Tag.objects.get(id=t)
        tags.append(t)
    
    try:
        newsletter = NewsLetter(
            newsletter_name = newsletter_name,
            register_url = register_url,
            explain = newsletter_explain,
            image = newsletter_image,
        )
        newsletter.save()
        
        for tag in tags:
            newsletter.tags.add(tag)

        status = 'S00'
        message = 'Success Newsletter POST'
        value = ''

    except:
        status = 'E00'
        message = 'FAIL Newsletter POST'
        value = ''
    

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }
    
    return Response(response)

@api_view(['POST'])
def famous_newsletter(request):
    newsletters = NewsLetter.objects.order_by('-followers')[:10]
    value = []

    for newsletter in newsletters:
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
            image = '/'+image

        
        value.append({
            'newsletter_pk'     : newsletter.id,
            'newsletter_name'   : newsletter.newsletter_name,
            'register_url'      : newsletter.register_url,
            'newsletter_explain': newsletter.explain,
            'newsletter_image'  : request.build_absolute_uri('/media' + image),
            'newsletter_tags'              : tags,
            'followers'         : newsletter.followers
        })

    response = {
        'status'    : 'S00',
        'message'   : 'Famous Newsletters',
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def get_episode(request):
    newsletter = request.data['newsletter_pk']

    try:
        episode_queryset = Episode.objects.filter(newsletter=newsletter)

        episodes = []
        for episode in episode_queryset:
            episodes.append({
                'episode_pk'    : episode.id,
                'episode_title' : episode.title,
                'episode_date'  : episode.date,
                'episode_url'   : episode.episode_url
            })
        
        status = 'S00'
        message = 'GET Episode'
        value = episodes
    except:
        status = 'E00'
        message = 'FAIL'
        value = ''

    response = {
        'status'    : status,
        'message'   : message,
        'value'     : value
    }

    return Response(response)

@api_view(['POST'])
def upload_episode(request):
    newsletter = NewsLetter.objects.get(newsletter_name='동네서점')

    try:
        episodes = Episode.objects.filter(newsletter=newsletter)
        for episode in episodes:
            episode.delete()
    except:
        pass
    print(newsletter)
    data = pd.read_csv('data/dongne.csv')
    print(data)

    
    for row in data.iloc():
        print(row['title'], row['link'])
        episode = Episode(
            newsletter=newsletter,
            title=row['title'],
            episode_url=row['link'],
        )
        episode.save()
    
    response = {
        'status'    : 'S00',
        'message'   : 'POST Episodes',
        'value'     : ''
    }

    return Response(response)

def register_newsletter_page(request):
    tags = Tag.objects.all()

    context = {
        'tags'  : tags
    }
    return render(request, 'register.html', context)

def register_newsletter(request):
    data = request.POST
    newsletter_name = data['newsletter_name']
    register_url = data['register_url']
    explain = data['explain']
    try:
        tags = data.getlist('tags')
    except:
        tags = []
    image = request.FILES['newsletter_image']

    newsletter_tags = []
    for tag in tags:
        t = Tag.objects.get(id=tag)
        newsletter_tags.append(t)
    
    newsletter = NewsLetter(
        newsletter_name=newsletter_name,
        register_url=register_url,
        explain=explain,
        image=image
    )
    newsletter.save()
    for tag in newsletter_tags:
        newsletter.tags.add(tag)

    return redirect('register_page')

@api_view(['POST'])
def update_newsletter_image(request):
    newsletters = NewsLetter.objects.all()

    for newsletter in newsletters:
        #print(newsletter.image)
        if newsletter.newsletter_name == '뉴닉':
            print('new_neek')
        elif newsletter.image == '/newsletter/new_neek.png':
            newsletter.image = '/newsletter/default.png'
            newsletter.save()


    response = {
        'status' : 'S00',
        'value'     : 'testing'
    }
    return Response(response)

def get_privacy(request):
    return render(request,'privacy.html')

def register_episode(request):
    data = request.POST
    episodes = data.getlist('episodes')
    dates = data.getlist('dates')
    titles = data.getlist('titles')
    episode_urls = data.getlist('episode_urls')
    newsletter_pk = data['newsletter']
    
    newsletter = NewsLetter.objects.get(id=newsletter_pk)
    
    for idx in len(data):
        print(idx)

    return