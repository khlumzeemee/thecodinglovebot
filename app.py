'''
Created on Mar 18, 2016

@author: oreo
'''

import os
import urllib
from flask import Flask, Response, jsonify, request
from bs4 import BeautifulSoup
from slackclient import SlackClient

app = Flask(__name__)

TOKEN = 'QvdxLn8OjvvkrA0DgRRzCh8X'
THECODINGLOVE_BOT_DEBUG = True
THECODEINGLOVE_URI = "http://www.thecodinglove.com/random"

@app.route('/thecodinglove', methods=['POST', 'GET'])
def thecodinglove():
    #For get method tests only
    if request.method == 'GET':
        resp = get_post()
        return Response(str(resp))
    elif request.form['token'] != TOKEN:
        return Response("Invalid token")
    
    post = get_post()
    
    if post:    
        caption = post.div.h3.string
        gif_url = post.img["src"]
        
        #sc = SlackClient(TOKEN)
        return jsonify(text="The Coding Love",
                       attachment_text=caption, 
                       image_url=gif_url)
        
    #Default
    return Response()

def get_post():
    with urllib.request.urlopen(THECODEINGLOVE_URI) as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        
        #This is where the post is
        return soup.find(id="post1")
    return None


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=THECODINGLOVE_BOT_DEBUG)