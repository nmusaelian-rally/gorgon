import hmac
import hashlib


def validateGithubSignature(secret, request, mode='prod'):

    sha_name, signature = request.headers.get('X-Hub-Signature').split('=')
    if sha_name != 'sha1':
        return False

    # HMAC requires its key to be bytes, but data is strings.
    mac = hmac.new(secret, msg=request.data, digestmod=hashlib.sha1)
    return hmac.compare_digest(mac.hexdigest(), signature)

def validateReferer(request, mode='prod'):
    if request.headers.get('Referer', None) != "https://github.com/":
        return False
    return True