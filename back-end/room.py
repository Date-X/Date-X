# -*- coding: UTF-8 -*-
# from usr import Usr
from preference import available_pre
from room_request import Room_request
from flask_pymongo import  PyMongo
import datetime
import json
from bson.json_util import dumps
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

class Room_manager(object):
    def __init__(self, db):
        self.db = db
        self._id = 0
        self.rooms = []
        self.subareas2num = {}  # 每个分区的房间人数
        self.room_id2id = {}  # 一般情况下，第i个房间的id就是i

    def getRoombyroomid(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            return dumps({"response_code": 0})

        res['owner'] = self.db.User.find_one({"id":res['owner']})
        for i,usr in enumerate(res['users']):
            res['users'][i] = self.db.User.find_one({"id":usr})

        return dumps([{"response_code": 1}, res])

    def getRoom_id2id(self):
        return self.room_id2id

    def deleteRoom(self, room_id):
        res = self.db.Room.find_one({"room_id":room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code":0})
        self.db.Room.delete_one({"room_id":room_id})
        return dumps({"response_code":1})

    def deleteByID(self, room_id, usrid):
        res = self.db.Room.update_one({"room_id":(room_id)},{"$pull":{"users":usrid}})
        if res.matched_count == 0:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code":0})
        return dumps({"response_code":1})

    def addRoombyreq(self, request):
        #根据request创建房间，成功返回房间id，失败返回False
        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            return dumps({"response_code": 0})
        # if not request.checkReq():
        #     print("error: can not establish room with your request!")
        #     return dumps({"response_code": 0})
        room = self.db.Room
        id = 0
        res = room.find({}).sort("room_id")
        if res.count() != 0:
            id = room.find({}).sort("room_id",-1)[0]['room_id'] + 1
        room.insert_one({"room_id":id,"name":request.getName(),"area":request.getSubarea(),
                                  "description":request.getDescription(),"owner":request.getRoom_owner(),
                                   "active":1,"users":[request.getRoom_owner()],"messages":[]})
        # self._id += 1
        return dumps({"response_code":1,"room_id":id})

    def searchRoom(self, request):
        #根据request搜索房间，返回符合条件的房间id的list
        #暂不支持按description搜索

        if not isinstance(request, Room_request):
            print("error: request type is wrong!")
            dumps({"response_code": 0})

        room = self.db.Room
        query = {}
        # if request.getName() != "":
        #     query['name'] = request.getName()
        if request.getSubarea() != "":
            query['area'] = request.getSubarea()
        if request.getDescription() != "":
            query['description'] = request.getDescription()
        res = room.find(query)

        cur = [x for x in res]
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.User.find_one({"id":room['owner']})
            for i,usr in enumerate(room['users']):
                room['users'][i] = self.db.User.find_one({"id":usr})

        # res = [x['_id'] for x in res]
        # for room in self.rooms:
        #     if request.name != "" and request.name != room.name:
        #         continue
        #     if request.subarea != "" and request.subarea != room.subarea:
        #         continue
        #     if request.room_owner_id != "" and request.room_owner_id != room.room_owner_id:
        #         continue
        #     res.append(room.getId())
        return dumps([{"response_code": int(res.count() != 0)},cur])

    def getName(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['name']
        old_usr = self.db.Room.find_one({"room_id": room_id})['users']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getName()
        print("error: room ", room_id, " does not exist!")
        return False

    def getSubarea(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['area']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getSubarea()
        print("error: room ", room_id, " does not exist!")
        return False


    def getRoomByOwnID(self, usrid):
        cur = self.db.Room.find({"owner": usrid})
        if cur.count() == 0:
            return dumps({"response_code":0})

        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.User.find_one({"id":room['owner']})
            for i,usr in enumerate(room['users']):
                room['users'][i] = self.db.User.find_one({"id":usr})

        return dumps([{"response_code":1},list(cur)])

    def getRoomByUsrID(self, usrid):
        cur = self.db.Room.find({"users": usrid})
        if cur.count() == 0:
            return dumps({"response_code":0})

        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.User.find_one({"id":room['owner']})
            for i,usr in enumerate(room['users']):
                room['users'][i] = self.db.User.find_one({"id":usr})

        return dumps([{"response_code":1},list(cur)])

    def getRoomBySection(self, sec):
        cur = self.db.Room.find({"area": sec})
        if cur.count() == 0:
            return dumps({"response_code":0})

        cur = list(cur)
        for k,room in enumerate(cur):
            cur[k]['owner'] = self.db.User.find_one({"id":room['owner']})
            for i,usr in enumerate(room['users']):
                room['users'][i] = self.db.User.find_one({"id":usr})
        return dumps([{"response_code":1},list(cur)])

    def getDescription(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['description']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getDescription()
        print("error: room ", room_id, " does not exist!")
        return False

    def getRoom_owner(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['owner']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getRoom_owner()
        print("error: room ", room_id, " does not exist!")
        return False

    def getUsrs(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['users']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getUsrs()
        print("error: room ", room_id, " does not exist!")
        return False

    def getState(self, room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return False
        return res['active']
        if room_id in self.room_id2id:
            return self.rooms[room_id].getState()
        print("error: room ", room_id, " does not exist!")
        return False

    def setName(self, room_id, name):
        res = self.db.Room.update_one({"room_id": room_id},{"name":name})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True

    def setSubarea(self, room_id, subarea):
        res = self.db.Room.update_one({"room_id": room_id}, {"subarea": subarea})
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
        res = self.db.Room.update_one({"room_id": room_id}, {"descriptioin": description})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].setDescription(description)
        print("error: room ", room_id, " does not exist!")
        return False

    def addUsr(self, room_id, usrid):
        old_usr = self.db.Room.find_one({"room_id":room_id})['users']
        res = self.db.Room.update_one({"room_id": room_id}, {"users": old_usr + usrid})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].addUsr(usrid)
        print("error: room ", room_id, " does not exist!")
        return False

    def setRoom_owner(self, room_id, usrid):
        old_usr = self.db.Room.find_one({"room_id": room_id})['owner']
        res = self.db.Room.update_one({"room_id": room_id}, {"owner": usrid})
        if res.matched_count is 0:
            print("error: room ", room_id, " does not exist!")
            return False
        return True
        if room_id in self.room_id2id:
            return self.rooms[room_id].setRoom_owner(usrid)
        print("error: room ", room_id, " does not exist!")
        return False

    def active(self, room_id):
        res = self.db.Room.update_one({"room_id": room_id}, {"active": 1})
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
        res = self.db.Room.update_one({"room_id": room_id}, {"$push": {"messages":entry}})
        if res.matched_count is 0:
            print("error: room ", room_id, " or ", usrid," does not exist!")
            return dumps({"response_code": 0})
        return dumps({"response_code": 1})

    def getMessage(self,room_id):
        res = self.db.Room.find_one({"room_id": room_id})
        if res is None:
            print("error: room ", room_id, " does not exist!")
            return dumps({"response_code":0})
        if len(res['messages']) == 0:
            return dumps({"response_code": 0})
        return dumps([{"response_code": 1},res['messages']])
