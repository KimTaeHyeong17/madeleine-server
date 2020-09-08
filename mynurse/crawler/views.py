from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .news_parser import crawl_news
# Create your views here.
@api_view(['POST'])
def get_news(request):
    news = crawl_news()
    print(news)
    news_list = []
    for row in news.iterrows():
        print(type(row))
        news_list.append(
            {
                'press'     : row[1][0],
                'title'     : row[1][1],
                'link'      : row[1][2]
            }
        )
    response = {
        'status'    : 'S00',
        'message'   : 'This is News',
        'value'     : news_list
    }
    return Response(response)