# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import csv
import scraperwiki
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

url = urlopen("https://ndownloader.figshare.com/files/8500607")
zipfile = ZipFile(StringIO(url.read()))


reader = unicode_csv_reader(zipfile.open("full_tables/institutes.csv"))
for row in reader:
  scraperwiki.sqlite.save(unique_keys=['grid_id'], data={"grid_id": row[0], "name": row[1], "wikipedia_url": row[2], "email_address": row[3], "established":row[4]})
