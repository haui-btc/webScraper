from email.mime.text import MIMEText
# this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP_SSL as SMTP
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import sys
import os
import re
import time

# Scraping dynatrace releasenotes
# OneAgent: https://www.dynatrace.com/support/help/whats-new/release-notes/oneagent
# ActiveGate: https://www.dynatrace.com/support/help/whats-new/release-notes/activegate
# API: https://www.dynatrace.com/support/help/whats-new/release-notes/dynatrace-api

latest_release_url = ""

def get_website_info():
    baseURL = 'https://www.dynatrace.com'
    apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
    oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
    agURL = baseURL + '/support/help/whats-new/release-notes//activegate'
    # ===========================================================================
    # session erstellen
    session1 = HTMLSession()
    # mit session auf website zugreifen
    page1 = session1.get(apiURL)
    # JS part der website ausführen (render zu html)
    page1.html.render()
    # Website lesen mit Beautifulsoup > hmtl parser
    soup1 = BeautifulSoup(page1.html.html, 'html.parser')
    # Suche nach gewünschter ID (Inspect tool auf gew. Website verwenden)
    results = soup1.find_all(
        lambda tag: tag.name == 'a' and tag.get('class') == ['anchor'])

    # für email
    releases = []
    for result in results:
        release = {}
        release['name'] = result.text
        release['url'] = baseURL + result['href']
        releases.append(release)
    return releases

# ===========================================================================

# Email
def send_mail():
    SMTPserver = 'mail.gmx.net'
    sender = 'monitoring.analytics@gmx.ch'
    destination = ['sascha.hauenstein@pm.me']

    USERNAME = "monitoring.analytics@gmx.ch"
    PASSWORD = "Monitoring2023!"

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content = latest_release_url

    subject = "Dynatrace: New API version"

    # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender  # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.quit()
    except:
        sys.exit("mail failed; %s" % "CUSTOM_ERROR")  # give an error message


get_website_info()
time.sleep(5)
send_mail()