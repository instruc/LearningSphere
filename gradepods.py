#!/usr/bin/python

# mark Pods as read and concatenate comments

from getpass import getpass
from learningsphere import *

username   = raw_input('Enter your LearningSphere username: ')
password   = getpass('Enter your LearningSphere password: ')
url        = 'http://hesseronline.mrooms3.net/'

br          = createBrowser()
br,page     = loginLS(br,url,username,password)
cid,myclass = selectClass(page)
pod         = selectPod()
class_url   = createPodURL(cid,pod)
podID       = getPodXReflectionID(br,class_url,pod)
base_url    = getPodBaseURL(podID)
maxnumber   = getNumberOfStudents(br,podID)

print ''
for index in range(0,maxnumber):
	url = base_url + str(index)
	gradePod(br,url,pod)

