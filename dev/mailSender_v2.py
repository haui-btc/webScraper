import requests 
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sys
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP

# Scraping dynatrace releasenotes
# OneAgent: https://www.dynatrace.com/support/help/whats-new/release-notes/oneagent
# ActiveGate: https://www.dynatrace.com/support/help/whats-new/release-notes/activegate
# API: https://www.dynatrace.com/support/help/whats-new/release-notes/dynatrace-api

baseURL = 'https://www.dynatrace.com'
apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
agURL = baseURL + '/support/help/whats-new/release-notes//activegate'
#===========================================================================

#WebScraper API-Versions

def get_latest_release_url_api(apiURL, baseURL):
    session = HTMLSession()
    page = session.get(apiURL)
    page.html.render()
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['anchor'])
    latest_release = results[0]
    latest_release_url = baseURL + latest_release['href']
    return latest_release_url

#===========================================================================

#WebScraper OneAgent-Versions

def get_latest_release_url_oa(oaURL, baseURL):
    session = HTMLSession()
    page = session.get(oaURL)
    page.html.render()
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['anchor'])
    latest_release = results[0]
    latest_release_url = baseURL + latest_release['href']
    return latest_release_url

#===========================================================================

#WebScraper ActiveGate-Versions

latest_release_url = ""

def get_latest_release_url_ag(agURL, baseURL):
    session = HTMLSession()
    page = session.get(agURL)
    page.html.render()
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') == ['anchor'])
    latest_release = results[0]
    latest_release_url = baseURL + latest_release['href']
    return latest_release_url

#===========================================================================

# Email

content = latest_release_url
subject = "New Releases Available"

def send_email(content, subject):
    SMTPserver = 'mail.gmx.net'
    sender =     'sascha.hauenstein@gmx.ch'
    destination = ['sascha.hauenstein@pm.me']

    USERNAME = "sascha.hauenstein@gmx.ch"
    PASSWORD = "Mueterfigger69!"
    text_subtype = 'plain'

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except:
        sys.exit("mail failed; %s" % "CUSTOM_ERROR")