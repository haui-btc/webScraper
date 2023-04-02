# Importing libraries
import time
import hashlib
from urllib.request import urlopen, Request
from releasenoteScraper import *
import logging

# create logger
logging.basicConfig(filename='website_changes.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# setting the URL you want to monitor
url = Request('https://www.20min.ch/',
			headers={'User-Agent': 'Mozilla/5.0'})

# to perform a GET request and load thegi
# content of the website and store it in a var
response = urlopen(url).read()

# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
logging.info("Website monitor started")
print("running")
time.sleep(10)
while True:
	try:
		# perform the get request and store it in a var
		response = urlopen(url).read()
		logging.info("reading url")

		# create a hash
		currentHash = hashlib.sha224(response).hexdigest()
		logging.info("create current hash")

		# wait for 30 seconds
		time.sleep(30)
		logging.info("wait 3o seconds")

		# perform the get request
		response = urlopen(url).read()
		logging.info("reading url")

		# create a new hash
		newHash = hashlib.sha224(response).hexdigest()
		logging.info("create new hash")

		# check if new hash is same as the previous hash
		if newHash == currentHash:
			logging.info("compare hashes: no changes")
			continue	
			

		# if something changed in the hashes
		else:
			# notify
			print("detected changes on website, sending email")
			logging.info("compare hashes: detected changes, sending email")
			send_email()

			# again read the website
			response = urlopen(url).read()
			logging.info("reading url")

			# create a hash
			currentHash = hashlib.sha224(response).hexdigest()
			logging.info("create current hash")

			# wait for 30 seconds
			time.sleep(30)
			logging.info("wait 3o seconds")
			continue

	# To handle exceptions
	except Exception as e:
		logging.error("Error occurred")
		logging.exception('')
		print("error")