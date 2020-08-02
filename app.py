from flask import Flask, render_template, request, redirect
import re
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/', methods=['POST','GET']) #method allows this route to accept POST and GET (by default only GET) requests.
# can now send requests using POST
def index():
    if request.method == 'POST':
        # validate website regex, else return error message under the input field
        website = request.form['content']
        validated_name = validate(website)
        if validated_name:
            # get the meta tags by scraping website for relevant data
            seo_tag = getMeta(website)
            if seo_tag:
            	return render_template('index.html', seo_tag=seo_tag)
            else:
            	error="Sorry, Its look like your Website doesn't have proper structure. Kindly try any other"
            	return render_template('index.html', error=error)  
        else:
            error = "Please check the domain name you provide [or] Check entered website domain is valid, including web protocol (http/https)"
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')


def validate(website):
	#validate the website is up or down
    try:
        page = requests.get(website)
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
		source = requests.get(website).text
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

		return seo_string
	except Exception as e:
		pass

# to run the flask application
if __name__ == '__main__':
    app.run(debug=True)