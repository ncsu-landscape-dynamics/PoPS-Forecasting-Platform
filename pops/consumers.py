import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

class DashboardConsumer(JsonWebsocketConsumer):
    print('____________________')
    print('DashboardConsumer class entered.')

    def connect(self):
        print('Connecting...')
        self.session_id = self.scope['url_route']['kwargs']['session']
        self.session_group_id = 'chat_%s' % self.session_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_id,
            self.channel_name
        )
        print('Connection finished.')
        self.accept()

    def disconnect(self, close_code):
        print('Disconnecting...')
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.session_group_id,
            self.channel_name
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