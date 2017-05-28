import requests
from bs4 import BeautifulSoup

rollno = '' # insert a valid roll number of any student of a school
url = 'http://cbseresults.nic.in/class12npy/class12th17.asp'

# Copied POST request headers from the request that Chrome on Mac sent to the above specified url.
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
	'sch': '65629',
	'cno': '8157',
	'B2': 'Submit'
}

# send POST request to get HTML page
response = requests.post(url, data, headers=headers)
html = response.content

# make Soup :D
soup = BeautifulSoup(html, 'lxml')

# Get name and roll number of student
studentDetails = []
tableStudent = soup.find("table", attrs={'width': '75%'})
for row in tableStudent.find_all("tr")[:2]:
	detail = row.find_all("td")[1].get_text().strip()
	studentDetails.append(str(detail))

# Start making string to finally print to text file
string = "{}: {}\n".format(studentDetails[0], studentDetails[1])

# Try to get marks data now
total_of_all = 0
subs = 0
tableMarks = soup.find("table", attrs={'cellpadding': '2'})
for row in tableMarks.find_all("tr")[1:-1]:
	subject = row.find_all("td")[1].get_text().strip().encode('utf-8')
	theory = row.find_all("td")[2].get_text().strip().encode('utf-8')
	theory = "N/A" if theory == "" else theory
	practical = row.find_all("td")[3].get_text().strip().encode('utf-8')
	practical = "N/A" if practical == "" else practical
	total = row.find_all("td")[4].get_text().strip().encode('utf-8')
	grade = row.find_all("td")[5].get_text().strip().encode('utf-8')
	subject_pass_fail = total[-1:].strip()
	total = total[0:3]
	string += "{}: {}\n 	{}, {}, {}, {}\n".format(subject, subject_pass_fail, theory, practical, total, grade)
	total = float(total)
	total_of_all += total
	subs += 1

result = tableMarks.find("td", attrs={'colspan': '5'}).get_text()

# Calculate Percentage and result
percentage = (total_of_all/subs)

result = tableMarks.find("td", attrs={'colspan': '5'}).get_text().strip().encode('utf-8')

string += "\nPercentage: {}%\n{}\n\n\n\n".format(percentage, result)

# write in text file
with open("results.txt", "a") as file:
	file.write(string)