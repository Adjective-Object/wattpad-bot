#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

r = requests.get("http://computoser.com/")
b = BeautifulSoup(r.text);

dllink = b.find(id="downloadMp3Link")['href']

print dllink
