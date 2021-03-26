import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import *
from User.models import *


class DetailsConsumer(AsyncWebsocketConsumer):
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
        if text_data_json['process'] == 'details-form-submission':
            if await self.verify_user(text_data_json['data']):
                response = await self.save_details(text_data_json['data'])
                if response['status']:
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'details-form-submission',
                            'status': True,
                            'data': response['data']
                        }
                    )
                else:
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'details-form-submission',
                            'status': False,
                            'error': response['error']
                        }
                    )
            else:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'details-form-submission',
                        'status': False,
                        'error': 'Not valid User..! Something Went Wrong, Please Try Again..!'
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
    def save_details(self, data):
        try:
            details = Details.objects.filter(id=data['id'], teacher__id=data['teacher']).get()

            details.name = data['name']
            if data['website'] == '':
                details.website = None
            else:
                details.website = data['website']

            details.email = data['email']

            if data['phone'] == '':
                details.phone = None
            else:
                details.phone = data['phone']

            if data['mobile'] == '':
                details.mobile = None
            else:
                details.mobile = data['mobile']

            if data['address'] == '':
                details.address = None
            else:
                details.address = data['address']

            if data['date_of_birth'] == '':
                details.date_of_birth = None
            else:
                details.date_of_birth = data['date_of_birth']
            details.save()

            return {
                'status': True,
                'data': {
                    'teacher': str(details.teacher.id),
                    'id': str(details.id),
                    'name': details.name,
                    'website': details.website,
                    'email': details.email,
                    'phone': details.phone,
                    'mobile': details.mobile,
                    'address': details.address,
                    'date_of_birth': details.date_of_birth,
                }
            }
        except:
            return {
                'status': False,
                'error': 'Data Not Found..!'
            }

    @database_sync_to_async
    def verify_user(self, data):
        if Details.objects.filter(id=data['id'], teacher__id=data['teacher']).count() != 0:
            return True
        return False


class DesignationConsumer(AsyncWebsocketConsumer):
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
        if text_data_json['process'] == 'designation-form-submission':
            if await self.verify_user(text_data_json['data']):
                response = await self.save_designation(text_data_json['data'])
                if response['status']:
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'designation-form-submission',
                            'status': True,
                            'data': response['data']
                        }
                    )
                else:
                    await self.channel_layer.group_send(
                        self.id,
                        {
                            'type': 'send_status',
                            'process': 'designation-form-submission',
                            'status': False,
                            'error': response['error']
                        }
                    )
            else:
                await self.channel_layer.group_send(
                    self.id,
                    {
                        'type': 'send_status',
                        'process': 'designation-form-submission',
                        'status': False,
                        'error': 'Not valid User..! Something Went Wrong, Please Try Again..!'
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
    def verify_user(self, data):
        if Designation.objects.filter(id=data['id'], teacher__id=data['teacher']).count() != 0:
            return True
        return False

    @database_sync_to_async
    def save_designation(self, data):
        try:
            designation = Designation.objects.filter(id=data['id'], teacher__id=data['teacher']).get()

            designation.designation = data['designation'] if data['designation'] is not None else None
            designation.department = data['department'] if data['department'] is not None else None
            designation.institute = data['institute'] if data['institute'] is not None else None

            designation.save()

            return {
                'status': True,
                'data': {
                    'teacher': str(designation.teacher.id),
                    'id': str(designation.id),
                    'designation': designation.designation,
                    'department': designation.department,
                    'institute': designation.institute,
                }
            }
        except:
            return {
                'status': False,
                'error': 'Data Not Found..!'
            }
