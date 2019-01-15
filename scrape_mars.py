from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd

def scrape():

    nasa_url = 'https://mars.nasa.gov/news/'
    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='slide')[0]
    news_title = results.find('div', class_='content_title').a.text
    news_p = results.find('div', class_='rollover_description_inner').text

    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    # !which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16729_hires.jpg"

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    most_recent_tweet = soup.find_all('div', class_='tweet')[0]
    mars_weather = most_recent_tweet.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    mars_df = pd.read_html("http://space-facts.com/mars/")[0]
    mars_df.columns = ['Description', 'Value']
    mars_table = mars_df.to_html(escape=False)

    mars_facts = {}
    mars_facts['title'] = news_title
    mars_facts['description'] = news_p
    mars_facts['featured image'] = featured_image_url
    mars_facts['tweet'] = mars_weather
    mars_facts['table'] = mars_table

    return mars_facts
