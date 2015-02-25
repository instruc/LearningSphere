#!/usr/bin/python

# functions for LearningSphere scripts

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import urlparse

def createBrowser():
	"""
	Create a browser object using mechanize.
	"""
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	return br

def loginLS(br,url,username,password):
	"""
	Logs in to LearningSphere. With some minimal checking.
	"""
	br.open(url)
	br.select_form(nr=0)
	br.form['username'] = username
	br.form['password'] = password

	try:
		page = br.submit().read()
	except Exception:
		raise SystemExit('Failed to login.')

	if 'Log in to the site' in br.title():
		raise SystemExit('Failed to login. Bad credentials?')

	return br,page

def selectClass(page):
	"""
	Allows user to select a class from those listed under My Courses tab.
	"""
	soup = BeautifulSoup(page)
	
	# get the <a> element under which our classes are listed
	for anchor in soup('a',{'class':'yui3-menu-label'}):
		if anchor.string == 'My courses':
			break
	
	classes = []
	for a in anchor.next_sibling('a'):
		name = a.string
		query = urlparse.urlparse(a['href']).query
		classid = urlparse.parse_qs(query)['id'][0]
		classes.append([classid,name])
	
	print '\nYour Classes\n'
	for index,cl in enumerate(classes):
		print ' [%d] %s' % (index + 1,cl[1])
	
	print '\nWARNING: Choosing an expired class causes this program to fail.\n'
	
	raw = raw_input('Select an active class: ')
	
	try:
		number = int(raw)
		if number < 1:
			raise SystemExit("Invalid selection!")
		elif number > len(classes):
			raise SystemExit("Invalid selection!")
		else:
			classid,myclass = classes[number - 1]
	except:
		raise SystemExit("Invalid selection!")

	print 'You selected ' + myclass + '.'
	return classid,myclass

def getStudentList(br,myclass,teachid,page):
	"""
	Navigates to Logs page and builds a list of students
	"""
	soup = BeautifulSoup(page)
	course_link = soup('a',{'title':myclass})[0]['href']
	logs_link = course_link.replace('course/view.php','report/log/index.php')
	br.open(logs_link)

	# exclude the Guest User (1) and teacher
	print 'Getting a list of students.'
	ids = []
	br.select_form(nr=0)
	students = br.form.find_control('user')
	for i in students.items:
		if i.name == '' or i.name == '1' or i.name == teachid:
			continue
		else:
			ids.append([i.name, [label.text for label in i.get_labels()][0]])
	
	return br,ids

def getTeacherID(page):
	soup    = BeautifulSoup(page)
	href    = soup('span',{'class':'usersname'})[0].a['href']
	query   = urlparse.urlparse(href).query
	params  = urlparse.parse_qs(query)
	teachid = params['id'][0]
	return teachid

def displayAttendance(br,ids,lastweek):
	"""
	Displays attendance
	"""
	print '\nStudent              | Status  | Last Login'
	print   '---------------------+---------+-----------'

	# get the activity of each student
	for record in ids:
		number = record[0]
		name   = record[1]
	
		br.select_form(nr=0)
		students = br.form.find_control('user')
		students.value = [ number ]
		page = br.submit().read()
		soup = BeautifulSoup(page)

		try:
			date = soup.table.tbody.tr.td.string
		except AttributeError:
			raise SystemExit("Cannot find date. Were these logs deleted?")

		log =  datetime.strptime(date,'%d %b, %H:%M').replace(year=2015)

		if lastweek < log:
			print '%-20s | PRESENT | %s' % (name,date)
		elif lastweek > log:
			print '%-20s | ABSENT  | %s' % (name,date)
		else:
			print 'Error: %s' % record

def selectPod():
	"""
	Select a Pod number 1 - 8.
	"""
	print '\nAvailable Pods\n'
	for i in range(1,9):
		print ' [%d] Pod %d' % (i,i)
	
	pod_raw = raw_input('\nSelect a Pod: ')
	
	try:
		pod = int(pod_raw)
	except:
		raise SystemExit('Invalid selection!')

	if pod < 1:
		raise SystemExit('Invalid selection!')
	elif pod > 8:
		raise SystemExit('Invalid selection!')

	# return the string because we'll concat it later	
	return pod_raw

def createPodURL(classid,pod):
	"""
	Creates the URL for the previously selected Pod.
	"""
	base = 'http://hesseronline.mrooms3.net/course/view.php?id='
	url = base + classid + '&section=' + pod
	return url

def getPodXReflectionID(br,class_url,pod):
	"""
	Get the Pod ID for the previously selected Pod.
	"""
	# first navigate to class_url and extract Pod X id
	page = br.open(class_url).read()
	soup = BeautifulSoup(page)

	for span in soup('span',{'class','instancename'}):
		if span.contents[0] == 'Pod ' + pod + ' Reflection':
			break
	
	# confirm we got the string
	if span.contents[0] == 'Pod ' + pod + ' Reflection':
		pass
	else:
		raise SystemExit('Cannot find Pod X Reflections.')

	href  = span.parent['href']	
	query = urlparse.urlparse(href).query
	podID = urlparse.parse_qs(query)['id'][0]

	return podID

def getPodBaseURL(podID):
	base = 'http://hesseronline.mrooms3.net/mod/assign/view.php?id='
	url  = base + podID + '&action=grade&rownum=' 
	return url

def getNumberOfStudents(br,podID):
	base = 'http://hesseronline.mrooms3.net/mod/assign/view.php?id='
	url  = base + podID + '&action=grading'
	page = br.open(url).read()
	soup = BeautifulSoup(page)
	num_of_students = len(soup.table.tbody('tr'))
	return num_of_students

def gradePod(br,url):
	"""

	"""
	print "test"
	return True



	page = br.open(url).read()
	soup = BeautifulSoup(page)
	rows = len(soup.table.tbody('tr'))

	if rows == 3:
		br.select_form(nr=0)
		br.form['grade'] = ['1'] # 1 means Not Submitted
	elif rows == 6:
		br.select_form(nr=0)
		br.form['grade'] = ['2'] # 2 means Submitted
		name = soup('div',{'class','usersummarysection'})[0].a.next_sibling.next_sibling.string
		text = soup('div',{'class','no-overflow'})[1].p.string

		with open('pod_reflections.txt','a') as out:
			out.write(name + ':\n' + text + '\n')
	else:
		raise SystemExit('Cannot determine Pod submission status.')
