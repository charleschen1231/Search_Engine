import requests
from bs4 import BeautifulSoup
import pprint
import json
import pandas as pd
from lxml import etree


'''

爬取bbc网站中climate相关的文本200个，
爬取sport 200个
Technology  200个

climate:https://www.bbc.co.uk/search?q=climate&d=weather_ps&page=1
sport

'''

import requests
from bs4 import BeautifulSoup

import pandas as pd





# construct page list
page_indexs = range(1, 5, 1)
page_indexs = list(page_indexs)
print(page_indexs)

# download all the htmls of page to analyse
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

climate_title_htmls = []
climate_titles=[]
def  get_climate_links():
    for idx in page_indexs:
        print(idx)
        # if idx == 0:
        url = f"https://www.bbc.co.uk/search?q=climate&d=weather_ps&page={idx}"
        # else:
        #     url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page={idx}"

        # url = f"https://movie.douban.com/top250?start={idx}&filter="

        print("craw html:", url)
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception("error")
        # time.sleep(2)

        soup = BeautifulSoup(r.text, "html.parser")
        role = "list"
        spacing = "responsive"

        # ul role="list" spacing="responsive" class="ssrcss-1020bd1-Stack e1y4nx260"
        items=(
            soup.find('ul',spacing="responsive", class_="ssrcss-1020bd1-Stack e1y4nx260")

            # div class ="ssrcss-tq7xfh-PromoContent e1f5wbog8"
            .find_all('div', class_="ssrcss-tq7xfh-PromoContent e1f5wbog8")
        )

        print('items=',items)
        for item in items:
            title_link = item.find('div', class_='ssrcss-1f3bvyz-Stack e1y4nx260').find("a").get('href')

            print('title_link=', title_link)

            climate_title_htmls.append(title_link)
            # get title
            title = item.find('div', class_='ssrcss-1f3bvyz-Stack e1y4nx260').get_text()
            print('title=', title)
            climate_titles.append(title)

    data_infos = {
            "title":  climate_titles,

            "title_link": climate_title_htmls,

        }
    df = pd.DataFrame(data_infos)
    print(df)
    df.to_csv("climate.csv")

    return df



print("kaishi")
'''
title,
title_link,
content
tag_1:[sport,climate,technology 

out put:

'''






if __name__ == '__main__':
     df=get_climate_links()











# 加载数据
#
content_datas=[]
df = pd.read_csv("climate.csv")
for title_link in df['title_link']:
    print(title_link)
    if(title_link==title_link=='https://www.bbc.co.uk/sport/olympics/65099356'):
        content = "Climate change is threatening high-performance sport's existence, says UK Sport chief executive Sally Munday.The government agency has a new sustainability strategy, called Team of Tomorrow.The aim is to get British Olympic and Paralympic sport to have a net positive impact on the environment by 2040.Every governing body has been told to have a sustainability action plan in place by 2025.The Premier League's domestic flights dilemma"
        print('content=', content)
        content_datas.append(content)
    elif(title_link==title_link=='https://www.bbc.co.uk/sport/football/65085346'):
        content = "Ten years ago we were a lone voice with a radical idea, today it's fast becoming normal.League One Forest Green Rovers - labelled the 'greenest' football club in the world - were always likely to come top of a list of the English Football League's most sustainable clubs.But owner and chairman Dale Vince says a new table ranking the top 20 EFL clubs on their climate-friendly activities off the pitch shows real progress among the rest of the English football pyramid.Vince said: It's great to see the extent to which sustainability in football has become a thing, almost but not yet - an accepted part of the game"
        print('content=', content)
        content_datas.append(content)

    elif (title_link == title_link == 'https://www.bbc.co.uk/programmes/w13xtvmk'):
        content = "The BBC will host an ambitious, high-level Global Climate Debate on Monday 1 November, the opening day of the climate summit. Four leading global political figures will come together to take questions from young people in the studio and around the world on the challenges presented by climate change, and the hopes for global solutions to be achieved at the COP climate change meeting."
        print('content=', content)
        content_datas.append(content)

    elif (title_link == title_link == 'https://www.bbc.co.uk/programmes/l00567ch'):
        content = "Justin Rowlatt puts your Global climate questions to UN Secretary-General Antonio Guterres"
        print('content=', content)
        content_datas.append(content)

    else:
        r = requests.get(title_link)
        soup = BeautifulSoup(r.text, "html.parser")
        if (soup.find("div", class_='synopsis-toggle__short') is not None):
            content = soup.find("div", class_='synopsis-toggle__short').get_text()
            # content=soup.find('div',class_='br_container')
            print('content=', content)
            content_datas.append(content)
        elif (soup.find("div", class_='text--prose longest-synopsis') is not None):
            content = soup.find("div", class_='text--prose longest-synopsis').get_text()
            print('content=', content)
            content_datas.append(content)
        elif (soup.find_all("div", class_="ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0") is not None):
            content = soup.find("div", class_="ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0").get_text()
            print('content=', content)
            content_datas.append(content)


df['content'] = content_datas
print('df=',df)
df.to_csv("climate.csv")