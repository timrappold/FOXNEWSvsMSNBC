
import sys
#sys.path.append("../data/")


from bs4 import BeautifulSoup
import requests
import os
import sys
import time
import numpy as np
from selenium import webdriver
import pickle
import re

data_path = 'data/'

def get_soup(url):
    """
    Accepts URL and returns a BeautifulSoup object using the requests library.

    :param url: str.
    :return: BeautifulSoup object.
    """
    hdr = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=hdr)
    assert response.status_code == 200, "HTML status code isn't 200 for {}.".format(url)

    return BeautifulSoup(response.text, "lxml")

# Scrape and save Fox News episode transcript links:


def scrape_FOX_transcript_urls(filename='fox_news_episode_links.pkl'):
    """
    Scrape FOX News website for links to episode transcripts for `Hannity` and
    `The Ingraham Angle`. The number of links is determined in num_page_expands.

    :param filename: str. Use *.pkl to indicate serialization.
    :return: None
    """
    chromedriver = "~/Downloads/chromedriver"  # path to the chromedriver executable
    chromedriver = os.path.expanduser(chromedriver)
    print('chromedriver path: {}'.format(chromedriver))
    sys.path.append(chromedriver)

    landing_urls = {
        'Hannity': 'http://www.foxnews.com/category/shows/hannity/transcript.html',
        'Ingraham': 'http://www.foxnews.com/category/shows/ingraham-angle/transcript.html'
        }

    shows = {}
    num_page_expands = 12

    for show, url in landing_urls.items():
        print('Show: ', show)
        print('Landing URL: ', url)

        driver = webdriver.Chrome(chromedriver)
        driver.get(url)

        # Expand page source by clicking on load-more button:
        for i in range(num_page_expands):
            print(i)
            driver.find_element_by_css_selector(
                '.button.load-more.js-load-more').click()
            r = 0.5 * np.random.randn(1) + 6
            time.sleep(r)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # Gather all the links to the episode transcripts:
        link_list = []
        for i, class_ in enumerate(soup.find_all('h2', class_="title")):
            episode_link = (class_.find('a').get_text(), class_.find('a')['href'])
            print(episode_link)
            link_list.append(episode_link)

        shows[show] = {'urls': link_list,
                       'landing_url': url}

        # Save links:
        with open(filename, 'wb') as picklefile:
            pickle.dump(shows, picklefile)

    return None

# Scrape and save Fox News episode transcripts:


def scrape_FOX_transcripts(from_file='fox_news_episode_links.pkl',
                           to_file='fox_news_transcripts3.pkl'):
    """
    Scrape transcripts of MSNBC's `Rachel Maddow Show` and `The Last Word with
    Lawrence O'Donnel`. Stores transcripts in a dictionary with the following
    structure: {'show': show (str),
                'title': title (str),
                'date': air date (str),
                'url': url of transcript (str),
                'transcript': transcript (str)}

    :param from_file: path to file with episode transcript links.
    :param to_file: path to file with transcripts.
    :return:
    """

    with open(from_file, 'rb') as picklefile:
        fox_links = pickle.load(picklefile)

    episodes_list = []

    for show in fox_links:
        for episode in fox_links[show]['urls']:
            print('Title:', episode[0], 'Link:', episode[1])
            url = 'http://www.foxnews.com' + episode[1]
            soup = get_soup(url)
            transcript = soup.find('div', class_="article-body").get_text()

            ep = {'show': show,
                  'date': episode[1].strip('/transcripts/')[:10],
                  'title': episode[0],
                  'url': url,
                  'transcript': transcript}

            episodes_list.append(ep)

            with open(to_file, 'wb') as picklefile:
                pickle.dump(episodes_list, picklefile)

            r = 0.5 * np.random.randn(1) + 2
            time.sleep(r)

    return None


# Scrape MSNBC:


def scrape_MSNBC_transcripts(filename=data_path + 'msnbc_transcripts2.pkl'):
    """
    Scrape transcripts of MSNBC's `Rachel Maddow Show` and `The Last Word with
    Lawrence O'Donnel`. Stores transcripts in a dictionary with the following
    structure: {'show': show (str),
                'title': title (str),
                'date': air date (str),
                'url': url of transcript (str),
                'transcript': transcript (str)}

    :param filename: str.
    :return: None
    """

    root_urls = {'Maddow': 'http://www.msnbc.com/transcripts/rachel-maddow-show/',
                 'ODonnel': 'http://www.msnbc.com/transcripts/the-last-word/'}

    # episodes_list = []

    for show, root_url in root_urls.items():
        show_links = []
        print()
        print(show, root_url)
        for month in ['2018/5', '2018/4', '2018/3', '2018/2', '2018/1', '2017/12',
                      '2017/11']:  # ,'2017/10','2017/9']:
            print(month)
            url = root_url + month
            soup = get_soup(url)

            for link in soup.find('div', class_='item-list').find_all('a',
                                                                      href=True):
                print('Link:', link)
                episode_url = 'http://www.msnbc.com' + link['href']
                show_links.append(episode_url)

                # Get Soup object for episode's transcript page:
                episode_soup = get_soup(episode_url)

                # Get episode transcript text:
                transcript = episode_soup.find(itemprop='articleBody').get_text()

                # Get episode title:
                headline = episode_soup.find(itemprop='headline').get_text()
                title = headline.split('TRANSCRIPT')[0]

                ep = {'show': show,
                      'title': title,
                      'date': episode_url.split('/')[-1][:10].replace('-', '/'),
                      'url': episode_url,
                      'transcript': transcript}

                episodes_list.append(ep)

                with open(filename, 'wb') as picklefile:
                    pickle.dump(episodes_list, picklefile)

                r = 0.5 * np.random.randn(1) + 2
                time.sleep(r)

    return None


def main(scrape_fresh=False):
    """
    Load, or scrape and load, Fox and MSNBC transcripts.

    :param scrape_fresh: bool.
    :return: list of dictionaries.
    """
    fox_filename = data_path + 'fox_news_transcripts3.pkl'
    msnbc_filename = data_path + 'msnbc_transcripts2.pkl'

    if scrape_fresh:

        scrape_FOX_transcript_urls(filename=data_path + 'fox_news_episode_links.pkl')

        scrape_FOX_transcripts(from_file=data_path + 'fox_news_episode_links.pkl',
                               to_file=fox_filename)

        scrape_MSNBC_transcripts(filename=msnbc_filename)

    with open(fox_filename, 'rb') as picklefile:
        fox_transcripts = pickle.load(picklefile)

    with open(msnbc_filename, 'rb') as picklefile:
        msnbc_transcripts = pickle.load(picklefile)

    transcripts = msnbc_transcripts + fox_transcripts

    return transcripts


if __name__ == '__main__':

    main()

