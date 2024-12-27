import requests
from bs4 import BeautifulSoup
import os
import json
import shutil
from urllib.parse import urljoin


currency_url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'

def parse_book_detail(detail_url):
    response = requests.get(url=detail_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for article in soup.find_all('article', class_="product_page"):
            for child in article.children:
                if child.name == 'p':
                    description = child.text
                    return description


def parse_book_data(book_url=None, book_title=None):

    response = requests.get(url=book_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
            if book_title in article.find('h3').find('a').get('title'):
                title = article.find('h3').find('a').get('title')
                h3 = article.find('h3')
                a = h3.find('a')
                detail_p = a.get('href')
                detail_url = urljoin(book_url, detail_p)
                description = parse_book_detail(detail_url=detail_url)
                image = article.find('img')
                image_name = os.path.basename(image.get('src'))
                media_path = os.path.join('media', 'book_images', image_name)
                media_path_for_db = os.path.join('book_images', image_name)
                image_url = urljoin(book_url, image.get('src'))
                res_image = requests.get(url=image_url, stream=True)
                res_image.raise_for_status()
                with open(file=media_path, mode='wb') as f:
                    shutil.copyfileobj(res_image.raw, f)
                res_curr = requests.get(url=currency_url)
                curr = json.loads(res_curr.text)
                price = article.find('p', class_='price_color').get_text()[1:]
                price_in_sum =float(curr[1]['Rate'])*float(price[1:])
                return {"title": title, "photo": media_path_for_db, "price": price_in_sum, "description": description}