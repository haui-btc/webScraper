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

# create logger
logging.basicConfig(filename='web_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("script started")

# URLs
baseURL = 'https://www.dynatrace.com'
apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
agURL = baseURL + '/support/help/whats-new/release-notes//activegate'

# Webscraping
def get_api_release_notes():
    try:
        logging.info("start HTML session")
        session = HTMLSession()
        logging.info("store " + apiURL + " in session")
        page = session.get(apiURL)
        logging.info("render html")
        page.html.render()
        logging.info("parse html with BeatifulSoup")
        soup = BeautifulSoup(page.html.html, 'html.parser')
        logging.info("grep defined html elements")
        results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class')==['anchor'])
        releases = []
        logging.info("grep name and url")
        for result in results:
            release = {}
            release['name'] = result.text
            release['url'] = baseURL + result['href']
            releases.append(release)
        return releases
    except RequestException as e:
        logging.error(f"An error occurred while making the request: {e}")        
        return None
    except Exception as e:        
        logging.error(f"An unexpected error occurred: {e}")
        return None

# Email-Settings
def send_email():
    SMTPserver = 'mail.gmx.net'
    sender = 'monitoring.analytics@gmx.ch'
    destination = ['haui_btc@protonmail.com']
    USERNAME = "monitoring.analytics@gmx.ch"
    PASSWORD = "Monitoring2023!"

    # get date    
    date = datetime.datetime.now()
    date = date.strftime("%d. %B %Y")

    # grep latest release
    logging.info("run function: 'get_api_release_notes'")
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
                logging.info("sending email to: " + destination[0])
                conn.sendmail(sender, destination, msg.as_string())
                conn.quit()
                break
            except (smtplib.SMTPException, ConnectionRefusedError) as e:
                logging.error(f"Failed to send email: {str(e)}. Retrying in {delay} seconds...")
                retries -= 1
                time.sleep(delay)
        
        if retries == 0:
            raise Exception("Failed to send email after multiple attempts. Exiting script.")
        
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

# activate function for testing
send_email() 