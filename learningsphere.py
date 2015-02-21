#!/usr/bin/python

# functions for LearningSphere scripts

import mechanize
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

# create a class for colorized output
class c:
	RED   = '\033[91m'
	GREEN = '\033[92m'
	END   = '\033[0m'

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
	Logs in to LearningSphere. With some minimal credential checking.
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
		classes.append(a.string)
	
	print '\nYour Classes\n'
	for index,cl in enumerate(classes):
		print ' [%d] %s' % (index + 1,cl)
	
	print c.RED 
	print 'WARNING: Choosing an expired class causes this program to fail.'
	print c.END
	
	raw = raw_input('Select an active class: ')
	
	try:
		number = int(raw)
		if number < 1:
			raise SystemExit("Invalid selection!")
		elif number > len(classes):
			raise SystemExit("Invalid selection!")
		else:
			myclass = classes[number - 1]
	except:
		raise SystemExit("Invalid selection!")

	return myclass,soup

def getStudentList(br,myclass,soup):
	"""
	Navigates to Logs page and builds a list of students
	"""
	course_link = soup('a',{'title':myclass})[0]['href']
	logs_link = course_link.replace('course/view.php','report/log/index.php')
	br.open(logs_link)

	# exclude the Guest User (1) and myself (3748).
	print 'Getting a list of students.'
	ids = []
	br.select_form(nr=0)
	students = br.form.find_control('user')
	for i in students.items:
		if i.name == '' or i.name == '1' or i.name == '3748':
			continue
		else:
			ids.append([i.name, [label.text for label in i.get_labels()][0],''])
	
	return br,ids

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
			PA = c.GREEN + 'PRESENT' + c.END
			print '%-20s | %s | %s' % (name,PA,date)
			record[2] = 'P'
		elif lastweek > log:
			PA = c.RED + 'ABSENT' + c.END
			print '%-20s | %s  | %s' % (name,PA,date)
			record[2] = 'A'
		else:
			print 'Error: %s' % record

# select a Pod to view
def selectPod(soup,myclass):
	base_url = 'http://hesseronline.mrooms3.net/course/view.php?id='
	href     = soup('a', {'title':myclass})[0]['href']
	class_id = href.replace(base_url,'')

	print ''
	for i in range(1,9):
		print ' [%d] Pod %d' % (i,i)
	
	pod_raw = raw_input('\nSelect a Pod: ')
	pod = int(pod_raw)

	if pod < 1:
		raise SystemExit('Dude! Stop fuzzing me!')
	elif pod > 8:
		raise SystemExit('Dude! Stop fuzzing me!')
	else:
		url = base_url + class_id + '&section=' + pod_raw
	
	return url,pod_raw

# Navigate to Pod X Reflection and get href and the number of students
def podXreflection(br,url,pod):
	print 'Navigating to Pod ' + pod + '.'

	page = br.open(url).read()
	soup = BeautifulSoup(page)

	for span in soup('span'):
		try:
			if span.contents[0] == 'Pod ' + pod + ' Reflections':
				break
		except:
			pass

	href = span.parent['href'] + '&action=grading'
	
	# on this page we need to find how many students are in this class
	print 'Navigating to Pod ' + pod + ' Reflection Grading page.'
	page = br.open(href).read()
	soup = BeautifulSoup(page)
	student_number = len(soup.table.tbody('tr'))

	return student_number,href

# test whether page has submitted content
def didSubmit(soup):

	if soup.table.tbody.tr.td.next_sibling.string == 'No attempt':
		return False
	elif soup.table.tbody.tr.td.next_sibling.string == 'Submitted for grading':
		return True
	else:
		raise SystemExit('Cannot determine Pod reflection status.')

def markSubmitted(br,soup):
	br.select_form(nr=0)
	br.form['grade'] = 'Submitted'



def markNotSubmitted(br,soup):
	br.select_form(nr=0)
	br.form['grade'] = 'Not Submitted'





