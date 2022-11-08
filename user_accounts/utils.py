import jwt
from django.contrib.auth.models import User

def giveUserFromToken(token_str):
    try:
        token_obj = jwt.decode(token_str, options={"verify_signature": False})
    except:
        token_obj = None
    if token_obj:
        return User.objects.get(username=token_obj.get('username', None))
    return None