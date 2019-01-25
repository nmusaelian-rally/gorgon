
import os
from app.app import app,db
from flask import Flask, request, render_template

from handlers.gh_handler  import handleGithubAppPost
from helpers.signature    import validateGithubSignature, validateReferer
from  handlers.setup      import setupApp

# @handlers.before_first_request()
# def beVeryAfraid():
#     pass

HOOK_SECRET_KEY = os.environb[b'HOOK_SECRET_KEY']

@app.route('/home', methods=['GET'])
def home():
    return "home"

@app.route('/setup', methods=['GET','POST'])
def setup():
    # if request.method == 'GET':
    #     if not validateReferer(request):
    #         return "403"
    # elif request.method == 'POST':
    #     if not validateGithubSignature(HOOK_SECRET_KEY, request, mode='prod'):
    #         return "403"
    return setupApp(db, request)
    #return handleGeneralCrappiness(db, request)


@app.route('/', methods=['POST'])
def githubAppPost(): return handleGithubAppPost(db, request)



@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
