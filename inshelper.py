
from app.models import Installation
from pyral  import Rally

def validInstallationParms(install_id, sub_id, api_key):
    #app_installation = Installation.query.get(install_id)
    app_installation = Installation.query.filter_by(install_id=int(install_id)).all()
    if not app_installation:
        return False, "No record of the installed handlers for %s" % install_id
    if not sub_id or not api_key:
        return False, "Both Subscription ID and Api Key values were not specified"
    status, message = validRallyIdent(api_key, sub_id)
    return status, message


def validRallyIdent(api_key, sub_id):
    try:
        rally = Rally("rally1.rallydev.com", apikey=api_key)
        fields = "SubscriptionID"
        user = rally.get('User', fetch=fields, instance=True)
        if not user:
            return False, "The Api Key provided is not valid"
        if user.SubscriptionID != int(sub_id):
            return False, "The Api Key provided does not match "
    except Exception as ex:
        #return False, "Unable to reach Rally to verify your Api Key and Subscription ID"
        return False, str(ex)

    return True, "Everything is copacetic!"
