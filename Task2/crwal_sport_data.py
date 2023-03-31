import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

sport_title_htmls = []

url = f"https://www.bbc.co.uk/sport"

print("craw html:", url)
r = requests.get(url, headers=headers)
if r.status_code != 200:
    raise Exception("error")

soup = BeautifulSoup(r.text, "html.parser")
items = soup.find("main", id='main-content').find_all("div", class_="ssrcss-1ocoo3l-Wrap e42f8511")

for item in items:
    infos = item.find_all_next('div', class_="ssrcss-15rbpu3-PromoSwitchLayoutAtBreakpoints e3z3r3u0")
    if infos is not None:
        for i in infos:
            herf = i.findNext("div", spacing="2", class_="ssrcss-1f3bvyz-Stack e1y4nx260").find("a").get('href')
            title_herf = "https://www.bbc.co.uk" + herf
            if len(title_herf) < 100 and title_herf != "https://www.bbc.co.uk/sport/av/basketball/65124833":
                sport_title_htmls.append(title_herf)

sport_titles = []
sport_contents = []
for html in sport_title_htmls:
    r = requests.get(html, headers=headers)
    if r.status_code != 200:
        raise Exception("error")
    soup = BeautifulSoup(r.text, "html.parser")
    if soup.find('h1', id='page') is not None:
        title = soup.find('h1', id='page').get_text()
        content_tag = soup.find('div', class_="qa-story-body story-body gel-pica gel-10/12@m gel-7/8@l gs-u-ml0@l gs-u-pb++")
        if content_tag is not None:
            content = content_tag.get_text()
        else:
            content = ''
    elif soup.find('h1', id="main-heading") is not None:
        title = soup.find('h1', id="main-heading").get_text()
        content_tag = soup.find("article", class_="ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6")
        if content_tag is not None:
            content = content_tag.get_text()
        else:
            content = ''
    else:
        continue

    sport_titles.append(title)
    sport_contents.append(content)
    # introduce a delay of 1 second between each request to be polite
    # time.sleep(1)

# check if all arrays have the same length
if len(sport_titles) == len(sport_title_htmls) == len(sport_contents):
    data_infos = {
        "title": sport_titles,
        "title_link": sport_title_htmls,
        "content": sport_contents
    }
    df = pd.DataFrame(data_infos)
    df.to_csv("sport.csv", index=False)
    print("Finished scraping the data and saved to 'sport.csv'")
else:
    print(f"No title or content found on page {html}")

