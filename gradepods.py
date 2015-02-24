#!/usr/bin/python

# mark Pods as read and concatenate comments

from getpass import getpass
from mountwashington import *

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
s_number    = getStudentNumber(br,podID)

for index in range(0,s_number):
	url = base_url + str(index)
	gradePod(br,url)
