
import os
from app.app import app,db
from flask import Flask, request, render_template

from handlers.gh_handler  import handleGithubAppPost
from helpers.signature    import validateGithubSignature
from handlers.setup       import setupApp

# @handlers.before_first_request()
# def beVeryAfraid():
#     pass

HOOK_SECRET_KEY = os.environb[b'HOOK_SECRET_KEY']

@app.route('/home', methods=['GET'])
def home():
    return "home"

@app.route('/setup', methods=['GET','POST'])
def setup():
    return setupApp(db, request)

@app.route('/', methods=['POST'])
def githubAppPost():
    if not validateGithubSignature(HOOK_SECRET_KEY, request):
        return "403 Request not authorized"
    return handleGithubAppPost(db, request)

#
# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)
