import aiohttp
import asyncio
import shelve
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CACHE_FILE = 'link_checker_cache'
PARSER = 'lxml'  # Change this to 'lxml' if you want to use lxml

visited_urls = set()

def is_visited(url):
    with shelve.open(CACHE_FILE) as cache:
        # If URL is in cache, return True
        if url in cache:
            return True
    return False

def mark_as_visited(url):
    with shelve.open(CACHE_FILE, writeback=True) as cache:
        cache[url] = True

async def fetch(url, session):
    async with session.get(url) as response:
        content = await response.text()
        mark_as_visited(url)
        return content

async def get_all_links(url, session):
    if is_visited(url):
        return

    content = await fetch(url, session)
    soup = BeautifulSoup(content, PARSER)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            full_url = urljoin(url, href)
            if is_same_domain(url, full_url) and not is_visited(full_url):
                yield full_url

def is_same_domain(main_url, url_to_check):
    return urlparse(main_url).netloc == urlparse(url_to_check).netloc

async def main():
    url = "https://ursa.fi"
    async with aiohttp.ClientSession() as session:
        async for link in get_all_links(url, session):
            print(link)

if __name__ == "__main__":
    asyncio.run(main())
