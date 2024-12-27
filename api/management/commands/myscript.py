import requests
from bs4 import BeautifulSoup
from .db import execute_query
import os
import aiohttp
import asyncio
import aiofiles
import json

url = 'https://books.toscrape.com/'
currency_url = 'https://cbu.uz/oz/arkhiv-kursov-valyut/json/'

async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()

async def fetch_image(session, image_url, save_path):
    async with session.get(image_url) as response:  
        if response.status == 200:
            async with aiofiles.open(file=save_path, mode='wb') as f:
                await f.write(await response.read())
    
async def fetch_detail(session, detail_url):
    detail_html = await fetch(session, detail_url)
    detail_soup = BeautifulSoup(detail_html, 'html.parser')
    for article in detail_soup.find_all('article', class_="product_page"):
        for child in article.children:
            if child.name == 'p':
                description = child.text
                return description


async def parsing():
    async with aiohttp.ClientSession() as session:
        try:
            response_html = await fetch(session=session, url=url)
            soup = BeautifulSoup(response_html, 'html.parser')

            for article in soup.find_all('article', class_="product_pod"):
                if article.find('h3'):
                    h3 = article.find('h3')
                    a = h3.find('a')
                    title = a.get('title')
                    detail_p = a.get('href')
                    detail_url = os.path.join(url, detail_p)
                    description = await fetch_detail(session=session,detail_url=detail_url)
                image = article.find('img')
                image_name = os.path.basename(image.get('src'))
                media_path = os.path.join('media', 'book_images', image_name)
                media_path_for_db = os.path.join('book_images', image_name)
                image_url = os.path.join(url, image.get('src'))
                await fetch_image(session=session, image_url=image_url, save_path=media_path)

                res = requests.get(url=currency_url)
                curr = json.loads(res.text)
                price = article.find('p', class_='price_color').get_text()[1:]
                price_in_sum =float(curr[1]['Rate'])*float(price)
                execute_query(title=title, photo=media_path_for_db, price=price_in_sum, description=description)

        except aiohttp.ClientError as e:
            print(f"HTTP xatolik yuz berdi: {e}")
        except asyncio.TimeoutError:
            print("So'rov vaqtida kutib turish tugadi (timeout).")
