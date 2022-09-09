import requests
from fake_useragent import UserAgent
import bs4
import re


KEYWORDS = ["Читальный зал", "1С", "Python"]
base_url = 'https://habr.com'
url = '/ru/all/'
response = requests.get(base_url + url, headers={'User-Agent': UserAgent().chrome})
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')

articles = soup.find_all('article')
for article in articles:
    total_article_text = []
    title = article.find(class_='tm-article-snippet__title-link').text
    total_article_text.extend(title.split())

    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    for hub in hubs:
        hub = hub.text.split(',')
        total_article_text.extend(hub)

    link = base_url + article.find(class_='tm-article-snippet__title-link').attrs['href']
    article_response = requests.get(link, headers={'User-Agent': UserAgent().chrome})
    article_text = bs4.BeautifulSoup(article_response.text, features='html.parser')
    article_text = article_text.find_all(class_='tm-article-body')
    for txt in article_text:
        txt = txt.text.split()
        total_article_text.extend(txt)

    article_info = []
    for word in total_article_text:
        word = re.findall(r'(\w+[\s]?\w+)', word)
        if len(word) > 0:
            word = word[0]
            if word in KEYWORDS and link not in article_info:
                article_info.append(article.find(class_='tm-article-snippet__datetime-published').text)
                article_info.append(title)
                article_info.append(link)
                print(f'по ключевому слову "{word}" найдена уникальная статья :\n{article_info}')
                print()

