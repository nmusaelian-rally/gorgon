import os
from flask import render_template
from app.models import Installation
from helpers.rally import validRallyIdent
import datetime


def setupApp(db, request):
    # https://ef151b60.ngrok.io/setup?installation_id=575440&setup_action=update
    if request.method == 'GET':
        install_id = request.args.get('installation_id')
        app_installation = Installation.query.filter_by(install_id=int(install_id)).all()
        if not app_installation:
            installation = Installation(install_id=install_id)
            db.session.add(installation)
            db.session.commit()
            sub_id = ''
            api_key = ''
        else:
            app_installation = app_installation[0]
            sub_id  = app_installation.sub_id
            api_key = app_installation.api_key

        #print("in setupApp the current dir is %s" % os.getcwd())

        return render_template('setup.html', install_id=install_id, sub_id=sub_id, api_key=api_key)

    elif request.method == 'POST':
        action = 'install'

        install_id, sub_id, api_key = request.form['install_id'], request.form['sub_id'], request.form['api_key']
        #print("IN SETUP.PY: %s, %s, %s" %(install_id, sub_id, api_key))

        installation = Installation.query.filter_by(install_id=int(install_id))
        if not installation:
            return render_template('setup_result.html', install_id=install_id,
                                   message="No installation record found for %s" % install_id)

        installation = installation.first()
        if installation.sub_id and installation.api_key:
            action = 'update'
        installation.sub_id  = sub_id
        installation.api_key = api_key

        if action == 'install':
            installation.enabled_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        if action == 'update':
            installation.last_update = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # call validation for the install_id, sub_id, api_key; install_id must exist, api_key must be valid and be associated with the sub_id
        proceed, problem = validRallyIdent(api_key, sub_id)
        if proceed:
            db.session.commit()
            db.session.flush()
            message = "Successfully recorded your Rally Subscription ID and Api Key."
        else:
            message = problem
        return render_template('setup_result.html', install_id=install_id, message=message)

