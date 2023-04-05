# webScraper
> Monitor a website and send an email if anything changes.
```bash
.
|-- Dockerfile
|-- README.md
|-- __pycache__
|   |-- email.cpython-311.pyc
|   `-- releasenoteScraper.cpython-311.pyc
|-- config.template
|-- requirements.txt
`-- src
    |-- __pycache__
    |   |-- releasenoteScraper.cpython-311.pyc
    |   `-- scraper_email.cpython-311.pyc
    |-- monitor.py
    `-- scraper_email.py

3 directories, 10 files
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

[INTERVALL]
intervall = 60
```
