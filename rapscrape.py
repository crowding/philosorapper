#!/usr/bin/env python3

import itertools
from bs4 import BeautifulSoup
from urllib import request, parse
import sys

def page_soup(url):
    print(url, end="")
    with request.urlopen(url) as page:
        soup = BeautifulSoup(page.read())
        print("\r", end="")
    return soup

def song_urls_from_song_list(list, base_url):
    links = list.find_all("a", "song_link")
    urls = abs_urls([x.attrs ['href'] for x in links],
                    base_url)
    return urls

def song_urls_from_page_soup(soup, base_url):
    song_lists = soup.find_all("ul", "song_list")
    urls = song_urls_from_song_list(song_lists[-1], base_url)
    return urls

def further_pages_from_soup(soup, base_url):
    page_links = soup.find("div","pagination").find_all("a")
    return abs_urls([x.attrs['href'] for x in page_links], base_url)

def song_urls_from_root_url(root_url):
    root_soup = page_soup(root_url)
    urls = further_pages_from_soup(root_soup, root_url)
    page_soups = ((page_soup(u)) for u in urls)
    song_urls = itertools.chain(
        song_urls_from_page_soup(root_soup, root_url),
        itertools.chain.from_iterable(
            song_urls_from_page_soup (s, u) for (s, u) in zip (page_soups, urls)))
    return song_urls

def song_urls_from_page_url(url, base_uel):
    root_url = "http://rapgenius.com/artists/" + rapper
    with request.urlopen(url) as page:
        soup = BeautifulSoup(page.read())
    return song_urls_from_page_soup(soup, base_url)

def abs_urls(relative_urls, base_url):
    return [parse.urljoin(base_url, x) for x in relative_urls]

def song_lyrics_from_soup(soup):
    return soup.find("div", "lyrics").text
    pass

def scrape_artist_lyrics(rapper):
    root_url = "http://rapgenius.com/artists/" + rapper
    song_urls = song_urls_from_root_url(root_url)
    song_soups = (page_soup(u) for u in song_urls)
    lyrics = (song_lyrics_from_soup(s) for s in song_soups)
    return lyrics

def scrape_artist_to_file(rapper, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for l in scrape_artist_lyrics(rapper):
            print(l, file=f)

if (__name__ == "__main__"):
    scrape_artist_to_file("Jay-z", "jay_z_lyrics.txt")
    

