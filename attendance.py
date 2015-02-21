#!/usr/bin/python

# get weekly attendance

from getpass import getpass
from datetime import datetime,timedelta
from learningsphere import *

username = raw_input('Enter your LearningSphere username: ')
password = getpass('Enter your LearningSphere password: ')
url      = 'http://hesseronline.mrooms3.net/'

today    = datetime.today()
lastweek = today - timedelta(days=7)

br           = createBrowser()
br,page      = loginLS(br,url,username,password)
myclass,soup = selectClass(page)

print 'Searching ' + myclass + '.'

ids    = []
br,ids = getStudentList(br,myclass,soup)

displayAttendance(br,ids,lastweek)

