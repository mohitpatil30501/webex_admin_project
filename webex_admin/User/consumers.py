import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']

        # Join room group
        await self.channel_layer.group_add(
            self.id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # teacher
        if text_data_json['process'] == 'signup-verify-teacher':
            if await self.id_check(text_data_json['data']['id']) != 0:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'signup-verify-teacher',
                        'status': False,
                        'error': 'ID already exist, Try to LogIn...!'
                    }
                )
            else:
                data = await self.signup_verify_teacher(text_data_json['data'])
                status = data['status']
                if status:
                    await self.id_session(text_data_json['data']['id'])
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'signup-verify-teacher',
                            'status': status,
                            'data': data['data']
                        }
                    )
                else:
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'signup-verify-teacher',
                            'status': status,
                            'error': data['error']
                        }
                    )
        elif text_data_json['process'] == 'username-availability-teacher':
            username = text_data_json['username']
            count = await self.username_check_teacher(username)
            if count != 0:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'username-availability-teacher',
                        'status': False,
                        'error': 'Username Already Exists...!'
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'username-availability-teacher',
                        'status': True,
                        'data': 'Username Available'
                    }
                )
        elif text_data_json['process'] == 'password-availability-teacher':
            password = text_data_json['password']
            username = text_data_json['username']
            data = await self.password_check_teacher(password, username)
            if not data['status']:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'password-availability-teacher',
                        'status': False,
                        'error': data['error']
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'password-availability-teacher',
                        'status': True,
                        'data': data['data']
                    }
                )

    async def send_status(self, event):
        if event['status']:
            await self.send(text_data=json.dumps({
                'process': event['process'],
                'status': event['status'],
                'data': event['data']
            }))
        else:
            await self.send(text_data=json.dumps({
                'process': event['process'],
                'status': event['status'],
                'error': event['error']
            }))

    # teacher Functions
    @database_sync_to_async
    def signup_verify_teacher(self, data):
        try:
            user = CollegeTeacherData.objects.filter(id=data['id']).get()
            return {
                'status': True,
                'data': {
                    'id': user.id,
                    'name': user.name,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
            }
        except:
            return {
                'status': False,
                'error': 'Invalid ID'
            }

    @database_sync_to_async
    def id_check(self, id):
        return Teacher.objects.filter(college_data__id=id).count()

    @database_sync_to_async
    def id_session(self, id):
        self.scope["session"]["id-teacher"] = id

    @database_sync_to_async
    def username_check_teacher(self, username):
        return User.objects.filter(username=username).count()

    @database_sync_to_async
    def password_check_teacher(self, password, username):
        if len(password) < 8:
            return {
                'status': False,
                'error': 'Password must be at least 8 characters'
            }
        if len(username) == 0:
            return {
                'status': False,
                'error': 'Please Set Username First'
            }
        capital = small = number = symbol = False
        id = self.scope["session"]["id-teacher"]
        try:
            data = CollegeTeacherData.objects.filter(id=id).get()
            data = [data.id, data.name, data.first_name, data.last_name, data.email]
        except:
            data = None
        if data is not None:
            for word in data:
                if word.upper() in password.upper() or password.upper() in word.upper():
                    return {
                        'status': False,
                        'error': 'Password must be not related to personal details'
                    }

            if username.upper() in password.upper() or password.upper() in username.upper():
                return {
                    'status': False,
                    'error': 'Password must be not related to personal details'
                }

            for c in password:
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    capital = True
                elif c in "abcdefghijklmnopqrstuvwxyz":
                    small = True
                elif c in "1234567890":
                    number = True
                elif c in r'''~`!@#$%^&*()_+-={}|[]\;':",./<>?''':
                    symbol = True
                elif c == ' ':
                    return {
                        'status': False,
                        'error': 'Password not contain whitespace'
                    }

            if not capital or not small or not number or not symbol:
                return {
                    'status': False,
                    'error': 'Password must be contain one Capital, Small, Number and Symbol character'
                }
            else:
                return {
                    'status': True,
                    'data': 'Password is suitable'
                }
        else:
            return {
                'status': False,
                'error': 'Problem to PRN Data..!'
            }


class UserResetPasswordConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['id']

        # Join room group
        await self.channel_layer.group_add(
            self.id,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['process'] == 'password-availability':
            password = text_data_json['password']
            id = text_data_json['id']
            data = await self.password_check(password, id)
            if not data['status']:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'password-availability',
                        'status': False,
                        'error': data['error']
                    }
                )
            else:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'password-availability',
                        'status': True,
                        'data': data['data']
                    }
                )

    async def send_status(self, event):
        if event['status']:
            await self.send(text_data=json.dumps({
                'process': event['process'],
                'status': event['status'],
                'data': event['data']
            }))
        else:
            await self.send(text_data=json.dumps({
                'process': event['process'],
                'status': event['status'],
                'error': event['error']
            }))

    @database_sync_to_async
    def password_check(self, password, id):
        if len(password) < 8:
            return {
                'status': False,
                'error': 'Password must be at least 8 characters'
            }
        if len(id) == 0:
            return {
                'status': False,
                'error': 'Something Went Wrong'
            }
        capital = small = number = symbol = False
        try:
            if Teacher.objects.filter(id=id).count() != 0:
                data = Teacher.objects.filter(id=id).get()
                data = [data.college_data.id, data.college_data.name, data.teacher.first_name, data.teacher.last_name,
                        data.college_data.email]
        except:
            data = None
        if data is not None:
            for word in data:
                if word.upper() in password.upper() or password.upper() in word.upper():
                    return {
                        'status': False,
                        'error': 'Password must be not related to personal details'
                    }

            for c in password:
                if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    capital = True
                elif c in "abcdefghijklmnopqrstuvwxyz":
                    small = True
                elif c in "1234567890":
                    number = True
                elif c in r'''~`!@#$%^&*()_+-={}|[]\;':",./<>?''':
                    symbol = True
                elif c == ' ':
                    return {
                        'status': False,
                        'error': 'Password not contain whitespace'
                    }

            if not capital or not small or not number or not symbol:
                return {
                    'status': False,
                    'error': 'Password must be contain one Capital, Small, Number and Symbol character'
                }
            else:
                return {
                    'status': True,
                    'data': 'Password is suitable'
                }
        else:
            return {
                'status': False,
                'error': 'Problem to PRN / ID Data..!'
            }
