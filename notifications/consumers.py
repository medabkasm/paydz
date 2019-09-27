
from channels.generic.websocket import AsyncWebsocketConsumer , WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification , Message
from accounts.models import User
from offers.models import Offer
from django.core import serializers
from django.forms.models import model_to_dict
import json


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):   # get a websocket connection.

        if(self.scope["user"].is_superuser):
            await self.channel_layer.group_add(
                "AdminGroup",
                self.channel_name
                )
            await self.accept()
            await self.new_notification(self.scope)  # to initialize a web socket connection with unseen notifications and messages.
            await self.new_message(self.scope)
        else:
            await self.close()

    async def disconnect(self, close_code):  # discard a websocket connection.
        await self.channel_layer.group_discard(
            "AdminGroup",
            self.channel_name
        )



    async def new_notification(self,event):

        self.unseenNotificationsList = await self.get_unseen_notifcations(None,True)
        self.unseenNotifications = self.unseenNotificationsList[0]  # get all notifications with seen = False , (Queryset).
        self.unseenNotifsCount = self.unseenNotificationsList[1]  # the latest created notification model.
        if self.unseenNotifsCount > 0 :
            self.lastOffer = self.unseenNotifications[0].notif  # the last notification , is the last notification created.
            self.notifier = self.lastOffer.user
            self.notifsListObj = []  # the number of unseen notifs .
            self.notifsDict = {"username":"" , "fields": ""}
            for notification in self.unseenNotifications:
                self.notif = serializers.serialize('json',[notification.notif,])  # json data with wrapper with [].
                self.notif = json.loads(self.notif)  # get ride of [].
                self.user = await self.get_username(None,True,self.notif[0]['pk'])
                self.username = self.user.username
                self.phone = self.user.phone
                self.notifsDict["username"] = self.username
                self.notifsDict["phone"] = self.phone
                self.notifsDict["fields"] = self.notif[0]['fields']
                self.notifsListObj.append(self.notifsDict.copy())
            self.type = "notification"
        else:
            self.type = "no notifications"
            self.unseenNotifsCount = 0
            self.notifsListObj = None

        await self.send(json.dumps({
            "type": self.type,
            "count": self.unseenNotifsCount,
            "content": self.notifsListObj
        }))


    async def new_message(self,event):
        self.unseenNotificationsList = await self.get_unseen_notifcations(True,None)
        self.unseenNotifications = self.unseenNotificationsList[0]  # get all notifications with seen = False , (Queryset).
        self.unseenNotifsCount = self.unseenNotificationsList[1]  # the latest created notification model.
        
        if self.unseenNotifsCount > 0 :
            self.lastMsg = self.unseenNotifications[0].msg  # the last message , is the last notification created.
            self.notifier = self.lastMsg.user
            self.msgsListObj = []  # the number of unseen notifs .
            self.msgsDict = {}
            for notification in self.unseenNotifications:
                self.msg = serializers.serialize('json',[notification.msg,])  # json data with wrapper with [].
                self.msg = json.loads(self.msg)  # get ride of [].
                self.user = await self.get_username(True,None,self.msg[0]['pk'])
                self.username = self.user.username
                self.phone = self.user.phone
                self.msgsDict["username"] = self.username
                self.msgsDict["phone"] = self.phone
                self.msgsDict["fields"] = self.msg[0]['fields']
                self.msgsListObj.append(self.msgsDict.copy())
            self.type = "message"
        else:
            self.type = "no messages"
            self.unseenNotifsCount = 0
            self.msgsListObj = None

        await self.send(json.dumps({
            "type": self.type,
            "count": self.unseenNotifsCount,
            "content": self.msgsListObj
        }))





    @database_sync_to_async
    def get_username(self,msg,notif,pk):
        if msg == None:
            return Offer.objects.get(pk = pk).user # get the latest created notification model.
        else:
            return Message.objects.get(pk = pk).user # get the latest created notification model.

    @database_sync_to_async
    def get_unseen_notifcations(self,msg,notif):
        if msg == None:
            try:
                return [ Notification.objects.filter(seen = False,msg=None).order_by('-date') , Notification.objects.filter(seen = False,msg=None).count() ]
            except:
                return None
        else:
            try:
                return [ Notification.objects.filter(seen = False,notif=None).order_by('-date') , Notification.objects.filter(seen = False,notif=None).count() ]
            except:
                return None
