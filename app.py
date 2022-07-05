import re
from flask import Flask,jsonify,make_response
from bs4 import BeautifulSoup as bs
import requests

app = Flask(__name__)

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

url = "https://jobs.scotiabank.com/go/IT-&-Digital-Banking-Jobs/2298017/"

list = []

@app.route('/fetchData',methods=['GET'])
def return_scraped_data():
    req = requests.get(url, headers)
    soup = bs(req.content, 'html.parser')
    jobs = soup.find_all(class_="jobTitle-link")
    for j in jobs:
        list.append({"jobName":url+j.string,"jobLink":j["href"]})
    response = make_response(
                jsonify(
                    {"list":list}
                )
            )
    response.headers["Content-Type"] = "application/json"
    return response