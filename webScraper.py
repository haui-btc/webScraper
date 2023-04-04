# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from src.releasenoteScraper import *
import logging
import sys
import urllib.error
from requests.exceptions import RequestException

# create logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
	filename='web-scraper.log', 
	filemode='w', 
	level=logging.INFO)

logging.info("script started")

try:
    # setting the URL you want to monitor
    logging.info("reading defined url")
    url = Request('https://www.20min.c', headers={'User-Agent': 'Mozilla/5.0'})

    # to perform a GET request and load the content of the website and store it in a var
    logging.info("GET request")
    response = urlopen(url).read()
    
except RequestException as e:
    logging.error(f"An error occurred while making the request: {e}")
    logging.error("exiting the script")
    sys.exit(1) # Exit the script with a non-zero exit code

except Exception as e:        
    logging.error(f"An unexpected error occurred: {e}", exc_info=True)   
    logging.error("exiting the script")
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

		# wait for 30 seconds
		logging.info("wait 30 seconds")
		time.sleep(30)		

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

			# wait for 30 seconds
			logging.info("wait 30 seconds")
			time.sleep(30)			
			continue

	# To handle exceptions
	except urllib.error.URLError as e:
		logging.error(f"Failed to load URL: {e}", exc_info=True)	
		logging.error("exiting the script")
		sys.exit(1) # Exit the script with a non-zero exit code		
    
	except Exception as e:
		logging.error(f"An error accurred: {e}", exc_info=True)	
		logging.error("exiting the script")
		sys.exit(1) # Exit the script with a non-zero exit code


		