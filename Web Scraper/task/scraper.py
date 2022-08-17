import os
import re
import string

import requests as requests
from bs4 import BeautifulSoup

Page_N = int(input())
input_article_type = input()
cwd_path = os.getcwd()



def scrape_page(page_number):
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    response = requests.get(url, params={'page': page_number})

    if response.status_code != 200:
        print(f"The URL returned {response.status_code}!")
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find("section", {'id': 'new-article-list'}).findAll(
            "li", {'class': 'app-article-list-row__item'})

        os.chdir(cwd_path)
        os.mkdir('Page_' + str(page_number))

        for article in articles:
            soup = BeautifulSoup(article.encode('utf-8'), 'html.parser')
            article_type = soup.find('span', {'class': 'c-meta__type'}).text
            if article_type == input_article_type:
                article_link = "https://www.nature.com" + article.a.get('href')
                response = requests.get(article_link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_title = soup.find('h1', {
                        'class': 'c-article-magazine-title'}).text
                    article_title = re.sub('[' + string.punctuation + ']', '',
                                           article_title)
                    article_title = article_title.replace(' ', '_')
                    try:
                        os.chdir(os.path.join(cwd_path, 'Page_' + str(page_number)))
                        file = open(article_title + ".txt", "wb")
                        article_body = soup.find('div', {
                            'class': 'c-article-body'}).text
                        file.write(article_body.encode('utf-8'))
                        os.chdir("..")
                    except IOError:
                        print("Issue with files.")


for i in range(Page_N):
    scrape_page(i + 1)
print("Saved all articles.")
