from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import json
from asgiref.sync import async_to_sync


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        # self.user = self.scope["user"]
        # self.chatroom_name = self.scope["url_route"]["kwargs"].get("groupname", None)

        # if not self.user or not self.user.is_authenticated:
        #     self.close()  # Close connection if the user is not authenticated
        #     return

        # # Ensure the group exists
        # self.chatroom = get_object_or_404(GroupChatName, name=self.chatroom_name)

        # # Add the channel to the group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.chatroom_name, self.channel_name
        # )

        self.accept()

    # def disconnect(self, close_code):
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.chatroom_name, self.channel_name
    #     )

    # def receive(self, text_data):
    #     # Process the received data
    #     text_data_json = json.loads(text_data)
    #     body = text_data_json.get("body", "")

    #     # Create the message in the database
    #     message = GroupMessages.objects.create(
    #         body=body, author=self.user, group=self.chatroom
    #     )

    #     event = {"type": "message_handler", "message_id": message.id}

    #     async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    # def message_handler(self, event):
    #     # Render the new message as HTML
    #     message_id = event["message_id"]
    #     message = GroupMessages.objects.get(id=message_id)
    #     context = {"message": message, "user": self.user}
    #     html = render_to_string("voting_p.html", context)

    #     # Send the rendered HTML back to the client
    #     self.send(text_data=json.dumps({"html": html}))
