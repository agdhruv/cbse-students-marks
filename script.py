import requests
from bs4 import BeautifulSoup
import sys
import linecache

# Whenever a the combination of roll number, school code and centre code do not match, an exception will be raised.
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


no_of_students = 120 # Enter the approximate number of students of class 12 in your school here
any_rno = '9188280' # Enter any roll number of your school here
any_rno = int(any_rno)

highest_perc = 0
lowest_perc = float('inf')
marks_in_x = [] # to get the highest score in a subject
marks_in_x_by = [] # to get the highest scorer(s) in a subject
highest_in_x = 0
highest_in_x_by = []
i = 0 # counter to keep check on how many students' results did we get


# We need to do the same thing for all students of the school. Hence, start loop.
for rno in range(any_rno-no_of_students,any_rno+no_of_students):
	rollno = str(rno)
	url = 'http://cbseresults.nic.in/class12npy/class12th17.asp'

	# Copied headers to from Chrome on Mac to replicate a POST request from a browser.
	headers = {
		"Host": "cbseresults.nic.in",
		"Connection": "keep-alive",
		"Content-Length": "42",
		"Cache-Control": "max-age=0",
		"Origin": "http://cbseresults.nic.in",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Referer": "http://cbseresults.nic.in/class12npy/class12th17.htm",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6",
		"Cookie": "sssssss=0123e2aasssssss_0123e2aa"
	}
	data = {
		'regno': rollno,
		'sch': '65629', # enter school code
		'cno': '8157', # enter centre code (examination centre)
		'B2': 'Submit'
	}

	# send POST request to get HTML page
	response = requests.post(url, data, headers=headers)
	html = response.content

	# make Soup :D
	soup = BeautifulSoup(html, 'lxml')

	# Get name and roll number of current student in a list.
	studentDetails = []

	# Here is when the first exception may be raised, since something we are looking for might not
	# be present in th HTML page if the credentials entered are wrong.
	try:
		tableStudent = soup.find("table", attrs={'width': '75%'})
		for row in tableStudent.find_all("tr")[:2]:
			detail = row.find_all("td")[1].get_text().strip()
			studentDetails.append(str(detail))

		# Start making string to finally print to text file
		string = "{}: {}\n".format(studentDetails[0], studentDetails[1])

		# Try to get marks data now - this is where we play the game!
		total_of_all = 0
		subs = 0
		tableMarks = soup.find("table", attrs={'cellpadding': '2'})
		for row in tableMarks.find_all("tr")[1:-1]:
			if row.find("td", attrs={"colspan": '6'}):
				continue

			subject = row.find_all("td")[1].get_text().strip().encode('utf-8')
			theory = row.find_all("td")[2].get_text().strip().encode('utf-8')
			theory = "N/A" if theory == "" else theory
			practical = row.find_all("td")[3].get_text().strip().encode('utf-8')
			practical = "N/A" if practical == "" else practical
			total = row.find_all("td")[4].get_text().strip().encode('utf-8')
			grade = row.find_all("td")[5].get_text().strip().encode('utf-8')
			if total == "---":
				total = "N/A"
				string += "{}:\n 	{}, {}, {}, {}\n".format(subject, theory, practical, total, grade)
				total = "0"
				subs -= 1
			elif total[-1:] == "A":
				total = "Absent"
				string += "{}:\n 	{}, {}, {}, {}\n".format(subject, theory, practical, total, grade)
				total = "0"
				subs -= 1
			else:
				total = total[0:3]
				string += "{}:\n 	{}, {}, {}, {}\n".format(subject, theory, practical, total, grade)
			total = float(total)
			total_of_all += total
			subs += 1

			# To get the name and marks of the topper in a subject
			if subject == 'MATHEMATICS':
				marks_in_x.append(total)
				marks_in_x_by.append(studentDetails[1])

		result = tableMarks.find("td", attrs={'colspan': '5'}).get_text()

		# Calculate Percentage and result
		percentage = (total_of_all/subs)
		result = tableMarks.find("td", attrs={'colspan': '5'}).get_text().strip().encode('utf-8')

		# Calculate highest and lowest percentages
		if percentage > highest_perc:
			highest_perc = percentage
		if percentage < lowest_perc:
			lowest_perc = percentage

		# Complete forming the final string to be written into the text file
		string += "\nPercentage: {}%\n{}\n\n\n\n".format(percentage, result)

		# print the number of the results that we are getting
		i += 1
		print i

		# write in text file
		with open("results.txt", "a") as file:
		    file.write(string)

	except Exception as e:
		# PrintException() # this function can be called for debugging
		print "Invalid credentials."
		continue

print "\n\nHighest Percentage: " + str(highest_perc)
print "Lowest Percentage: " + str(lowest_perc)

highest_in_x = max(marks_in_x)
for i in range(len(marks_in_x)):
	if marks_in_x[i] == highest_in_x:
		highest_in_x_by.append(marks_in_x_by[i])
print highest_in_x, highest_in_x_by