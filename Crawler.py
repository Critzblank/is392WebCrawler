from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import re
import ssl
import os

seedUrls = ['https://en.wikipedia.org/wiki/Computer', 'https://en.wikipedia.org/wiki/Computer_programming']
keys = ['PC', 'Linux', 'Windows', 'operating system', 'programming language', 'interface', 'coding', 'software', 'hardware', 'processor']
queue = []

visitedUrlList = {''}
savedUrlList = []
pageCounter = 0
maxPages = 500

textFolder = "Crawled Pages/"
if not os.path.exists(textFolder):
    os.makedirs(textFolder)

for url in seedUrls:
	queue.append(url)
	visitedUrlList.add(url)

def get_page_content(url):
	try:
		html_response_text = urlopen(url).read()
		page_content = html_response_text.decode('utf-8')
		return page_content
	except Exception as e:
		return None

def save(text, path):
	f = open(path, 'w', encoding = 'utf-8', errors = 'ignore')
	f.write(text)
	f.close()

def get_urls(soup):
	links = soup.find_all('a')
	urls = []
	for link in links:
		urls.append(link.get('href'))
	return urls

def is_url_valid(url):
	if url is None:
		return False
	if re.search('#', url):
		return False
	if re.search('%', url):
		return False
	if re.search('[png, jpeg]', url):
		return False
	if url[0:6] == '/wiki/':
		return "https://en.wikipedia.org"+url
	elif re.search('https://en.wikipedia.org/wiki/', url):
		return url
	else:
		return False
        
while queue:
	url = queue.pop(0)
	pageContent = get_page_content(url)
	if pageContent is None:
		continue
	termCounter = 0
	soup = bs(pageContent, 'html.parser')
	page_text = soup.get_text()
	for term in keys:
		if re.search(term, page_text, re.I):
			termCounter += 1
			if termCounter >= 2:
				title = soup.title.string
				title = title.replace('/','')
				title = title.replace(':','')
				title = title.replace('\\','')
				title = title.replace('|','')
				title = title.replace('"','')
				path = textFolder + title + ".html"
				print("saved a page")
				save (page_text, path)
				savedUrlList.append(url)
				print(len(savedUrlList))
				pageCounter += 1
				print (title, termCounter, url)
				break
	if pageCounter >= maxPages:
		break
	outGoingUrls = get_urls(soup)
	for outGoingUrl in outGoingUrls:
		fixedUrl = is_url_valid(outGoingUrl)
		if fixedUrl and outGoingUrl not in visitedUrlList:
			queue.append(fixedUrl)
			visitedUrlList.add(outGoingUrl)


fileName = textFolder + "URL list.txt"
f = open(fileName, 'w')
i = 1
for url in savedUrlList:
	f.write(str(i) + ': ' + url + '\n')
	i += 1
f.close()

