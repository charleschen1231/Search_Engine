'''

1 class 1爬取页面相关元素 并解析
2  class 2 爬取内容 并生成datarrame

1  This part of the code is the crawler part of task1. It can get the title of the article, the link of the title of the article,
 the author of the article, the link of the author's introduction, the publication time, and the content of the article.
  I crawled the abstract part as the content of the article.

2 The first time I manually crawled the publication information, then I got the total number of publications,
then set a time interval to monitor the number, and if the number changed, It can automatically crawled all the publications again.



'''
import requests
from bs4 import BeautifulSoup
import pprint
import json
import pandas as pd
from lxml import etree
import time
from datetime import datetime, timedelta

# # get the publication numbers
# def get_numbers():
#     url = 'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/'
#
#     r = requests.get(url, headers=headers)
#     if r.status_code != 200:
#         raise Exception("error")
#     # time.sleep(2)
#
#     soup = BeautifulSoup(r.text, "html.parser")
#
#     # 获取文章数量
#     # i class="icon icon-publications"
#     publication_num = soup.find('span', class_="count").get_text()
#     publication_num = publication_num.replace("(", "").replace(")", "")
#     print('publication_num=', publication_num)
#     return publication_num
#
#
#
# while True:
#     # 计算当前时间和下一次执行任务的时间差
#     now = datetime.now()
#     # set a time interval to monitor the number
#     next_run = now + timedelta(minutes=5)
#     time_diff = (next_run - now).total_seconds()
#
#     # 等待时间差
#     time.sleep(time_diff)
#
#     # 执行任务
#     get_numbers()




data_titles = []
data_title_links = []
data_publication_years = []
data_author_hrefs = []
data_authors = []

# construct page list
page_indexs = range(0, 5, 1)
page_indexs = list(page_indexs)
print(page_indexs)

# download all the htmls of page to analyse
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
class Crwal_pages_parser:
    def __init__(self):
        print(self)

    # print(page_indexs)



    def download_all_htmls():
        htmls = []
        for idx in page_indexs:
            print(idx)
            if idx == 0:
                url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/"
            else:
                url = f"https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/?page={idx}"

            # url = f"https://movie.douban.com/top250?start={idx}&filter="
            print("craw html:", url)
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                raise Exception("error")
            htmls.append(r.text)
        return htmls



    def parse_single_html(html):

        tree = etree.HTML(html)

        div_titles = tree.xpath('//h3[@class="title"]')
        div_infos = tree.xpath('//div[@class="result-container"]')
        print("div_titles:", type(div_titles))

        for div_title in div_titles:
            # print(type(div_title))
            # print(len(div_title))
            title_links = div_title.xpath('./a/@href')[0].strip()
            # /html/body/main/div[1]/div/div/section/ul/li[1]/div[2]/div[1]/h3/a/span
            # title = div.xpath('//a[@rel="ContributionToBookAnthology"]/span/text()')[0].strip()
            title = div_title.xpath('./a/span[last()]/text()')
            print(type(title))
            print('title:', title[0])
            print('title_links=', title_links)

            data_titles.append(title[0])
            data_title_links.append(title_links)

        for div_info in div_infos:
            publication_year = div_info.xpath('.//span[@class="date"]/text()')
            print("publication_year:", publication_year)

            authors_href = div_info.xpath('.//a[@rel="Person"]/@href')
            print(authors_href)

            authors = div_info.xpath('.//a[@rel="Person"]/span/text()')
            print(authors)
            data_publication_years.append(publication_year)
            data_author_hrefs.append(authors_href)
            data_authors.append(authors)

        # # return datas
        #     print(len(data_titles))
        #     print(len(data_title_links))
        #     print(len(data_publication_years))
        #     print(len(data_authors))
        #     print(len(data_author_hrefs))

        data_infos = {
            "title": data_titles,
            "publication_year": data_publication_years,
            "title_link": data_title_links,
            "authors": data_authors,
            "author_href": data_author_hrefs
        }
        df = pd.DataFrame(data_infos)
        print(df)
        df.to_csv("Publication_Info.csv")


content_datas = []
class Content:
    def __init__(self):
        print(self)

    def get_content():
        df = pd.read_csv("Publication_Info.csv")
        for title_link in df['title_link']:
            print(title_link)
            r = requests.get(title_link)
            soup = BeautifulSoup(r.text, "html.parser")

            if (soup.find("div", class_='textblock') is not None):

                content = soup.find("div", class_='textblock').get_text('p')
                print(type(content))
                print(content)
                content_datas.append(content)



            elif (soup.find("div", class_='rendering').find('h1').find('span').contents is not None):
                ontent = soup.find("div", class_='rendering').find('h1').find('span').contents
                print(type(content))
                print('content_title=', content)
                content_datas.append(content)

        print(len(content_datas))
        df['content'] = content_datas
        print('df=', df)
        df.to_csv("Publication_Info.csv")
        print(len(df))




if __name__ == '__main__':

    # if(num != len(df)):
        crwal_parser = Crwal_pages_parser
        htmls = crwal_parser.download_all_htmls()

        print('len:', len(htmls))

        for html in htmls:
            crwal_parser.parse_single_html(html)

        contenter = Content
        contenter.get_content()

        # num = get_numbers()






