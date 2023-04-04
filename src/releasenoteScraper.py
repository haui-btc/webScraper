import requests 
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
import smtplib
import sys
import os
import re
import datetime
from requests.exceptions import RequestException
import logging
import time
import configparser

# get config infos
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
	filename='web-scraper.log', 
	filemode='w', 
	level=logging.INFO)

# URLs
baseURL = 'https://www.dynatrace.com'
apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
#oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
#agURL = baseURL + '/support/help/whats-new/release-notes//activegate'

# Webscraping function
logging.info("start scraping process")

def get_api_release_notes():
    try:
        # Initializing a new session with the website to be scraped
        logging.info("new HTML session")
        session = HTMLSession()

        # Sending a GET request to the API's URL and storing the response in a variable named 'page'
        logging.info("get " + apiURL)
        page = session.get(apiURL)

        # Rendering the HTML content of the page using the built-in method of the library
        logging.info("render html")
        page.html.render()

        # Parsing the HTML content of the page using BeautifulSoup and storing the result in a variable named 'soup'
        logging.info("parse html with BeatifulSoup")        
        soup = BeautifulSoup(page.html.html, 'html.parser')

        # lambda function: searching for all HTML tags with 'a' and class 'anchor' and store the result in a variable
        logging.info("grep defined html elements")        
        results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class')==['anchor'])

        # Initializing an empty list named 'releases' to store the release notes
        releases = []

        # Looping through all the search results and extracting the release names and URLs and appending them to the 'releases' list
        logging.info("grep name and url")
        for result in results:
            release = {}
            release['name'] = result.text
            release['url'] = baseURL + result['href']
            releases.append(release)

        # Returning the list of extracted release notes    
        return releases
    
    # Handling any requests exceptions and logging an error message with the specific error message
    except RequestException as e:
        logging.error(f"An error occurred while making the request: {e}", exc_info=True)        
        return None
    
    # Handling any other unexpected exceptions and logging an error message with the specific error message
    except Exception as e:        
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return None

# Email
def send_email():
    SMTPserver = config.get('EMAIL', 'SMTPserver')
    sender = config.get('EMAIL', 'sender')
    destination = config.get('EMAIL', 'destination')
    USERNAME = config.get('EMAIL', 'USERNAME')
    PASSWORD = config.get('EMAIL', 'PASSWORD')

    # get date    
    date = datetime.datetime.now()
    date = date.strftime("%d. %B %Y")

    # grep latest release    
    releases = get_api_release_notes()
    logging.info("grep latest release")
    latest_release = releases[0]
    latest_release_name = latest_release['name']
    latest_release_url = latest_release['url']

    # Email content
    logging.info("create email content with latest release info")
    content = f"Hi there, \n\n a new API release is available. \n\n {date}: \n {latest_release_name} \n {latest_release_url} \n\n All releases:\n {apiURL}"
    text_subtype = 'plain'    
    subject = "Dynatrace: New API version"

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        retries = 3
        delay = 5 # seconds
        while retries:
            try:
                logging.info("connecting to smtp-server: " + SMTPserver)
                conn = SMTP(SMTPserver)
                conn.set_debuglevel(False)
                conn.login(USERNAME, PASSWORD)
                logging.info("sending email")
                conn.sendmail(sender, destination, msg.as_string())
                conn.quit()
                break
            except (smtplib.SMTPException, ConnectionRefusedError) as e:
                logging.error(f"Failed to send email: {str(e)}. Retrying in {delay} seconds...")#, exc_info=True)
                retries -= 1
                time.sleep(delay)
        
        if retries == 0:
            raise Exception("Failed to send email after multiple attempts. Exiting script.")#, exc_info=True)
        
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}", exc_info=True)

# activate function for testing
#send_email() 