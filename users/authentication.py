import jwt, datetime
from rest_framework import exceptions

def create_access_token(id):
  return jwt.encode(
    {
      'user_id':id,
      'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=30),
      'iat':datetime.datetime.utcnow()
    },
    'richardboyz_access',
    algorithm='HS256'
  )

def create_refresh_token(id):
  return jwt.encode(
    {
      'user_id':id,
      'exp':datetime.datetime.utcnow()+datetime.timedelta(days=7),
      'iat':datetime.datetime.utcnow()
    },
    'richardboyz_refresh',
    algorithm='HS256'
  )

def decode_access_token(token):
  try:
    payload = jwt.decode(token,'richardboyz_access',algorithms='HS256')

    return payload['user_id']
  except:
    raise exceptions.AuthenticationFailed('unauthenticated')
  
def decode_refresh_token(token):
  try:
    payload = jwt.decode(token,'richardboyz_refresh',algorithms='HS256')

    return payload['user_id']
  except:
    raise exceptions.AuthenticationFailed('unauthenticated')