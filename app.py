
from flask import Flask,jsonify,make_response
from bs4 import BeautifulSoup as bs
import requests
app = Flask(__name__)

url = "https://jobs.scotiabank.com/go/IT-&-Digital-Banking-Jobs/2298017/"
url_params = "/?q=&sortColumn=referencedate&sortDirection=desc"
url_factor = 25
list = []

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

@app.route('/api/scotiabank/ping')
def ping():
    response = make_response({'status': 'OK'})
    return response



@app.route('/api/scotiabank',methods=['GET'],defaults={'page':1})
@app.route('/api/scotiabank/<page>',methods=['GET'])
def scotia_scraped_data(page=1):
    modified_url = url
    if(int(page) > 1):
        modified_url+=str((int(page)*url_factor - url_factor))+url_params 
    req = requests.get(modified_url, headers)
    soup = bs(req.content, 'html.parser')
    jobs = soup.find_all(class_="jobTitle-link")
    for j in jobs:
        list.append({"jobName":url+j.string,"jobLink":j["href"]})
    response = make_response(jsonify({"list":list}))
    response.headers["Content-Type"] = "application/json"
    return response
