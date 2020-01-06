from requests import get
import json
from bs4 import BeautifulSoup as bs

base_url = 'https://gogoanime.movie/'
name = 'naruto'
ep = 2

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

def get_links(base_url, name, ep):
    # name its the anime name
    # ep can be a tuble with a interval like (10, 20)
    # or the number os eps like 30, so it'll get the 30 first eps
    links = []
    if isinstance(ep, tuple):
        init = ep[0]
        end = ep[1]
        for ep in range(init, end):
            custom_url = f'{base_url}{name}-episode-{ep}'
            links.append(custom_url)
    else:
        for ep in range(1, ep):
            custom_url = f'{base_url}{name}-episode-{ep}'
            links.append(custom_url)
    return links


def get_page(link):
    try:
        request = get(link)
        page = request.text
    except:
        print('Invalid link')
        return
    return page


def get_download_page(html, elem, pattern):
    # elem its the html element where the link its alocate
    # pattern its the class to search for in the page
    parser = bs(html, 'html.parser')
    button = parser.find_all(elem, class_=pattern) # Search download button
    page_link = button[0].parent.get('href')  # Get download page link
    return page_link


def get_download_link(parser):
    def has_download_attr(tag):
        return tag.has_attr('download')

    link = parser.find_all(has_download_attr)[0].get('href')  # Search download button and get link
    return link


def download_anime(link, file_name):
    # file_name its the output file name
    try:
        response = get(link, stream=True, headers=headers)
        with open(f'{file_name}.mp4', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):  # chunk_size is the buffer(1mb) 
                f.write(chunk)
    except Exception as err:
        print('Connection Failed')
        return f'Error: {err}'


links = get_links(base_url, name, ep)
ep_count = 1
for link in links:
    print(f'Custom link: {link}')
    page = get_page(link)
    download_page = get_download_page(page, 'span', 'btndownload')
    page = get_page(download_page)
    parser = bs(page, 'html.parser')
    download_link = get_download_link(parser)
    print(f'Download link: {download_link}')
    download_anime(download_link, f'{name}-ep-{ep_count}')
    ep_count += 1
