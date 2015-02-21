# LearningSphere Scripts

## Before You Begin

1. Install [Python 2.7](https://www.python.org/downloads/).

	* Make sure you added `C:\Python27;C:\Python27\Scripts` to your PATH
	  variable.
	
2. Install [mechanize](https://pypi.python.org/pypi/mechanize/).

	* Run `pip install mechanize` at the command prompt.

3. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/).

	* Run `pip install beautifulsoup4` at the command prompt.

## Taking Attendance

The `attendance.py` script:

+ Logs in to the LearningSphere with the credentials you supply.
+ Presents a list of your classes for you to choose. (This is the same 
  list found under My Courses.)
+ Checks whether the last login date for each student was within the past 
  7 days.
+ Displays a list of students, their attendance status, and their last 
  login.

```
Student              | Status  | Last Login
---------------------+---------+-----------
Student A            | PRESENT | 20 Feb, 18:35
Student B            | PRESENT | 19 Feb, 00:03
Student C            | PRESENT | 19 Feb, 19:36
```

### Running The Script

To run, open the command prompt and run `python attendance.py`.
