import requests
from bs4 import BeautifulSoup

url = "https://habr.com/ru/articles/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
response = requests.get(url, headers=headers)
print(response.status_code)

soup = BeautifulSoup(response.text, "lxml")
articles = soup.find_all("article")
print(f"Найдено article: {len(articles)}")

if articles:
    print(articles[0].prettify()[:2000])

"""
articles = soup.find_all("article", class_="tm-articles-list__item")
print(len(articles))  # сколько?

snippets = soup.find_all("div", class_="article-snippet")
print(len(snippets))  # сколько?

metas = soup.find_all("div", class_="meta-container")
print(len(metas))  # сколько?
"""

