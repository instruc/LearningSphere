#!/usr/bin/python

# get weekly attendance

from getpass import getpass
from datetime import datetime,timedelta
from learningsphere import *

url      = 'http://hesseronline.mrooms3.net/'
today    = datetime.today()
lastweek = today - timedelta(days=7)
ids      = []

username    = raw_input('Enter your LearningSphere username: ')
password    = getpass('Enter your LearningSphere password: ')
br          = createBrowser()
br,page     = loginLS(br,url,username,password)
cid,myclass = selectClass(page) # cid not used in attendance.py
teachid     = getTeacherID(page)
br,ids      = getStudentList(br,myclass,teachid,page)
ids         = getAttendanceDates(br,ids)

displayAttendance(ids,lastweek)
