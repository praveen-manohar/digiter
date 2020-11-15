from bs4 import BeautifulSoup
import requests
import re

from grank import ranking
from keyword_density import kwmain
import crawler
import tldextract

import datetime

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


def validate(website):
	#validate the website is up or down
	try:
		page = requests.get(website, verify=False)
		if page.status_code != 404:
			#validate website is complete
			regex = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
			if re.search(regex, website):
				return True
			else:
				return False
		else:
			return False
	except Exception as e:
		return False

def getMeta(website):
	
	try:
		# set up beautiful soup
		# 1. create website request
		source = requests.get(website, verify=False).text
		# 2. parse website content
		soup = BeautifulSoup(source, 'lxml')
		# 3. grab all nessesary information from the page
		name = soup.find('h1').text.strip()
		title = soup.find('title').text.strip()
		image = soup.find('body').img['src']
		description = soup.find('p').text

		# string used to store meta tag
		seo_string = '<meta charset="utf-8">\n' \
				 '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n' \
				 '<meta name="viewport" content="width=device-width, initial-scale=1">\n' \
				 '<meta name="description" content="' + description + '">\n' \
				 '<link rel="canonical" href="' + website + '">\n' \
				 '<meta property="og:locale" content="en_US">\n' \
				 '<meta property="og:type" content="website">\n' \
				 '<meta property="og:site_name" content="' + name + '">\n' \
				 '<meta property="og:url" content="' + website + '">\n' \
				 '<meta property="og:title" content="' + title + '">\n' \
				 '<meta property="og:description" content="' + description + '">\n' \
				 '<meta property="og:image" content="' + image + '">'
		
		txt(seo_string)
		print("allokay")

		return seo_string
	except Exception as e:
		pass

def txt(seo_string):
	print("inside txt")
	file ='files/meta/'+ datetime.date.today().strftime("%d-%m-%Y_%H-%M-%S") +'_meta_digiter.txt'
	print("going")
	with open(file, 'w') as f:
		print("gents in")
		f.writelines(seo_string)
		f.close()
		print("done")
	files = file
	return

def sitemap_genarator(website):
	try:
		web = website
		ext = tldextract.extract(web)
		domain_name = ext.domain

		# validate website regex, else return error message under the input field
		validated_name = validate(web)
		if validated_name:
			crawl = crawler.Crawler(num_workers=1, parserobots=None, output="files/sitemap/"+domain_name+"__sitemap_.xml", report=True, domain=website, exclude=[], skipext=[], drop=[], debug=False, verbose=False, images=False, auth=False)
			seo_tag = crawl.run()
			if seo_tag:
				return seo_tag
			else:
				error="Sorry, Its look like your Website doesn't have proper structure. Kindly try any other"
				return error  
		else:
			error = "Please check the domain name you provide [or] Check entered website domain is valid, including web protocol (http/https)"
			return error
	except Exception as e:
		error = "eroor : "+str(e)
		return error

def keyword_density(web):
	website = web 
	validated_name = validate(website)
	if validated_name:
		kwd_ = kwmain(website)
		if kwd_:
			kwd_score = "Your " + str(website) + " Keyword Desity rank is " + str(kwd_)
			return kwd_score
		else:
			error="Sorry, Its look like your Website doesn't have proper structure. Kindly try any other"
			return error  
	else:
		error = "Please check the domain name you provide [or] Check entered website domain is valid, including web protocol (http/https)"
		return error

def rank(url,keyw,device):
	# validate website regex, else return error message under the input field
	website = url
	key = keyw
	mode = device

	validated_name = validate(website)
	if validated_name:
		# get the meta tags by scraping website for relevant data
		seo_tag = ranking(mode,website,key)
		if seo_tag:
			return seo_tag
		else:
			error="Sorry, Its look like your Website doesn't have proper structure. Kindly try any other"
			return error   
	else:
		error = "Please check the domain name you provide [or] Check entered website domain is valid, including web protocol (http/https)"
		return error

def main():
	inp = input("\n<< Digiter - Webversion (https://digiterbee.herokuapp.com) >> \n 1 > To Generate Meta tag for website headers \n 2 > To Generate Sitemap.xml \n 3 > To Check Keyword Density \n 4 > To Check Google Rank\n 5 > To Exit ->")
	if (inp=="1"):
		website=input("-> Enter your website : ")
		getMeta(website)
		main()
	elif(inp=="2"):
		website=input("-> Enter your website : ")
		sitemap_genarator(website)
		main()
	elif(inp=="3"):
		website=input("-> Enter your website : ")
		keyword_density(website)
		main()
	elif(inp=="4"):
		url=input("-> Enter your Website : ")
		keyw=input("-> Enter your Keyword : ")
		device=input("-> Enter 'desktop' or 'mobile' : ")
		rank(url,keyw,device)
		main()
	elif(inp=="5"):
		exit()
	else:
		print("enter valid")
		main()

if __name__ == "__main__": 
    main()