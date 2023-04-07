# webScraper
> Monitors a website for changes by comparing the hash of the website's content
    at different times and send an email if anything changes.
```bash
.
|-- Dockerfile
|-- README.md
|-- __pycache__
|   |-- email.cpython-311.pyc
|   `-- releasenoteScraper.cpython-311.pyc
|-- app
|   |-- __pycache__
|   |   |-- releasenoteScraper.cpython-311.pyc
|   |   `-- scraper_email.cpython-311.pyc
|   |-- monitor.py
|   `-- scraper_email.py
|-- config.ini
|-- config.template
|-- docker-compose.debug.yml
|-- docker-compose.yml
`-- requirements.txt

3 directories, 13 files
```

## config.template

Change values and rename file to config.ini

```bash
[EMAIL]
SMTPserver = mail.xyz.net
sender = mail@mail.net
destination = mail@mail.net
USERNAME = mail@mail.net
PASSWORD = <pwd>

retries = <int>
# delay after smtp-connection retry in seconds
delay = <int>

[INTERVALL]
# website monitoring frequence in seconds
intervall = <int>

[URL] 
# website to monitor
monitor = <url>
```
