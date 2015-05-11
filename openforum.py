#!/usr/bin/python

# open 'Discuss this topic' links

from sys import argv
from os import remove
from bs4 import BeautifulSoup
import webbrowser

if len(argv) != 2:
	raise SystemExit('SYNTAX: python openforum.py PATH')

with open(argv[1], 'r') as f:
	c = f.read()

soup = BeautifulSoup(c)
hrefs = []
for anchor in soup('a'):
	if anchor.string == "Discuss this topic":
		hrefs.append(anchor['href'])

for href in hrefs:
	webbrowser.open(href,new=2)

remove(argv[1])
