import requests
from bs4 import BeautifulSoup
import pprint
import json
import pandas as pd
from lxml import etree



'''
technology
url=f'https://www.bbc.co.uk/search?q=Technology&d=HOMEPAGE_PS'
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
url = "https://www.bbc.co.uk/search?q=Technology&d=HOMEPAGE_PS"
res = requests.get(url, headers=headers)


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
        url = f"https://www.bbc.co.uk/search?q=Technology&d=HOMEPAGE_PS={idx}"
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
    df.to_csv("technology.csv")

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
df = pd.read_csv("technology.csv")
for title_link in df['title_link']:
    print(title_link)
    if(title_link==title_link=='https://www.bbc.co.uk/sport/golf/65106521'):
        content = "A Mexican golf course designed by Tiger Woods will host the 2023 World Wide Technology Championship.The 15-time major champion designed El Cardonal, located at Diamante Cabo San Lucas, based on the courses he grew up playing in southern California.The par-72, 7,300-yard course - which overlooks the Pacific Ocean - opened in 2014.The World Wide Technology Championship was previously held at Mayakoba, on Mexico's Riviera Maya.In 2007 it became the first PGA Tour event to be contested outside the United States or Canada, but the agreement with Mayakoba ended in 2022.The 2023 edition of the tournament will take place in the autumn."
        print('content=', content)
        content_datas.append(content)
    elif(title_link==title_link=='https://www.bbc.co.uk/programmes/p00zxjxl'):
        content = "Sorry, we couldn’t find that pageCheck the page address or search for it below."
        print('content=', content)
        content_datas.append(content)

    elif (title_link == title_link == 'https://www.bbc.co.uk/programmes/p00fqcbg'):
        content = "Twitter chief Elon Musk is among those who want training of AIs above a certain capacity to be halted for at least six months.Apple co-founder Steve Wozniak and some researchers at DeepMind also signed."
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
df.to_csv("technology.csv")