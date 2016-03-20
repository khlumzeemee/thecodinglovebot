'''
Created on Mar 18, 2016

@author: oreo
'''

import os
import urllib
from flask import Flask, Response, jsonify, request
from bs4 import BeautifulSoup

app = Flask(__name__)

TOKEN = 'QvdxLn8OjvvkrA0DgRRzCh8X'
THECODINGLOVE_BOT_DEBUG = True
THECODEINGLOVE_URI = "http://www.thecodinglove.com/random"

@app.route('/thecodinglove', methods=['POST'])
def thecodinglove():

    if request.form['token'] != TOKEN:
        return Response("Invalid token")
    
    post = get_post()
    
    if post:
        json_response = {}
        caption = post.div.h3.string
        gif_url = post.img["src"]
        
        json_response["text"] = "The Coding Love"
        attachment = []
        attachment.append({"title":caption, "image_url":gif_url})
        json_response["attachments"] = attachment
                
        #sc = SlackClient(TOKEN)
        return jsonify(**json_response)
        
    #Default
    return Response()

def get_post():
    with urllib.request.urlopen(THECODEINGLOVE_URI) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        #This is where the post is
        return soup.find(id="post1")
    return None

@app.route('/', methods=['GET'])
def index():
    return str(get_post())
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=THECODINGLOVE_BOT_DEBUG)