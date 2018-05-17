# -*- coding: UTF-8 -*-
from usr import Usr_manager
from room_request import Room_request
from room import Room_manager
from flask import Flask, request

usr_manager = Usr_manager()
room_manager = Room_manager()

app = Flask(__name__)


# 不存在的用户会返回False，用于检测用户是否存在
@app.route('/usr/<usrid>')
def check_usr_exists(usrid):
    return str(usrid in usr_manager.usrid2id)


# 注册成功返回True，错误返回False
@app.route('/sginup', methods=['POST'])
def sgin_up():
    if request.method == 'POST':
        usrid = request.form['usrid']
        password = request.form['password']
        return str(usr_manager.addUsr(usrid, password))


# 登陆成功返回True，错误返回False
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usrid = request.form['usrid']
        password = request.form['password']
        return str(usr_manager.checkPassword(usrid, password))


# GET:不存在的用户返回false，存在返回用户偏好
# POST:修改用户偏好，成功返回True，失败返回False
@app.route('/usr/<usrid>/preference', methods=['GET', 'POST'])
def show_usr_preference(usrid):
    if request.method == 'GET':
        return str(usr_manager.getPre(usrid))
    if request.method == 'POST':
        pre = request.form['preference']
        return str(usr_manager.setPre(usrid, pre))


# 成功返回房间id，失败返回False
@app.route('/create', methods = ['POST'])
def create_room():
    if request.method == 'POST':
        room_owner_id = request.form['usrid']
        name = request.form['name']     #room name
        subarea = request.form['subarea']
        description = request.form['description']

        if room_owner_id in usr_manager.usrid2id:
            room_request = Room_request()
            room_request.setRoomowner(room_owner_id)
            room_request.setName(name)
            room_request.setSubarea(subarea)
            room_request.setDescription(description)

            return str(room_manager.addRoombyreq(room_request))


# 不存在的房间会返回False，用于检测房间是否存在
@app.route('/room/<room_id>')
def check_room_exist(room_id):
    return str(room_id in room_manager.room_id2id)

# GET:返回对应房间号的对应属性，房间号不存在返回False
# POST:修改对应房间号的对应属性（包括房间名、分区、描述、房间主人）
@app.route('/room/<room_id>/<profile>', methods=['GET', 'POST'])
def show_room_profile(room_id, profile):
    if request.method == 'GET':
        if profile == 'id':
            return str(room_manager.getId(room_id))
        if profile == 'name':
            return str(room_manager.getName(room_id))
        if profile == 'subarea':
            return str(room_manager.getSubarea(room_id))
        if profile == 'description':
            return str(room_manager.getDescription(room_id))
        if profile == 'room_owner_id':
            return str(room_manager.getRoom_owner(room_id))
        if profile == 'usrs_id':
            return str(room_manager.getUsrs(room_id))
        if profile == 'state':
            return str(room_manager.getState(room_id))
            
    if request.method == 'POST':
        room_owner_id = request.form['usrid']
        name = request.form['name']     #room name
        subarea = request.form['subarea']
        description = request.form['description']

        if name:
            return str(room_manager.setName(room_id,name))
        if subarea:
            return str(room_manager.setSubarea(room_id,subarea))
        if description:
            return str(room_manager.setDescription(room_id, description))
        if room_owner_id:
            return str(room_manager.setRoom_owner(room_id, room_owner_id))


# 向对应房间添加用户
@app.route('/room/<room_id>/add',methods = ['POST'])
def add_usr_to_room(room_id):
    usr_id = request.form['usrid']
    if usr_id in usr_manager.usrid2id:
        return str(room_manager.addUsr(room_id, usr_id))
    return str(False)

@app.route('/print', methods = ['GET'])
def myprint():
    usr_manager.printUsrs()
    room_manager.printRooms()
    return str(True)
    

if __name__ == "__main__":
    app.run()