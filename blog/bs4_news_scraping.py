import asyncio
import os
import time
import json

import httpx
from bs4 import BeautifulSoup

# start_time = time.process_time() # If you want to measure the CPU execution time of a program
# start_time = time.time()
data_list = []  # list for all data articles (for .json file)
list_urls = []  # only for urls
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}


def scraping_function():
    """ function, to get list all urls articles from main page """
    url = 'https://portal.lviv.ua/article'  # target link
    resp = httpx.get(url, headers=headers, timeout=10.0)
    if resp.status_code != 200:
        raise Exception('HTTP err access!')

    soup = BeautifulSoup(resp.text, 'lxml')
    all_article = soup.find_all("div", class_='news-list-desc')

    for article in all_article:
        url_link = 'https://portal.lviv.ua' + article.select_one('a')['href']
        list_urls.append(url_link)
    return list_urls


async def article_content(url):
    """ get content on Single page each article """
    async with httpx.AsyncClient() as client:
        respon_detail = await client.get(url, headers=headers)
        soup_one_detail = BeautifulSoup(respon_detail.text, 'lxml')  #

    # getting content from all list <p> tags:
    one_detail = soup_one_detail.find_all(class_='article-content')  # get list <p> content article
    content = ' '.join([p.text for p in one_detail]) + 'link to original page:' + url

    # one_img = soup_one_detail.find('img', class_='article-content')
    try:
        img_ = soup_one_detail.find(class_='article-content').find_all('img')
        image_url = img_[0]['src']
    except Exception:  # IndexError, no images. Add default image-Logo
        image_url = 'https://portal.lviv.ua/wp-content/themes/lvivportal/images/logo.png'

    data_list.append({
        'title': soup_one_detail.find(class_='article-title').text,
        'url_link': url,
        'photo_url': image_url,
        'article-date': soup_one_detail.find(class_='article-date').text,
        'author': soup_one_detail.find(class_='article-comments-date').select_one('h4').text,
        'content': content
    })
    # return print('finished article:', url)


async def get_data_all_tasks():
    """ Run all tasks """
    scraping_function()  # run function to create list-urls
    queue = asyncio.Queue()
    tasks_list = []
    for item in list_urls:
        task = asyncio.create_task(article_content(item))
        tasks_list.append(task)

    await queue.join()
    await asyncio.gather(*tasks_list, return_exceptions=True)


def main():
    """ start async, write data to json """
    start_time = time.time()
    asyncio.run(get_data_all_tasks())
    if os.path.exists("data_news.json"):
        os.remove("data_news.json")
    else:
        with open('data_news.json', 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=4, ensure_ascii=False)

    print('time after json file', time.time() - start_time, 'sec')
    print('data_list created, done. Total articles = ', len(data_list))
    return data_list


if __name__ == "__main__":
    main()
