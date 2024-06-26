from django.contrib.auth.hashers import make_password,check_password
from lmiApp.models import *
from django.forms.models import model_to_dict
from django.core.exceptions import *
import uuid,json
from django.core.validators import validate_email
import re
from django.core.exceptions import ValidationError

def createAccount(data,msg):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        dob = data.get('dob')
        email = data.get('email')
        is_hr = data.get("is_hr")
        password = data.get('password')
        if not first_name or not last_name or not dob or not email or not password:
            msg["message"] = "All the fields are required"
            msg["status"] = 400
            return msg
        else:
            
            try:
                validate_email(email)
                validate_password(password)
                password = make_password(password)
                new_CustomUser =  CustomUser(
                first_name = first_name,
                last_name = last_name,
                dob=dob,
                email=email,
                is_hr = is_hr,
                password = password)
                new_CustomUser.save()
                resultset = model_to_dict(new_CustomUser)
                resultset.pop("password")
                msg["success"] = True
                msg["message"] = resultset
                return msg

            except Exception as e:
                msg["message"] = str(e)
                msg["status"] = 500
                return msg

def checkPassword(dbpass,bodypass):
     if check_password(bodypass,dbpass):
          return True
     return False

def createSession(request ,user):
    request.session.clear_expired()
    request.session['sessionID'] = str(uuid.uuid1())       
    request.session['email'] = user.email
    request.session['ID'] = user.id
    request.session['isHR'] = user.is_hr

def getUsersProfile(user):     
        user_data = model_to_dict(user)
        user_data.pop("password")
        return user_data

def login(data,msg,request):
    try:
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            msg["message"] = "Please provide email and password"
            msg["status"] = 400
            return msg
        user = CustomUser.objects.get(email=email)
        request.session.clear_expired()
        if 'email' in request.session.keys():
            msg["message"]="You are already logged in!!"
            msg["status"] = 409
            return msg
        result = checkPassword(user.password,password)
        if not result:
            msg["message"]="Invalid password. Check your credentials and attempt login again."
            msg["status"] = 403
            return msg
        createSession(request,user)
        msg["success"]=True     
        msg["status"] = 200
        msg["message"]=getUsersProfile(user)
        return msg
    except ObjectDoesNotExist as e:
            msg["status"] = 404
            msg["message"]="User with this email dosen't exists!!"   
            return msg
    except Exception as e:
        msg["status"] = 500
        msg["message"]=str(e)
        return msg

def logout(msg,request):
    try:
        request.session.set_expiry(0)       
        del request.session['sessionID']
        del request.session['email']
        del request.session['ID']
        del request.session['isHR']
        msg["success"] = True
        msg["status"] = 200
        msg["messsage"] = "Successfully logout !"
        return msg
    except Exception as e:
        msg["status"] = 500
        msg["message"] = str(e)
        return msg
    
def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search("[A-Z]", value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search("[0-9]", value):
        raise ValidationError("Password must contain at least one numeric digit.")
    if not re.search("[!@#$%^&*()_+=\-{};:'\"<>,.?/]", value):
        raise ValidationError("Password must contain at least one special character.")