
from app.models import Installation
from pyral  import Rally


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
