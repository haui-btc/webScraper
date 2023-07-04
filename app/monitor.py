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
from bs4 import BeautifulSoup

# get config
config = configparser.ConfigParser()
config.read('config.ini')

# logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='web-scraper.log',
                    filemode='w',
                    level=logging.INFO)


def website_monitor():
    """
    Monitors a website for changes by comparing the hash of a specific HTML table's content
    at different times.

    Parameters:
    url (str): The URL of the website to monitor.

    Returns:
    None
    """
    url = config.get('URL', 'monitor')
    intervall = config.get('INTERVALL', 'intervall')

    # setting the URL you want to monitor
    logging.info("reading defined url")
    url_request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Initialize hash
    currentHash = None
    newHash = None

    while True:
        try:
            # to perform a GET request and load the content of the website and store it in a var
            logging.info("GET request")
            response = urlopen(url_request).read()

            # parse the HTML and get the first table's HTML as a string
            logging.info("parsing HTML")
            soup = BeautifulSoup(response, 'lxml')
            table_html = str(soup.find('table'))

            # create a new hash
            logging.info("create new hash")
            newHash = hashlib.sha224(table_html.encode()).hexdigest()

            # check if new hash is same as the previous hash
            if currentHash is not None and newHash == currentHash:
                print("compare hashes: no changes")
                logging.info("compare hashes: no changes")
            # if something changed in the hashes and this is not the first iteration
            elif currentHash is not None and newHash != currentHash:
                # notify
                print("compare hashes: detected changes, sending email")
                logging.info("compare hashes: detected changes")
                send_email()

            # update currentHash
            currentHash = newHash

            # wait for X seconds
            logging.info("wait " + intervall + " seconds")
            time.sleep(int(intervall))

        # To handle exceptions
        except URLError as e:
            logging.error(f"Failed to load URL: {e}", exc_info=True)
            logging.error("exiting the script")
            sys.exit(1)  # Exit the script with a non-zero exit code

        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            logging.error("exiting the script")
            sys.exit(1)  # Exit the script with a non-zero exit code

        except KeyboardInterrupt as ex:
            print("adios!")
            logging.error("adios! exiting the script")
            sys.exit(1)  # Exit the script with a non-zero exit code


if __name__ == "__main__":
    website_monitor()
