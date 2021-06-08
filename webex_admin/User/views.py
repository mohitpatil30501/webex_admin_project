import base64
import datetime
import json

import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import *
from webex_admin.settings import SECRET_KEY

from Dashboard.models import *

from conference.models import *

from webex_admin.settings import CLIENT_ID, CLIENT_SECRET, CLIENT_URL

from conference.models import AccessToken


def teacher_create(request):
    if request.method == "POST":
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Teacher.objects.filter(college_data__id=id, college_data__email=email).count() != 0:
            return render(request, "error/index.html",
                          {'error': 'Something Went Wrong', 'message': "ID already exist, Try to LogIn"})

        if User.objects.filter(username=username).count() != 0:
            return render(request, "error/index.html",
                          {'error': 'Something Went Wrong', 'message': "User Already Exist"})

        try:
            teacher_data = CollegeTeacherData.objects.filter(id=id, email=email).get()
        except:
            return render(request, "error/index.html",
                          {'error': 'Something Went Wrong',
                           'message': "College Data is Not Satisfies like: ID, Email"})

        try:
            user = User.objects.create_user(username, email=email, first_name=first_name,
                                            last_name=last_name, password=password)
        except:
            return render(request, "error/index.html",
                          {'error': 'Something Went Wrong',
                           'message': "Some data is Not Satisfies like: Username, Password, Email"})

        email_status = email_confirmation_send_to_teacher(user, request)
        if email_status:
            teacher = Teacher.objects.create(teacher=user, college_data=teacher_data)
            Details.objects.create(teacher=teacher, name=teacher.college_data.name, email=teacher.college_data.email)
            Designation.objects.create(teacher=teacher)
            user.is_active = False
            user.save()
            return redirect(CLIENT_URL + str(username))
        else:
            user.delete()
            return render(request, "error/index.html",
                          {'error': 'Email Server Down',
                           'message': "Problem to send email...!"})

    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Only POST method Allowed"})


def auth_signup(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "User/register.html")
    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Only POST method Allowed"})


def auth_login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "User/login.html", {'message': ''})
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).count() == 0:
            return render(request, "User/login.html", {'message': 'User Not Exist'})

        try:
            user = User.objects.filter(username=username).get()
            if not user.is_active:
                user_data = Teacher.objects.filter(teacher=user).get()
                if not user_data.email_verification:
                    return render(request, "User/login.html", {'message': 'Email is Not Verified'})
                return render(request, "User/login.html", {'message': 'User is InActive'})
        except:
            return render(request, "error/index.html",
                          {'error': 'Data Problem',
                           'message': "Failed to Extract Data..!"})

        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, "User/login.html", {'message': 'Incorrect Password'})

        login(request, user)
        return redirect('/dashboard')

    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Only POST method Allowed"})


def auth_logout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')

        return redirect('/')

    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Only POST method Allowed"})


def key_maker(username):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\xcfz\xfc\xdcF\xc1d\xc1\xb4\xfa5%\xe7\xa5\x14\x16',
        iterations=100000,
        backend=default_backend()
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(str(SECRET_KEY + username[::-1]).encode())))


def email_confirmation_send_to_teacher(user, request):
    # Key Making
    key = key_maker(user.username)

    # Collect Data
    # url : username={username}&data={encrypted data} //valid for 3 days

    data = {
        "username": user.username,
        "valid_time": str(datetime.datetime.today() + datetime.timedelta(days=3))
    }
    data = key.encrypt(json.dumps(data).encode()).decode()
    url = request.build_absolute_uri("/accounts/email_verification/teacher/" + user.username + "/" + data)

    message = '''
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
        <h1>SSBT</h1>
        <h3>Email Verification</h3>
        <form method="GET" action="''' + str(url) + ''''">
            <button type="submit">Click to Verify</button>
        </form>
        <hr>
        <p>Valid for 30 min only</p>
        <h2>If this mail is not relatable, Please Do not Click to Verify...!</h2>
    </body>
    </html>
    '''

    try:
        send_mail("Email Verification", "", "SSBT", [user.email, ], fail_silently=False, html_message=message)
        return True
    except:
        return False


