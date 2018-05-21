# -*- coding: UTF-8 -*-
from usr import Usr
from preference import available_pre
from room_request import Room_request
from flask_pymongo import  PyMongo

'''
ver 1.0
功能：
1.房间加人、设置房主
2.编辑房间基本信息（name、subarea）
3.激活房间
4.创建、删除房间
5.搜索房间

需要添加功能：
1.删除某人
2.满足人数组团成功
3.条件筛选
4.state应拥有更多含义
5.按照description模糊搜索
'''


class Room(object):
    def __init__(self, id):
        self.id = id  # id一经设置不能改变
        self.name = ""
        self.subarea = ""
        self.description = ""
        self.room_owner_id = -1
        self.usrs_id = []
        self.state = 0  # 0为未激活，1为激活

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getSubarea(self):
        return self.subarea
    
    def getDescription(self):
        return self.description

    def getRoom_owner(self):
        return self.room_owner_id

    def getUsrs(self):
        return self.usrs_id

    def getState(self):
        return self.state

    def setName(self, name):
        if isinstance(name, str):
            self.name = name
            return True
        print("error: ", name, " is not a string!")
        return False

    def setSubarea(self, subarea):
        if Usr.checkPre(subarea):
            self.subarea = subarea
            return True
        print("error: ", subarea, " is not an available subarea!")
        return False
    
    def setDescription(self,description):
        if isinstance(description, str):
            self.description = description
            return True
        print("error: description must be str!")
        return False

    def addUsr(self, usrid):
        # 只判断id是否大于0，不检查usrid合法性(即是否存在这个用户)
        if usrid < 0:
            print("error: usrid must not less than zero!")
            return False
        if usrid not in self.usrs_id:
            self.usrs_id.append(usrid)
        return True

    def setRoom_owner(self, usrid):
        # 只判断id是否大于0，不检查usrid合法性(即是否存在这个用户)，总会把房主id加入房间
        # Date-X.py中会检查用户合法性
        if usrid < 0:
            print("error: usrid must not less than zero!")
            return False
        self.room_owner_id = usrid
        self.addUsr(usrid)
        return True

    def active(self):
        # 改变state的唯一接口
        if self.id < 0:
            print("error: check room id failed!")
            return False
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
        if not self.usrs_id:
            print("error: check room usrs failed!")
            return False
        self.state = 1
        return True


class Room_manager(object):
    def __init__(self, db):
        self.db = db
        self.next_id = 0
        self.rooms = []
        self.subareas2num = {}  # 每个分区的房间人数
        self.room_id2id = {}  # 一般情况下，第i个房间的id就是i

    def getNext_id(self):
        return self.next_id

    def getRooms(self):
        return self.rooms

    def getRoombyroomid(self, room_id):
        if room_id in self.room_id2id:  # 这里发现room_id2id是有必要的，它可以用来表示id为i的房间是否存在
            return self.rooms[self.room_id2id[room_id]]
        print("error: room id ", room_id, "does not exists!")
        return None

    def getRoom_id2id(self):
        return self.room_id2id

    def addRoom(self):
        # 自动分配房间id，总是返回true
        self.rooms.append(Room(self.next_id))
        self.room_id2id[self.next_id] = self.next_id
        self.next_id += 1
        return True

    def deleteRoom(self, room_id):
        if room_id not in self.room_id2id:
            print("error: room ", room_id, " does not exist!")
            return False
        self.room_id2id.pop(room_id)
        return True

    def printRooms(self):
        count = 0
        for room in self.rooms:
            print("===================Room ", count, "===================")
            print("id:", room.getId())
            if room.getState() == 0:
                print("state: Unactivated")
            if room.getState() == 1:
                print("state: Acticated")
            print("name:", room.getName())
            print("subarea:", room.getSubarea())
            print("room owner:", room.getRoom_owner())
            print("room usrs:", room.getUsrs())
            count += 1
        
    def addRoombyreq(self, request, db):
        #根据request创建房间，成功返回房间id，失败返回False
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return False
        if not request.checkReq():
            print("error: can not establish room with your request!")
            return False
        room_tb = db.room
        print(room_tb.insert_one(request).insert_id)
        room_id = self.next_id
        self.addRoom()
        self.setName(room_id, request.getName())
        self.setSubarea(room_id,request.getSubarea())
        self.setDescription(room_id,request.getDescription())
        self.setRoom_owner(room_id,request.getRoom_owner())
        if self.active(room_id):
            return room_id
    
    def searchRoom(self, request):
        #根据request搜索房间，返回符合条件的房间id的list
        #暂不支持按description搜索
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return False
        res = []
        for room in self.rooms:
            if request.name != "" and request.name != room.name:
                continue
            if request.subarea != "" and request.subarea != room.subarea:
                continue
            if request.room_owner_id != "" and request.room_owner_id != room.room_owner_id:
                continue
            res.append(room.getId())
        return res


    #下面这些函数是对room对应函数的封装，使得所有操作都在room manager中进行
    def getId(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getId()
        print("error: room ", room_id, " does not exist!")
        return False

    def getName(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getName()
        print("error: room ", room_id, " does not exist!")
        return False

    def getSubarea(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getSubarea()
        print("error: room ", room_id, " does not exist!")
        return False

    def getDescription(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getDescription()
        print("error: room ", room_id, " does not exist!")
        return False

    def getRoom_owner(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getRoom_owner()
        print("error: room ", room_id, " does not exist!")
        return False

    def getUsrs(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getUsrs()
        print("error: room ", room_id, " does not exist!")
        return False

    def getState(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].getState()
        print("error: room ", room_id, " does not exist!")
        return False

    def setName(self, room_id, name):
        if room_id in self.room_id2id:
            return self.rooms[room_id].setName(name)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def setSubarea(self, room_id, subarea):
        if room_id in self.room_id2id:
            old_subarea = self.rooms[room_id].getSubarea()
            new_subarea = subarea
            if old_subarea != "":
                self.subareas2num[old_subarea] -= 1
            if Usr.checkPre(new_subarea):
                self.subareas2num[new_subarea] += 1
            return self.rooms[room_id].setSubarea(subarea)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def setDescription(self, room_id, description):
        if room_id in self.room_id2id:
            return self.rooms[room_id].setDescription(description)
        print("error: room ", room_id, " does not exist!")
        return False

    def addUsr(self, room_id, usrid):
        if room_id in self.room_id2id:
            return self.rooms[room_id].addUsr(usrid)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def setRoom_owner(self, room_id, usrid):
        if room_id in self.room_id2id:
            return self.rooms[room_id].setRoom_owner(usrid)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def active(self, room_id):
        if room_id in self.room_id2id:
            return self.rooms[room_id].active()
        print("error: room ", room_id, " does not exist!")
        return False