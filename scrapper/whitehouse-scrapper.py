#!/usr/bin/python

import os
import requests
from bs4 import BeautifulSoup

list_articles = []
base_urls_list = []
base_url = "https://www.whitehouse.gov/news/page/"

def get_base_urls():
    results = requests.get(base_url)
    source = results.content
    soup = BeautifulSoup(source, 'lxml')
    #  pagination_tag = soup.find("div", class_= "page-results__wrap")
    #  last_page_num = pagination_tag
    #  print(last_page_num)
    for i in range(1, 100):
        url = f'{base_url}{i}/'
        base_urls_list.append(url)

class Article():
    def __init__(self, title, link, date, statement, issue):
        self.title = title
        self.link = link
        self.date = date
        self.statement = statement
        self.issue = issue

def get_pages_articles():
    for page in base_urls_list:
        results = requests.get(page)
        source = results.content
        soup = BeautifulSoup(source, 'lxml')
        for article_tag in soup.find_all("article"):
            a_tag = article_tag.find("h2").find("a")
            link = a_tag.attrs['href']
            title = a_tag.contents[0].replace(',', ' ').replace('.', '').strip()

            statement = article_tag.p.text.strip()
            issue_tag = article_tag.find_all('p')[-1].a

            if issue_tag == None:
                issue = 'None'
            else:
                issue = issue_tag.contents[0].strip()

            date = article_tag.find('time').contents[0].replace(',',' ').strip()

            article = Article(title, link, date, statement, issue)
            list_articles.append(article)

def save_articles():

    f = open('../data/whitehouse-articles.csv', 'w')
    f.write('title, statement, issue, date, link\n ')
    for article in list_articles:
        f.write(f'{article.title}, {article.statement}, {article.issue}, \
                {article.date}, {article.link}\n')


if __name__ == "__main__":
    get_base_urls()
    get_pages_articles()
    
    print(list_articles[0].date)
    print(list_articles[0].statement)
    print(list_articles[0].title)
    print(list_articles[0].issue)
    print(list_articles[0].link)

    save_articles()
