import requests
from bs4 import BeautifulSoup

def percentage(totals):
	total = 0.0

	for i in totals:
		total += i

	return total/len(totals)

cookies = {
	'lllllll': 'c406fd81lllllll_c406fd81',
}

headers = {
	'Connection': 'keep-alive',
	'Pragma': 'no-cache',
	'Cache-Control': 'no-cache',
	'Origin': 'http://cbseresults.nic.in',
	'Upgrade-Insecure-Requests': '1',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Referer': 'http://cbseresults.nic.in/class12zpq/Class12th18.htm',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

highest_bo4 = 0
highest_bo5 = 0
highest_perc = 0

for j in range(2626001, 2626450):

	data = [
		('regno', str(j)),
		('sch', '20020'),
		('cno', '2068'),
		('B2', 'Submit'),
	]

	response = requests.post('http://cbseresults.nic.in/class12zpq/class12th18.asp', headers=headers, cookies=cookies, data=data)

	soup = BeautifulSoup(response.text, "lxml")

	try:
		roll_number = soup.select('table[width=75%] tr')[0].text.split(':')[1].strip().encode('utf-8')
	except Exception as e:
		print "Roll number not valid:", j
		continue

	name = soup.select('table[width=75%] tr')[1].text.split(':')[1].strip().encode('utf-8')

	print roll_number, name, "\n"

	marks = soup.select('body div[align=center]')[1].select('table')[0].select('tr')

	totals = []

	for tr in marks[1:-1]:
		columns = tr.select('td')

		code = columns[0].text.strip()

		if code[0] == '5' or code[0] == 'A':
			continue

		try:
			sub_name = columns[1].text.strip()
		except Exception as e:
			pass

		try:
			theory = columns[2].text.strip()
		except Exception as e:
			pass

		try:
			practical = columns[3].text.strip()
			if not practical:
				practical = 'N/A'
		except Exception as e:
			pass

		try:
			sub_name = columns[1].text.strip()
		except Exception as e:
			pass

		try:
			sub_name = columns[1].text.strip()
		except Exception as e:
			pass

		try:
			total = int(columns[4].text.strip())
			totals.append(total)
		except ValueError as e:
			total = 0
			totals.append(total)
			print "Something weird going on here"
			continue

		print code, sub_name, theory, practical, total

	totals.sort(reverse = True)
	bo4 = percentage(totals[:4])
	bo5 = percentage(totals[:5])
	perc = percentage(totals)

	print "\nBest of 4:", bo4
	print "Best of 5:", bo5
	print "Percentage of all:", perc
	print "\n\n"

	# highest_bo4 = max(bo4, highest_bo4)
	# highest_bo5 = max(bo5, highest_bo5)
	# highest_perc = max(perc, highest_perc)

# print highest_bo4
# print highest_bo5
# print highest_perc
