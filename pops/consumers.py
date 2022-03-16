import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from django.contrib.auth.mixins import LoginRequiredMixin
from channels.auth import login

from .models import Run, RunCollection
import channels.layers
from django.db.models import signals
from django.dispatch import receiver

class DashboardConsumer(JsonWebsocketConsumer, LoginRequiredMixin):
    print('____________________')
    print('DashboardConsumer class entered.')

    def connect(self):
        print('Connecting...')
        print(self.scope["user"])
        username=str(self.scope["user"])
        try :
            async_to_sync(login)(self.scope, self.scope["user"])
            print('User approved')
        except Exception:
            self.close()
            print('Closing connection due to unsuccesful user login')
            return
        self.session_id = self.scope['url_route']['kwargs']['session']
        self.session_group_id = 'chat_%s' % self.session_id
        # Join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_id,
            self.channel_name
        )
        x = {
            'jsonrpc': '2.0',
            'method': 'new_connection_detected',
            'params': {'user': username},
        }
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_id,
            {
                'type': 'chat_message',
                'content': x
            }
        )       
        self.accept()
        #len(self.channel_layer.groups.get('self.session_group_id', {}).items())
        print('Connection finished.')

    def disconnect(self, close_code):
        username=str(self.scope["user"])
        print('Disconnecting...')
        # Leave room group
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.session_group_id,
                self.channel_name
            )
        except:
            return
        x = {
            'jsonrpc': '2.0',
            'method': 'connection_removed',
            'params': {'user': username},
        }
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_id,
            {
                'type': 'chat_message',
                'content': x
            }
        )       
        print('Disconnection complete.')


    # Receive message from WebSocket
    def receive_json(self, data):
        print('Received message from websocket')
        print(data)
        s1 = json.dumps(data)
        incoming_data = json.loads(s1)
        method = incoming_data['method']
        params = incoming_data['params']
        if method == 'update_management':
            print('Updating management')
        elif method == 'new_run_collection':
            print('Adding new run collection to session')
        elif method == 'send_management_request':
            print('Sending management request to other users')
        elif method == 'run_pops':
            print('Run PoPS button clicked by user.')
        elif method == 'update_user':
            print('User changed run collections')
            #self.send_json(x)
        # Send message to room group
        # This iteratively performs the 'chat_message' function
        # for every member of the group            
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_id,
            {
                'type': 'chat_message',
                'content': data
            }
        )       
        print('Finished receive function')

    # Send message from room group
    def chat_message(self, event):
        print('Sending chat_message to room group')
        #print(event)
        message = event['content']
        #print(message)
        # Send message to WebSocket
        self.send_json(message)
        print('Finished chat message')

    def events_alarm(self, event):
        print('Event alarm triggered')
        x = {
            'jsonrpc': '2.0',
            'method': 'new_run_collection',
            'params': json.loads(event['content']),
        }
        print(json.dumps(x))

        self.send_json(x)

    def send_management_request(self, event):
        print('Requesting management from clients')
        x = {
            'jsonrpc': '2.0',
            'method': 'send_current_management',
            'params': {'run_collection': 42},
        }
        print(json.dumps(x))
        self.send_json(x)

    @staticmethod
    @receiver(signals.post_save, sender=Run, weak=False)
    def run_status_change(sender, instance, **kwargs):
        print(sender)
        print(instance)
        print(instance.status)
        print(instance.run_collection.session.pk)
        layer = channels.layers.get_channel_layer()
        group_name = 'chat_%s' % instance.run_collection.session.pk
        data = {
            'jsonrpc': '2.0',
            'method': 'run_status_update',
            'params': {
                'run_pk': instance.pk,
                'run_collection': instance.run_collection.pk,
                'status': instance.status,
                },
        }
        async_to_sync(layer.group_send)(group_name, {
                'type': 'chat_message',
                'content': data
        })
        
    @staticmethod
    @receiver(signals.post_save, sender=RunCollection, weak=False)
    def new_run_collection(sender, instance, **kwargs):
        print(sender)
        print(instance)
        print(instance.date_created)
        layer = channels.layers.get_channel_layer()
        group_name = 'chat_%s' % instance.session.pk
        data = {
            'jsonrpc': '2.0',
            'method': 'new_run_collection',
            'params': {
                'run_collection': instance.pk,
                'name': instance.name,
                'date': instance.date_created.strftime("%B %d, %Y, %X"),
                'description': instance.description,
                },
        }
        async_to_sync(layer.group_send)(group_name, {
                'type': 'chat_message',
                'content': data
        })