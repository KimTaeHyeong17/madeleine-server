import pandas as pd 
import feedparser
import requests

#네이버뉴스에서 백신으로 검색한 결과 rss
urls =  'http://newssearch.naver.com/search.naver?where=rss&query=%EB%B0%B1%EC%8B%A0&field=0&nx_search_query=&nx_and_query=&nx_sub_query=&nx_search_hlquery=&is_dts=0' 

def crawl_news():
    title_list = list()
    link_list = list()
    author_list = list()

    d = feedparser.parse(urls)
    for i in range(len(d.entries)):
        title = d.entries[i].title
        title_list.append(title)

        link = d.entries[i].link
        link_list.append(link)

        author = d.entries[i].author
        author_list.append(author)

    df = pd.DataFrame({'언론사': author_list, '제목' : title_list, '링크' : link_list})
    print(df.head())

    return df.head()