
import os
from app.app import app,db
from flask import request

from handlers.gh_handler  import handleGithubAppPost
from helpers.signature    import validateGithubSignature
from handlers.setup       import setupApp

HOOK_SECRET_KEY = os.environb[b'HOOK_SECRET_KEY']

@app.route('/home', methods=['GET'])
def home():
    return "home"

@app.route('/setup', methods=['GET','POST'])
def setup():
    print("I am about to call the  setupApp method ...")
    return setupApp(db, request)

@app.route('/', methods=['POST'])
def githubAppPost():
    print("I am in the githubAppPost method ...")
    if not validateGithubSignature(HOOK_SECRET_KEY, request):
        print("Unable to validate the request using the HOOK_SECRET_KEY of [%s]" % HOOK_SECRET_KEY)
        return "403 Request not authorized"
    print("the Github post message was validated ...")
    return handleGithubAppPost(db, request)

#
# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)
