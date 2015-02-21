## Before You Begin

1. Install [Python 2.7](https://www.python.org/downloads/).

2. Install [mechanize](https://pypi.python.org/pypi/mechanize/).

3. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/).

# Taking Attendance

## What Happens

This script:

+ Logs in to the LearningSphere with the credentials you supply.
+ Presents a list of your classes for you to choose. (This is the same list found under My Courses.)
+ Checks whether the last login date for each student was within the past 7 days.
+ Displays a list of students, their attendance status, and their last login.

```
Student              | Status  | Last Login
---------------------+---------+-----------
Student A            | PRESENT | 20 Feb, 18:35
Student B            | PRESENT | 19 Feb, 00:03
Student C            | PRESENT | 19 Feb, 19:36
```

## Running the Program

From the command prompt, run

```bash
$ python attendance.py
```
