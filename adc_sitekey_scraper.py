from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as bs
import requests
import sys

links = [
    'http://www.adidas.com/us/men-shoes-new_arrivals?sz=48&start=0',
    'http://www.adidas.com/us/women-shoes-new_arrivals?sz=48&start=0',
    'http://www.adidas.com/us/men-shoes-new_arrivals?sz=48&start=0&srule=top-sellers',
    'http://www.adidas.com/us/women-shoes-new_arrivals?sz=48&start=0&srule=top-sellers',
]

product_selector = '.image a'  # selector on the product page for the individual links
product_links = []  # placeholder for the individual product links

captcha_class = '.g-recaptcha'  # selector for the site-key placeholder
site_key = 'data-sitekey'  # element attribute to get the site-key


# Gets a new html session
def new_session(url):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36',
        'X-XHR-Referer': 'http://www.adidas.com/us',
        'Referer': 'http://www.adidas.com/us',
        'Accept': 'text/html, application/xhtml+xml, application/xml',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8,da;q=0.6',
        'DNT': '1'
    })
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    return soup


# Scrapes category pages for product links with the selector for the anchor tag
def category_scraper(url, selector):
    category = new_session(url)
    for link_src in category.select(selector):
        product_links.append(link_src['href'])
    return product_links


# Scrapes individual product pages for a captcha token
def sitekey_scraper(url):
    product = new_session(url)
    selector_captcha = product.find_all(attrs={"class": "g-recaptcha"})
    if selector_captcha:
        captcha_attribute = selector_captcha[0]['data-sitekey']
        if captcha_attribute:
            print("!!!!!!!!!!!!!Key Found on " + url + "!!!!!!!!!!!!")
            return captcha_attribute
    else:
        print("Not found")
        return


# Loops through the list of product categories and store the links in the all_list object
for link in links:
    print("Gathering products links from " + link)
    product_links = category_scraper(link, product_selector)

# Checks the individual products for the recaptcha sitekey
print("Found " + str(len(product_links)) + " product links")
print("Starting site-key scraper")
index = 0
for product in product_links:
    index += 1
    print(str(index) + " of " + str(len(product_links)) + " :Checking for site key in: " + str(product))
    site_key_results = sitekey_scraper(str(product))
    if site_key_results:
        print("")
        print("Recaptcha Sitekey:")
        print("")
        print(str(site_key_results))
        break
    else:
        continue
