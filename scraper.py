from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import csv
import scraperwiki
import sys
import requests
import re
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding("utf-8")


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

# check the downloads page for the latest release (assumed to be the first download button we find)
page = requests.get("https://grid.ac/downloads")
soup = BeautifulSoup(page.content, 'html.parser')

downloads = soup.find_all(text=re.compile('Download release'))
link = "https:"+downloads[0].parent['href']

# Visit the doi on figshare and get the download link
page = requests.get(link)
soup = BeautifulSoup(page.content, 'html.parser')
downloads = soup.find_all('a', class_='download-button')
download_link = downloads[0]['href']



# Download the zip and load in the institutes CSV to the database
url = urlopen(download_link)
zipfile = ZipFile(StringIO(url.read()))


reader = unicode_csv_reader(zipfile.open("full_tables/institutes.csv"))
next(reader, None)  # skip the headers
for row in reader:
  scraperwiki.sqlite.save(unique_keys=['grid_id'], data={"grid_id": row[0], "name": row[1], "wikipedia_url": row[2], "email_address": row[3], "established":row[4]})
