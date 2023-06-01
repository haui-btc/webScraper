import logging
import hashlib
import time
import sys
import urllib.error
from urllib.request import Request, urlopen
from urllib.error import URLError
from requests.exceptions import RequestException
from scraper_email import send_email
import configparser
import requests
from bs4 import BeautifulSoup
import time

# get config
config = configparser.ConfigParser()
config.read('config.ini')

# logging 
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
	filename='web-scraper.log', 
	filemode='w', 
	level=logging.INFO)

# The URL of the website and the table selector
#table_selector = 
url = config.get('URL', 'monitor')


# The initial content of the table
previous_content = ""

while True:
    # Send a GET request to the website
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the table element using the selector
    #table = soup.select_one(table_selector)
    table = soup.find_all(lambda tag: tag.get('class')==['table'])
    # Get the current content of the table
    current_content = str(table)
    
    # Compare the current content with the previous content
    if current_content != previous_content:
        print("Table content changed!")
        # Do something here, such as sending an email or a notification        
    
        # Update the previous content
        previous_content = current_content

    else:
        print(f'No changes detected')
    
    # Wait for some time before checking again
    time.sleep(10)
