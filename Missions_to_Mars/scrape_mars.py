from splinter import Browser
from bs4 import BeautifulSoup as bs
import time

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

    scraped_mars = []
    articles = {}

    # Visit Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(2)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve all elements that contain articles information
    infos = soup.find_all('div', class_="list_text")

    for info in infos:
        title = info.find('a').text.strip()
        paragraph = info.find( class_='article_teaser_body').text.strip()
        articles.update( {title : paragraph} )
    # scraped_mars = {
    #     "sloth_img": titles,
    #     "min_temp": paragraphs,
    # }
    
    for item in articles:
        scraped_mars.append({"art_title":item, "art_paragraph":articles[item]})
    
#     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit'
#     browser.visit(url)

#     time.sleep(3)

#     featured_image_urls = []
#     # HTML object
#     html = browser.html
# # Parse HTML with Beautiful Soup
#     soup = bs(html, 'html.parser')

# # Retrieve all elements that contain articles information
#     infos = soup.find_all('div', class_="img")

#     for info in infos:
#         link = info.find('img')
#         href = link['src']
#         featured_image_urls.append('https://www.jpl.nasa.gov' + href)

#     for item in featured_image_urls:
#         scraped_mars.append({"featured_image_url":item})

#     mars_weather = []
#     url = 'https://twitter.com/marswxreport?lang=en'
#     browser.visit(url)
#     time.sleep(4)

#     html = browser.html
#     # Parse HTML with Beautiful Soup
#     soup = bs(html, 'html.parser')

#     # Retrieve all elements that contain articles information
#     infos = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

#     for info in infos: 
#         weather = info.text.strip()
#         if (weather!="" and weather[0]=='I'):
#             mars_weather.append(weather)

#     for item in  mars_weather:
#         scraped_mars.append({"mars_weather":item})
    
#     import pandas as pd
#     url = 'https://space-facts.com/mars/'
#     tables = pd.read_html(url)
#     mars_facts_df = tables[0]
#     mars_facts_df = mars_facts_df.rename(columns={0:"Parameter", 1:"Value"})

#     params = mars_facts_df['Parameter'].to_list()
#     values = mars_facts_df['Value'].to_list()

#     for item in params:
#         scraped_mars.append({"param":item})
#     for item in values:
#         scraped_mars.append({"prama_value":item})

#     hemisph_images = {}
#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(url)
#     time.sleep(5)

#     html = browser.html
# # Parse HTML with Beautiful Soup
#     soup = bs(html, 'html.parser')

# # Retrieve all elements that contain articles information
#     infos = soup.find_all('div', class_="item")

#     for info in infos:
#         link = info.find('img')
#         href = link['src']
#         description = info.find('div', class_="description")
#         h3 = description.find('h3').text.strip()
#         hemisph_images.update( {h3 : 'https://astrogeology.usgs.gov' + href} )
    
#     for item in hemisph_images:
#         scraped_mars.append({"high_res_title":item, "high_res_img_url":hemisph_images[item]})
 
    # Close the browser after scraping
    browser.quit()

    # Return results
    return scraped_mars


