import base64
import time
codeTTL = 10 # Value is always in minutes
baseURL = "http://127.0.0.1:8000/pwdless/verify/" #for ease of use, i have hardcoded url
tokenMetaData = {}
tokenMetaData['iat'] = int(time.time())
tokenMetaData['nbf'] = int(time.time())
tokenMetaData['exp'] = int(time.time()) + codeTTL * 60
tokenMetaData['iss'] = baseURL
