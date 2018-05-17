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
    return usrid in usr_manager.usrs


# 注册成功返回True，错误返回False
@app.route('/sginup', methods=['POST'])
def sgin_up():
    if request.method == 'POST':
        usrid = request.form['usrid']
        password = request.form['password']
        return usr_manager.addUsr(usrid, password)


# 登陆成功返回True，错误返回False
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        usrid = request.form['usrid']
        password = request.form['password']
        return usr_manager.checkPassword(usrid, password)


# GET:不存在的用户返回false，存在返回用户偏好
# POST:修改用户偏好，成功返回True，失败返回False
@app.route('/usr/<usrid>/preference', methods=['GET', 'POST'])
def show_usr_preference(usrid):
    if request.method == 'GET':
        return usr_manager.getPre(usrid)
    if request.method == 'POST':
        pre = request.form['preference']
        return usr_manager.setPre(usrid, pre)


# 成功返回房间id，失败返回False
@app.route('/create', methods = ['POST'])
def create_room():
    if request.method == 'POST':
        room_owner_id = request.form['usrid']
        name = request.form['name']     #room name
        subarea = request.form['subarea']
        description = request.form['description']

        if room_owner_id in usr_manager.usrs:
            room_request = Room_request()
            room_request.setRoomowner(room_owner_id)
            room_request.setName(name)
            room_request.setSubarea(subarea)
            room_request.setDescription(description)

            return room_manager.addRoombyreq(room_request)


# 不存在的房间会返回False，用于检测房间是否存在
@app.route('room/<room_id>')
def check_room_exist(room_id):
    return room_id in room_manager.room_id2id


@app.route('room/<room_id>/<profile>', methods=['GET', 'POST'])
def show_room_profile(room_id, profile):
    if request.method == 'GET':
        if profile == 'id':
            return room_manager.getId(room_id)
        if profile == 'name':
            return room_manager.getName(room_id)
        if profile == 'subarea':
            return room_manager.getSubarea(room_id)
        if profile == 'description':
            return room_manager.getDescription(room_id)
        if profile == 'room_owner_id':
            return room_manager.getRoom_owner(room_id)
        if profile == 'usrs_id':
            return room_manager.getUsrs(room_id)
        if profile == 'state':
            return room_manager.getState(room_id)
            
    if request.method == 'POST':
        room_owner_id = request.form['usrid']
        name = request.form['name']     #room name
        subarea = request.form['subarea']
        description = request.form['description']

        if profile == 'name':
            return room_manager.setName(room_id,name)
        if profile == 'subarea':
            return room_manager.setSubarea(room_id,subarea)
        if profile == 'description':
            return room_manager.getDescription(room_id)
        if profile == 'room_owner_id':
            return room_manager.getRoom_owner(room_id)
        if profile == 'usrs_id':
            return room_manager.getUsrs(room_id)
        if profile == 'state':
            return room_manager.getState(room_id)

