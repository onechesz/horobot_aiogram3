import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def get_article_data_daily(session, article, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    async with session.get(url, headers=headers):
        return article.find(name='h3').text, article.find(name='div', attrs={'class': 'BDPZt KUbeq'}).text


async def gather_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(await response.text(), 'lxml')
        section = soup.find(name='section', attrs={'class': 'IjM3t'})
        articles = section.find_all(name='article')
        coros = list()

        for article in articles:
            coro = get_article_data_daily(session, article, url)
            coros.append(coro)

        return await asyncio.gather(*coros)


# horoscope_daily = {tup[0]: tup[1] for tup in asyncio.run(gather_data('https://74.ru/horoscope/daily/'))}
# horoscope_tomorrow = {tup[0]: tup[1] for tup in asyncio.run(gather_data('https://74.ru/horoscope/tomorrow/'))}
# horoscope_weekly = {tup[0]: tup[1] for tup in asyncio.run(gather_data('https://74.ru/horoscope/weekly/'))}


def horoscope_parser_daily():
    return gather_data('https://74.ru/horoscope/daily/')


def horoscope_parser_tomorrow():
    return gather_data('https://74.ru/horoscope/tomorrow/')


def horoscope_parser_weekly():
    return gather_data('https://74.ru/horoscope/weekly/')
