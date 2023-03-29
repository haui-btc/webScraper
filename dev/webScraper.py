# Scraping dynatrace releasenotes
# OneAgent: https://www.dynatrace.com/support/help/whats-new/release-notes/oneagent
# ActiveGate: https://www.dynatrace.com/support/help/whats-new/release-notes/activegate
# API: https://www.dynatrace.com/support/help/whats-new/release-notes/dynatrace-api

import requests 
from requests_html import HTMLSession
from bs4 import BeautifulSoup


baseURL = 'https://www.dynatrace.com'
apiURL = baseURL + '/support/help/whats-new/release-notes/dynatrace-api'
oaURL = baseURL + '/support/help/whats-new/release-notes//oneagent'
agURL = baseURL + '/support/help/whats-new/release-notes//activegate'

# session erstellen
session1 = HTMLSession()

# mit session auf website zugreifen
page1 = session1.get(apiURL)

# JS part der website ausführen (render zu html)
page1.html.render()

# Website lesen mit Beautifulsoup > hmtl parser
soup1 = BeautifulSoup(page1.html.html, 'html.parser')

# Suche nach gewünschter ID (Inspect tool auf gew. Website verwenden)
results = soup1.find_all(lambda tag: tag.name == 'a' and tag.get('class')==['anchor'])

# Alle Links der Versionen
""" for a in results:
        print(baseURL + a['href']) """

# für email
# Get the latest release and its URL
latest_release = results[0]
latest_release_url = baseURL + latest_release['href']

# Print the latest release and its URL
print(f"The latest release is: {latest_release.text}\n")
print(f"{latest_release_url}\n")






