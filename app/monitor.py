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
    Monitors a website for changes by comparing the hash of the website's content
    at different times.
    
    Parameters:
    url (str): The URL of the website to monitor.
    
    Returns:
    None
    """     
    url = config.get('URL', 'monitor')
    intervall = config.get('INTERVALL', 'intervall')

    try:
        # setting the URL you want to monitor
        logging.info("reading defined url")
        url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        # to perform a GET request and load the content of the website and store it in a var
        logging.info("GET request")
        response = urlopen(url).read()

    except RequestException as e:
        logging.error(f"An error occurred while making the request: {e}", exc_info=True)    
        logging.error("exiting the script")
        sys.exit(1) # Exit the script with a non-zero exit code

    except Exception as e:        
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)    
        logging.error("exiting the script")
        sys.exit(1) # Exit the script with a non-zero exit code  
    
    except KeyboardInterrupt as ex:
        print('goodbye!')
        logging.error("adios! exiting the script")
        sys.exit(1) # Exit the script with a non-zero exit code  

    # to create the initial hash
    logging.info("create initial hash")
    currentHash = hashlib.sha224(response).hexdigest()
    print("running")
    logging.info("wait 10 seconds")
    time.sleep(10)
    while True:
        try:
            # perform the get request and store it in a var
            logging.info("GET request")
            response = urlopen(url).read()

            # create a hash
            logging.info("create hash")
            currentHash = hashlib.sha224(response).hexdigest()        

            # wait for X seconds
            logging.info("wait " + intervall + " seconds")
            time.sleep(int(intervall))

            # perform the get request
            logging.info("GET request")
            response = urlopen(url).read()

            # create a new hash
            logging.info("create new hash")
            newHash = hashlib.sha224(response).hexdigest()   
        
            # check if new hash is same as the previous hash
            if newHash == currentHash:
                print("compare hashes: no changes")    
                logging.info("compare hashes: no changes")        
                continue                

            # if something changed in the hashes
            else:
                # notify
                print("compare hashes: detected changes, sending email")
                logging.info("compare hashes: detected changes")
                send_email()

                # again read the website
                logging.info("GET request")
                response = urlopen(url).read()            

                # create a hash
                logging.info("create current hash")
                currentHash = hashlib.sha224(response).hexdigest()            

                # wait for X seconds
                logging.info("wait " + intervall + " seconds")
                time.sleep(int(intervall))  
                continue                

        # To handle exceptions
        except URLError as e:
            logging.error(f"Failed to load URL: {e}", exc_info=True)    
            logging.error("exiting the script")
            sys.exit(1) # Exit the script with a non-zero exit code        
    
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)    
            logging.error("exiting the script")
            sys.exit(1) # Exit the script with a non-zero exit code
            
        except KeyboardInterrupt as ex:
            print("adios!")
            logging.error("adios! exiting the script")
            sys.exit(1) # Exit the script with a non-zero exit code  
        

if __name__ == "__main__":
    website_monitor()