def email_verification_of_teacher(request, username, data):
    # Key Making
    key = key_maker(username)
    try:
        data = key.decrypt(data.encode()).decode()
        data = json.loads(data)

        valid_time = datetime.datetime.strptime(data["valid_time"], '%Y-%m-%d %H:%M:%S.%f')

        if datetime.timedelta(0) <= valid_time - datetime.datetime.today() <= datetime.timedelta(3) and username == \
                data['username']:
            # change state to Active
            try:
                user = User.objects.filter(username=username).get()
                user.is_active = True
                user.save()
                teacher_data = Teacher.objects.filter(teacher=user).get()
                teacher_data.email_verification = True
                teacher_data.save()
            except:
                return render(request, "error/index.html",
                              {'error': 'Data Problem',
                               'message': "Unable to Extract user data...!"})
            return redirect('/')

        return render(request, "error/index.html",
                      {'error': 'Expired Link',
                       'message': "Link is Not Valid...!"})
    except:
        return render(request, "error/index.html",
                      {'error': 'Something went wrong',
                       'message': "Something went wrong...!"})


# forgot_password
def forgot_password(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return render(request, "User/forgot_password.html")
        return redirect('/')
    elif request.method == "POST":
        username = request.POST.get('username')
        if User.objects.filter(username=username).count() == 0:
            return render(request, "User/forgot_password.html", {'message': 'User Not Exist'})

        try:
            user = User.objects.filter(username=username).get()
            try:
                if Teacher.objects.filter(teacher=user).count() != 0:
                    student = Teacher.objects.filter(teacher=user).get()
                else:
                    return render(request, "User/forgot_password.html",
                                  {'message': "User Not Found"})
            except:
                return render(request, "User/forgot_password.html", {'message': "User Found, But Doesn't have Role."})
            key = key_maker(user.username)
            data = {
                "username": user.username,
                "valid_time": str(datetime.datetime.today() + datetime.timedelta(minutes=5))
            }
            data = key.encrypt(json.dumps(data).encode()).decode()
            url = request.build_absolute_uri("/accounts/reset_password/" + user.username + "/" + data)

            message = '''
                <!DOCTYPE html>
                <html>
                <head>
                </head>
                <body>
                    <h1>SSBT</h1>
                    <h3>Reset Password</h3>
                    <form method="GET" action="''' + str(url) + ''''">
                        <button type="submit">Click to Verify</button>
                    </form>
                    <hr>
                    <p>Valid for 5 min only</p>
                    <h2>If this mail is not relatable, Please Do not Click to Verify...!</h2>
                </body>
                </html>
                '''

            try:
                send_mail("Reset Password", "", "SSBT", [user.email, ], fail_silently=False, html_message=message)
                student.password_state = False
                student.save()
                return render(request, "User/forgot_password.html", {'message': 'Email Send Successfully'})
            except:
                return render(request, "User/forgot_password.html", {'message': 'Failed to Send Email'})

        except:
            return render(request, "error/index.html",
                          {'error': 'Something Went Wrong',
                           'message': "Data Extraction Problem"})

    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Only POST method Allowed"})


# reset Password
def reset_password_get(request, username, data):
    if request.method == "GET":
        key = key_maker(username)
        try:
            data = key.decrypt(data.encode()).decode()
            data = json.loads(data)

            valid_time = datetime.datetime.strptime(data["valid_time"], '%Y-%m-%d %H:%M:%S.%f')

            if datetime.timedelta(minutes=0, seconds=0) <= valid_time - datetime.datetime.today() <= datetime.timedelta(
                    minutes=5, seconds=0) and username == data['username']:
                # change state to Active
                try:
                    user = User.objects.filter(username=username).get()
                    if Teacher.objects.filter(teacher=user).count() != 0:
                        student_data = Teacher.objects.filter(teacher=user).get()
                    else:
                        return render(request, "User/login.html", {'message': 'User Have No Role.'})
                    if student_data.password_state:
                        return render(request, "error/index.html",
                                      {'error': 'Invalid Link',
                                       'message': "Link is Used or Expired"})
                    return render(request, "User/reset_password.html", {'id': student_data.id})
                except:
                    return render(request, "error/index.html",
                                  {'error': 'Data Problem',
                                   'message': "Unable to Extract user data...!"})
                # return JsonResponse({
                #     'username': username,
                #     'data': data,
                #     'valid_status': True
                # })
            return render(request, "error/index.html",
                          {'error': 'Expired Link',
                           'message': "Link is Not Valid...!"})
        except:
            return render(request, "error/index.html",
                          {'error': 'Something went wrong',
                           'message': "Something went wrong...!"})

    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Not Found-404"})


def reset_password_post(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                student = None
                if Teacher.objects.filter(teacher=request.user).count() != 0:
                    student = Teacher.objects.filter(teacher=request.user).get()
                if student is not None:
                    return render(request, "User/reset_password.html", {'id': student.id})
                return redirect('/')
            except:
                return render(request, "error/index.html",
                              {'error': 'Data Problem',
                               'message': "Unable to Extract user data...!"})
        else:
            return redirect('/')

    elif request.method == "POST":
        id = request.POST.get('id')
        password = request.POST.get('password')

        try:
            student = None
            if Teacher.objects.filter(id=id).count() != 0:
                student = Teacher.objects.filter(id=id).get()
            if student is None:
                return render(request, "error/index.html",
                              {'error': 'Data Problem',
                               'message': "Unable to Extract user data...!"})

            if student.password_state and not request.user.is_authenticated:
                return render(request, "User/login.html", {'message': 'Password is Already Reset or Unchanged'})

            if Teacher.objects.filter(id=id).count() != 0:
                student.teacher.set_password(password)
                student.teacher.save()

            student.password_state = True
            student.save()

            if request.user.is_authenticated:
                logout(request)

            return render(request, "User/login.html", {'message': 'Password Set Successful'})
        except:
            return render(request, "error/index.html",
                          {'error': 'Data Problem',
                           'message': "Unable to Extract user data...!"})
    return render(request, "error/index.html",
                  {'error': 'Wrong Method',
                   'message': "Not Found-404"})


def oauth(request):
    headers = {'Content-Type': 'application/json'}
    code = request.GET.get('code')
    username = request.GET.get('state')
    redirect_uri = ""

    if User.objects.filter(username=username).count() == 0:
        return render(request, "error/index.html",
                      {'error': 'Something Went Wrong',
                       'message': "User not found or Invalid link"})
    else:
        user = User.objects.filter(username=username).get()

    url = "https://api.ciscospark.com/v1/access_token"
    body = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(url, headers=headers, data=json.dumps(body)).json()

    token_data = AccessToken.objects.create(id=uuid.uuid4(), user=user, token=response['access_token'],
                                            refresh_token=response['refresh_token'])

    if datetime.datetime.now(datetime.timezone.utc) - token_data.last_modification >= datetime.timedelta(
            days=10):
        headers = {'Content-Type': 'application/json'}
        url = "https://api.ciscospark.com/v1/access_token"
        body = {
            'grant_type': 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': token_data.refresh_token
        }
        response = requests.post(url, headers=headers, data=json.dumps(body)).json()
        token_data.token = response['token']
        token_data.refresh_token = response['refresh_token']
        token_data.save()

    headers = {
        'Authorization': f'Bearer {token_data.token}',
        'Content-Type': 'application/json'
    }

    url = f"https://webexapis.com/v1/people?email={user.email}"
    response = requests.get(url, headers=headers).json()

    cisco_id = response['items'][0]['id']
    TeacherData.objects.create(id=uuid.uuid4(), name=str(user.first_name + ' ' + user.last_name), cisco_id=cisco_id)

    return render(request, "User/email.html", {'status': True,
                                               'email_status': True,
                                               'message': "Account created Successfully...."
                                               })
