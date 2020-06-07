from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import random

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scraper():
    browser = init_browser()
    sec = random.randint(2, 7)
    i1 = random.randint(0, 39)
    i2 = random.randint(0, 31)

    # Visit Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(sec)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve all elements that contain articles information
    info = soup.find_all('div', class_="list_text")
    
#    for info in infos:
    try:
        title = info[i1].find('a').text.strip()
        paragraph = info[i1].find( class_='article_teaser_body').text.strip()
    except IndexError:
        title = info[0].find('a').text.strip()
        paragraph = info[0].find( class_='article_teaser_body').text.strip()

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit'
    browser.visit(url)

    time.sleep(sec)

#     HTML object
    html = browser.html
#  Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

#  Retrieve all elements that contain articles information
    info = soup.find_all('div', class_="img")
    try:
        link = info[i2].find('img')
    except IndexError:
        link = info[0].find('img')

    href = link['src']
    img_link = 'https://www.jpl.nasa.gov' + href


    mars_weather = []
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(sec)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve all elements that contain articles information
    infos = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    for info in infos: 
        weather = info.text.strip()
        if (weather!="" and weather[0]=='I'):
            post = weather[8:]
            mars_weather.append(post)
    
    i3 = random.randint(0, (len(mars_weather)-1)) 
    try:    
        found_mars_weather = mars_weather[i3]
    except ValueError:
        found_mars_weather="scrape one more time for weather post"

    mars_facts = {}

    import pandas as pd
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df = mars_facts_df.rename(columns={0:"Parameter", 1:"Value"})
    params = mars_facts_df['Parameter'].to_list()
    values = mars_facts_df['Value'].to_list()

    for i in range(len(params)):
        mars_facts.update( {params[i] : values[i]} )
   

    hemisph_images = {}
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(sec)

    html = browser.html
 # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

 # Retrieve all elements that contain articles information
    infos = soup.find_all('div', class_="item")

    for info in infos:
        description = info.find('div', class_="description")
        h3 = description.find('h3').text.strip()
        link = info.find('a')
        href = link['href']
    
        url_full = 'https://astrogeology.usgs.gov' + href
    
        browser.visit(url_full)
        time.sleep(2)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        info_image = soup.find_all('img', class_="wide-image")
    
        href_full =  info_image[0]['src']
        hemisph_images.update( {h3 : 'https://astrogeology.usgs.gov' + href_full} )
    
    
    scraped_mars = {
        "titles": title,
        "paragraphs": paragraph,
        "featured_image_url": img_link,
        "weather": found_mars_weather,
        "mars_facts": mars_facts,
        "hemisph_images": hemisph_images
    }
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return scraped_mars


