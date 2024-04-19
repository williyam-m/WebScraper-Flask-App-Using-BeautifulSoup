from flask import Flask, jsonify, render_template, request, Response
import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_website(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all text content
        text_content = [element.text.strip() for element in soup.find_all(text=True)]

        # Find all links
        links = [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]

        # Find all image URLs
        images = [urljoin(url, img.get('src')) for img in soup.find_all('img', src=True)]

        # Find all video URLs
        videos = [urljoin(url, video.get('src')) for video in soup.find_all('video', src=True)]

        # Get HTML content
        html_content = str(soup)

        return {
            'html_content': html_content,
            'text_content': text_content,
            'links': links,
            'images': images,
            'videos': videos
        }
    except :
        return {
            'sorry': "try other url",
        }

@app.route('/api/scrape/<path:url>')
def scrape_api(url):
    scraped_content = scrape_website(url)
    return jsonify(scraped_content)

@app.route('/scrape', methods = ['POST'])
def scrape():
    if request.method == 'POST':
        url = request.form['url']
        scraped_content = scrape_website(url)
        return render_template('home.html', value = scraped_content)
    return render_template('home.html', value ='')

@app.route('/')
def home():
    return render_template('home.html', value = '')

if __name__ == '__main__':
    app.run(debug=True)
