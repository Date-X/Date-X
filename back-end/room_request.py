# -*- coding: UTF-8 -*-
import datetime
from usr import Usr


class Room_request(object):
    def __init__(self):
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.name = ""
        self.subarea = ""
        self.description = ""
        self.room_owner_id = -1
    
    def getTime(self):
        return self.time

    def getName(self):
        return self.name

    def getSubarea(self):
        return self.subarea
    
    def getDescription(self):
        return self.description

    def getRoom_owner(self):
        return self.room_owner_id

    def setTime(self):
        #将时间更改为当前时间，总是返回True
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return True
    
    def setName(self, name):
        # if isinstance(name, str):
        self.name = name
        return True
        # print("error: ", name, " is not a string!")
        # return False

    def setSubarea(self, subarea):
        # if Usr.checkPre(subarea):
        self.subarea = subarea
        return True
        # print("error: ", subarea, " is not an available subarea!")
        # return False
    
    def setDescription(self,description):
        # if isinstance(description, str):
        self.description = description
        return True
        # print("error: description must be str!")
        # return False

    def setRoomowner(self, room_owner_id):
        self.room_owner_id = room_owner_id

    
    def checkReq(self):
        #查看该request实例是否满足创建房间的需求
        if not isinstance(self.name, str) or self.name == "":
            print("error: check room name failed!")
            return False
        if not Usr.checkPre(self.subarea):
            print("error: check room subarea failed!")
            return False
        if not isinstance(self.description, str) or self.description == "":
            print("error: check room description failed!")
            return False
        if self.room_owner_id < 0:
            print("error: check room owner failed!")
            return False
        return True
