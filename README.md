# LearningSphere Scripts

Helpful scripts for online instructors who teach in the LearningSphere.

## Before You Begin

0. Install git.

1. Install [Python 2.7](https://www.python.org/downloads/).

	* Make sure you added `C:\Python27;C:\Python27\Scripts` to your PATH
	  variable.
	
2. Install [mechanize](https://pypi.python.org/pypi/mechanize/).

	* Run `pip install mechanize` at the command prompt.

3. Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/).

	* Run `pip install beautifulsoup4` at the command prompt.

## Running Scripts

To run a script:

1. `git clone https://github.com/instruc/LearningSphere/`
2. `cd LearningSphere`
3. `python attendance.py`

## Taking Attendance

The `attendance.py` script:

+ Logs in to the LearningSphere with the credentials you supply.
+ Presents a list of your classes for you to choose. (This is the same 
  list found under My Courses.)
+ Checks each student's view, update, and create actions
+ Displays a list of students, their last view action, their last update
  action, and their last create action.

```
      Student        |    View       |    Update     |    Create     |
---------------------+---------------+---------------+---------------+
Student A            | 12 May, 11:47 | 7 May, 00:12  | 10 May, 10:31 |
Student B            | 12 May, 20:58 | 12 May, 20:51 | 12 May, 20:51 |
Student C            | 11 May, 23:07 | 10 May, 22:43 | 10 May, 22:43 |

```

## Grading Pod Reflections

The `gradepods.py` script:

+ Logs in to the LearningSphere with the credentials you supply.
+ Presents a list of your classes for you to choose. (This is the same 
  list found under My Courses.)
+ Presents a list of Pods to choose from (1-8).
+ Marks as Not Submitted the Pod Reflections that have no submission.
+ Marks as Submitted the Pod Reflections that have submissions.
+ Writes to a file `pod_X_reflections.txt` the following information:
	* the name of the student
	* the student's full submission
	* the URL where the teacher can directly respond. 
