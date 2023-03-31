import requests 
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP
import sys
import os
import re
import datetime

# URLs
baseURL = 'https://www.dynatrace.com'
apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
agURL = baseURL + '/support/help/whats-new/release-notes//activegate'

# Webscraping
def get_api_release_notes():
    session = HTMLSession()
    page = session.get(apiURL)
    page.html.render()
    soup = BeautifulSoup(page.html.html, 'html.parser')
    results = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class')==['anchor'])
    releases = []
    for result in results:
        release = {}
        release['name'] = result.text
        release['url'] = baseURL + result['href']
        releases.append(release)
    return releases

# Email-Settings
def send_email():
    SMTPserver = 'mail.gmx.net'
    sender = 'monitoring.analytics@gmx.ch'
    destination = ['sascha.hauenstein@pm.me']
    USERNAME = "monitoring.analytics@gmx.ch"
    PASSWORD = "Monitoring2023!"

    # grep all releases
    """ releases = get_api_release_notes()

    content = "New API releases:\n"
    for release in releases:
        content += "\n- {} ({})".format(release['name'], release['url']) """

    # get date
    date = datetime.datetime.now()
    date = date.strftime("%d. %B %Y")

    # grep latest release
    releases = get_api_release_notes()
    latest_release = releases[0]
    latest_release_name = latest_release['name']
    latest_release_url = latest_release['url']

    # Email content
    content = f"Hi there, \n\n a new API release is available. \n\n {date}: \n {latest_release_name} \n {latest_release_url} \n\n All releases:\n {apiURL}"

    text_subtype = 'plain'
    
    subject = "Dynatrace: New API version"

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']= subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()

    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message

send_email()

