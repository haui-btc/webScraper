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

# get config
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
	filename='web-scraper.log', 
	filemode='w', 
	level=logging.DEBUG)

# URLs
baseURL = 'https://www.dynatrace.com'
saasURL = baseURL + "/support/help/whats-new/release-notes/saas"
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
        logging.info("get " + saasURL)
        page = session.get(saasURL)

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
    
    except KeyboardInterrupt as ex:
        print("adios!")
        logging.error("adios! exiting the script")
        sys.exit(1) # Exit the script with a non-zero exit code  
    

# Email
def send_email():
    SMTPserver = config.get('EMAIL', 'SMTPserver')
    sender = config.get('EMAIL', 'sender')
    destination = config.get('EMAIL', 'destination')
    USERNAME = config.get('EMAIL', 'USERNAME')
    PASSWORD = config.get('EMAIL', 'PASSWORD')

    # get date    
    date = datetime.datetime.now()
    date = date.strftime("%d.%m.%Y")


    # grep latest release    
    releases = get_api_release_notes()
    logging.info("grep latest release")
    latest_release = releases[0]
    latest_release_name = latest_release['name']
    latest_release_url = latest_release['url']

    # Email content
    logging.info("create email content with latest release info")
    content = f"{date}\n\n\nHi there,\n\na new Dynatrace SaaS release is available.\n\n{latest_release_name}:\n{latest_release_url}\n\nAll SaaS releases:\n{saasURL}"
    text_subtype = 'plain'    
    subject = "Dynatrace: New SaaS release"

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        retries = int(config.get('EMAIL','retries'))
        delay = int(config.get('EMAIL','delay'))
        while retries:
            try:
                logging.info("connecting to smtp-server: " + SMTPserver)
                conn = SMTP(SMTPserver)
                conn.set_debuglevel(False)
                conn.login(USERNAME, PASSWORD)
                logging.info("sending email")
                conn.sendmail(sender, destination, msg.as_string())
                logging.info("email sent successfully")                
                conn.quit()
                break
            
            except (smtplib.SMTPException, ConnectionRefusedError) as e:
                logging.error(f"Failed to send email: {str(e)}. Retrying in {delay} seconds...")#, exc_info=True)
                retries -= 1
                time.sleep(delay)
            
            except KeyboardInterrupt as ex:
                print("adios!")
                logging.error("adios! exiting the script")
                sys.exit(1) # Exit the script with a non-zero exit code                                             
        
        if retries == 0:
            raise Exception("Failed to send email after multiple attempts. Exiting script.")#, exc_info=True)
            logging.error("exiting the script")
            
    
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}", exc_info=True)
        sys.exit(1) # Exit the script with a non-zero exit code 

    except KeyboardInterrupt as ex:
        print("adios!")
        logging.error("adios! exiting the script")
        sys.exit(1) # Exit the script with a non-zero exit code  

# activate function for testing
#send_email() 