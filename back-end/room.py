# -*- coding: UTF-8 -*-
from usr import Usr
from preference import available_pre
from room_request import Room_request
from flask_pymongo import  PyMongo
import datetime
import json

'''
ver 1.1
连接MongoDB 完成

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
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            return json.dumps({"response_code": 0})
        return json.dumps([{"response_code": 1}, res])

    def getRoom_id2id(self):
        return self.room_id2id

    ##不应该使用
    def addRoom(self):

        room = self.db.Room
        room.insert_one({})
        # 自动分配房间id，总是返回true
        # self.rooms.append(Room(self.next_id))
        # self.room_id2id[self.next_id] = self.next_id
        # self.next_id += 1
        return True

    def deleteRoom(self, room_id):
        res = self.db.Room.find_one({"_id":room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return json.dumps({"response_code":0})
        self.db.Room.delete_one({"_id":room_id})
        return json.dumps({"response_code":1})

    def deleteByID(self, room_id, usrid):
        res = self.db.Room.update_one({"_id":room_id},{"$pull":{"users":usrid}})
        if res.matched_count == 0:
            print("error: room ", room_id, " does not exist!")
            return json.dumps({"response_code":0})
        return json.dumps({"response_code":1})

    def printRooms(self):
        count = 0
        cursor = self.db.Room.find({})
        for room in cursor:
            print("===================Room ", room['_id'], "===================")
            print("id:", room['_id'])
            if room['active'] == 0:
                print("state: Unactivated")
            if room['active'] == 1:
                print("state: Acticated")
            print("name:", room['name'])
            print("subarea:", room['area'])
            print("room owner:", room['owner'])
            print("room usrs:", room['users'])
            # count += 1

    def addRoombyreq(self, request):
        #根据request创建房间，成功返回房间id，失败返回False
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return json.dumps({"response_code": 0})
        # if not request.checkReq():
        #     print("error: can not establish room with your request!")
        #     return json.dumps({"response_code": 0})
        room = self.db.Room
        room_id = room.insert_one({"name":request.getName(),"area":request.getSubarea(),
                                  "description":request.getDescription(),"owner":request.getRoom_owner(),
                                   "active":1,"users":[],"messages":[]}).inserted_id
        return json.dumps({"response_code":1,"room_id":room_id})
    
    def searchRoom(self, request):
        #根据request搜索房间，返回符合条件的房间id的list
        #暂不支持按description搜索

        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            json.dumps({"response_code": 0})

        room = db.Room
        query = {}
        # if request.getName() != "":
        #     query['name'] = request.getName()
        if request.getSubarea() != "":
            query['area'] = request.getSubarea()
        if request.getDescription() != "":
            query['description'] = request.getDescription()
        res = room.find(query)
        # res = [x['_id'] for x in res]
        # for room in self.rooms:
        #     if request.name != "" and request.name != room.name:
        #         continue
        #     if request.subarea != "" and request.subarea != room.subarea:
        #         continue
        #     if request.room_owner_id != "" and request.room_owner_id != room.room_owner_id:
        #         continue
        #     res.append(room.getId())
        return json.dumps([{"response_code": len(list(res)) != 0},list(res)])


    #下面这些函数是对room对应函数的封装，使得所有操作都在room manager中进行
    # def getId(self, room_id):
    #     res = self.db.Room.find_one({"_id": room_id})
    #     if res is None:
    #         print("error: room ", room_id, " does not exist!")
    #         return False
    #     return res['_id']

    def getName(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['name']
        old_usr = self.db.Room.find_one({"_id": room_id})['users']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getName()
        print("error: room ", room_id, " does not exist!")
        return False

    def getSubarea(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['area']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getSubarea()
        print("error: room ", room_id, " does not exist!")
        return False


    def getRoomByID(self, usrid):
        cur = self.db.Room.find({"usr": {"$all": [usrid]}})
        if cur.count() == 0:
            return json.dumps({"response_code":0})
        return json.dumps([{"response_code":1},list(cur)])

    def getRoomBySection(self, sec):
        cur = self.db.Room.find({"area": sec})
        if cur.count() == 0:
            return json.dumps({"response_code":0})
        return json.dumps([{"response_code":1},list(cur)])

    def getDescription(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['description']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getDescription()
        print("error: room ", room_id, " does not exist!")
        return False

    def getRoom_owner(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['owner']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getRoom_owner()
        print("error: room ", room_id, " does not exist!")
        return False

    def getUsrs(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['users']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getUsrs()
        print("error: room ", room_id, " does not exist!")
        return False

    def getState(self, room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['active']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getState()
        print("error: room ", room_id, " does not exist!")
        return False

    def setName(self, room_id, name):
        res = self.db.Room.update_one({"_id": room_id},{"name":name})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
    
    def setSubarea(self, room_id, subarea):
        res = self.db.Room.update_one({"_id": room_id}, {"subarea": subarea})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
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
        res = self.db.Room.update_one({"_id": room_id}, {"descriptioin": description})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].setDescription(description)
        print("error: room ", room_id, " does not exist!")
        return False

    def addUsr(self, room_id, usrid):
        old_usr = self.db.Room.find_one({"_id":room_id})['users']
        res = self.db.Room.update_one({"_id": room_id}, {"users": old_usr + usrid})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].addUsr(usrid)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def setRoom_owner(self, room_id, usrid):
        old_usr = self.db.Room.find_one({"_id": room_id})['owner']
        res = self.db.Room.update_one({"_id": room_id}, {"owner": usrid})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].setRoom_owner(usrid)
        print("error: room ", room_id, " does not exist!")
        return False
    
    def active(self, room_id):
        res = self.db.Room.update_one({"_id": room_id}, {"active": 1})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].active()
        print("error: room ", room_id, " does not exist!")
        return False

    def addMessage(self,room_id,usrid,content):
        entry = {"user":usrid,"content":content,"time":datetime.datetime.utcnow()}
        res = self.db.Room.update_one({"_id": room_id}, {"$push": {"messages":entry}})
        if res.matched_count is 0:
            print("error: room ", room_id, " or ", usrid," does not exist!")
            return json.dumps({"response_code": 0})
        return json.dumps({"response_code": 1})

    def getMessage(self,room_id):
        res = self.db.Room.find_one({"_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return json.dumps({"response_code":0})
        if len(res['messages']) == 0:
            return json.dumps({"response_code": 0})
        return json.dumps([{"response_code": 1},res['messages']])