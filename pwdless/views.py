from django.http.response import Http404, HttpResponse
from django.shortcuts import render,redirect
import jwt
import pwdless.confg as cg
import string, random,smtplib, base64,time
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your views here.
def oneTimeNonce(size=16, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generateCode(email):
	metadataDict = {}
	cg.tokenMetaData['jti'] = oneTimeNonce()
	cg.tokenMetaData['issuedFor'] = email
	jwtToken = jwt.encode(cg.tokenMetaData, settings.JWTSECRET , algorithm='HS256')
	message_bytes = jwtToken.encode('ascii')
	base64_bytes = base64.b64encode(message_bytes)
	base64_message = base64_bytes.decode('ascii')
	return(cg.baseURL + base64_message)

def trimToken(code):
	returnTokenWithoutURL = code.replace(cg.baseURL,"")
	base64_bytes = returnTokenWithoutURL.encode('ascii')
	message_bytes = base64.b64decode(base64_bytes)
	message = message_bytes.decode('ascii')
	return(message)

def sendEmail(code):
	try:
		tokenMetaData = jwt.decode(trimToken(code), settings.JWTSECRET , algorithms=['HS256'])
		recipientEmailAddress = tokenMetaData['issuedFor']
		if settings.EMAILMETADATA:
			message = 'Subject: {}\n\n{}'.format(settings.EMAIL_SUBJECT, settings.EMAIL_TEXT + str(code+"/?email="+recipientEmailAddress))
			server = smtplib.SMTP(settings.SMTP_SERVER,settings.SMTP_PORT)
			server.ehlo()
			server.starttls()
			server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
			server.sendmail(settings.EMAIL_USER, recipientEmailAddress, message)
			server.close()
			return True
	except Exception as e:
		print("Failed to send email. Error ==> " + str(e))
		return False

def validateCode(returnToken,returnEmail=""):	
	try:
		tokenMetaData = jwt.decode(trimToken(returnToken), settings.JWTSECRET , algorithms=['HS256'])
		# Validate JWT
		if tokenMetaData["exp"] < int(time.time()):
			print("Failed to validate returning token. Error ==> Token Expired")
			return False
		elif returnEmail != "":
			if tokenMetaData["issuedFor"] != returnEmail:
				print("Failed to validate returning token. Error ==> Code not associated with email address specified")
				return False
			return True
		else:
			return True
	except Exception as e:
		print("Failed to validate returning token. Error ==> " + str(e))
		return False

def validateEmail(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def emailView(request):
    if request.method == "POST":
        email = request.POST['email']
        if validateEmail(email):
            code = generateCode(email)
            sendEmail(code)
            return HttpResponse("<h1>Link is sent to your Email ID</h1>")
    return render(request,'email.html')


def codeView(request,token):
	code = token
	email = request.GET.get('email')
	if validateCode(code,returnEmail=email):
		return redirect('home',token=code)	
	else:
		return render(request,'error.html')
    


def home(request,token):
    try:
        dec = jwt.decode(trimToken(token),settings.JWTSECRET,algorithms=['HS256'])
        if dec["issuedFor"] == cg.tokenMetaData['issuedFor']:
            return render(request,'home.html',{'email': dec["issuedFor"]})
        else:
            return HttpResponse("<h1>You are not loggedIn,Code is expired or User is not associatd with this code</h1>")
    except Exception as e:
        return HttpResponse("<h1>Sorry,Your code is not valid</h1>")