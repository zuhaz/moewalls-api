"""
Scraper module for the MoeWalls API.
This module contains functions for scraping wallpaper data from the MoeWalls website.
"""

import requests
import random
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

def get_html(url, retries=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Error fetching {url}: {e}. Retrying...")
            time.sleep(random.uniform(1, 3))
    
    raise RequestException(f"Failed to fetch {url} after {retries} retries")

def get_soup(html):
    return BeautifulSoup(html, 'html.parser')

def get_video_url(wallpaper_url):
    try:
        html = get_html(wallpaper_url)
        soup = get_soup(html)
        video_element = soup.select_one("video.video-js.vjs-default-skin.vjs-big-play-centered > source")
        if video_element and 'src' in video_element.attrs:
            return video_element['src']
    except Exception as e:
        print(f"Error fetching video URL from {wallpaper_url}: {e}")
    return None

def scrape_wallpaper(wallpaper_li):
    if wallpaper_li.select_one("div.g1-advertisement"):
        return None
    
    wallpaper = {}
    wallpaper['title'] = wallpaper_li.select_one("h3.g1-gamma.g1-gamma-1st.entry-title a").text
    wallpaper['url'] = wallpaper_li.select_one("h3.g1-gamma.g1-gamma-1st.entry-title a")['href']
    wallpaper['thumbnail'] = wallpaper_li.select_one("a.g1-frame img")['src']
    wallpaper['video_url'] = get_video_url(wallpaper['url'])
    return wallpaper

def scrape_wallpapers(search_term, page=1, limit=None):
    url = f"https://moewalls.com/page/{page}/?s={search_term}"
    print(f"Scraping page {page}: {url}")
    
    wallpapers = []
    try:
        html = get_html(url)
        soup = get_soup(html)

        wallpapers_li = soup.select("li.g1-collection-item.g1-collection-item-1of3")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for li in wallpapers_li:
                if limit and len(wallpapers) >= limit:
                    break
                futures.append(executor.submit(scrape_wallpaper, li))
            
            for future in as_completed(futures):
                if limit and len(wallpapers) >= limit:
                    break
                result = future.result()
                if result:
                    wallpapers.append(result)
                    if limit and len(wallpapers) >= limit:
                        break
    
    except Exception as e:
        print(f"Error scraping page {page}: {e}")
        raise

    return wallpapers[:limit] if limit else wallpapers

def get_total_pages(search_term):
    try:
        url = f"https://moewalls.com/?s={search_term}"
        soup = get_soup(get_html(url))
        pagination = soup.select_one("div.pagination.loop-pagination")
        
        if pagination:
            page_numbers = pagination.find_all('a', class_='page-numbers')
            if page_numbers:
                last_page = max(int(page.text) for page in page_numbers if page.text.isdigit())
                return last_page
        
        return 1
    except Exception as e:
        print(f"Error getting total pages: {e}")
        raise
