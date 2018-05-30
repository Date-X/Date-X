# -*- coding: UTF-8 -*-
from usr import Usr_manager
from room_request import Room_request
from room import Room_manager
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import json,yaml,requests

app = Flask(__name__)
mongo = PyMongo(app)

usr_manager = Usr_manager(None)
room_manager = Room_manager(None)

@app.before_request
def initial():
    global usr_manager,room_manager
    db = mongo.db
    usr_manager = Usr_manager(db)
    room_manager = Room_manager(db)

# 获得openid
@app.route('/login', methods=['POST'])
def get_openid():
    data = request.data

    j_data = yaml.safe_load(data)
<<<<<<< HEAD
    
=======

>>>>>>> a73e40fc99e14a6d7bb32c8ac6af8945fbc256ff
    code = j_data['code']
    appid = 'wx88191e14844f68ad'
    secret = 'f8ad952cef6e1266f1f58d107c6eaed4'
    wxurl = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (appid, secret, code)
    response = requests.get(wxurl)
    res = {}
    openid = json.loads(response.text)['openid']
    res['openid'] = openid
    exist = 0
    if usr_manager.getId(openid):
        exist = 1   #用户存在
    res['exist'] = exist
    return jsonify(res)


# 完善信息
@app.route('/usr/complete',methods = ['POST'])
def complete_user():

    data = request.data

    j_data = yaml.safe_load(data)

    usr_id = data['open_id']
    sex = data['sex']
    pre = data['preference']
    res = usr_manager.setPre(usr_id,pre) and usr_manager.setSex(usr_id,sex)
    return json.dumps({'response_code':int(res)})
    # if usr_id in usr_manager.usrid2id:
    #     return str(room_manager.addUsr(room_id, usr_id))
    # return str(False)

# 查看信息
@app.route('/usr/info',methods = ['POST'])
def user_info():

    data = request.data

    j_data = yaml.safe_load(data)

    usr_id = j_data['open_id']
    return usr_manager.getUsrbyusrid(usr_id)

@app.route('/usr/roomlist1',methods = ['POST'])
def room_info1():

    data = request.data

    j_data = yaml.safe_load(data)

    usr_id = j_data['open_id']
    return room_manager.getRoomByID(usr_id)

@app.route('/room/section',methods = ['POST'])
def room_sec():
    data = request.data

    j_data = yaml.safe_load(data)

    sec = j_data['section']
    return room_manager.getRoomBySection(sec)

@app.route('/room/add',methods = ['POST'])
def room_add():

    data = request.data

    j_data = yaml.safe_load(data)

    name = j_data['name']
    subarea = j_data['section']
    description = j_data['description']
    room_owner_id = j_data['room_owner_id']

    room_request = Room_request()
    room_request.setRoomowner(room_owner_id)
    room_request.setName(name)
    room_request.setSubarea(subarea)
    room_request.setDescription(description)

    return room_manager.addRoombyreq(room_request)

@app.route('/room/kick',methods = ['POST'])
def room_kick():
    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    openid = j_data['openid']

    return room_manager.deleteByID(room_id,openid)

@app.route('/room/delete',methods = ['POST'])
def room_delete():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    return room_manager.deleteRoom(room_id)

@app.route('/room/get_message',methods = ['POST'])
def room_get_message():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    return room_manager.getMessage(room_id)

@app.route('/room/send_message',methods = ['POST'])
def room_send_message():

    data = request.data

    j_data = yaml.safe_load(data)

    room_id = j_data['room_id']
    openid = j_data['openid']
    message = j_data['message']
    return room_manager.addMessage(room_id,openid,message)

@app.route('/search',methods = ['POST'])
def room_search():

    data = request.data

    j_data = yaml.safe_load(data)

    if 'room_id' in j_data:
        room_id = j_data['room_id']
        return room_manager.getRoombyroomid(room_id)

    subarea = None
    description = None
    # name = request.form['name']
    if 'section' in j_data:
        subarea = j_data['section']
    if 'description' in j_data:
        description = j_data['description']

    room_request = Room_request()
    if subarea is not None:
        room_request.setSubarea(subarea)
    if description is not None:
        room_request.setDescription(description)
    return room_manager.searchRoom(room_request)

# 不存在的用户会返回False，用于检测用户是否存在
@app.route('/usr/<usrid>')
def check_usr_exists(usrid):
    return str(usrid in usr_manager.usrid2id)


# 注册成功返回True，错误返回False
@app.route('/signup', methods=['POST'])
def sgin_up():

    db = mongo.db
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
    db = mongo.db
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

            return str(room_manager.addRoombyreq(room_request,db))


# 不存在的房间会返回False，用于检测房间是否存在
@app.route('/room/<room_id>')
def check_room_exist(room_id):
    return str(room_id in room_manager.room_id2id)

# GET:返回对应房间号的对应属性，房间号不存在返回False
# POST:修改对应房间号的对应属性（包括房间名、分区、描述、房间主人）
@app.route('/room/<room_id>/<profile>', methods=['GET', 'POST'])
def show_room_profile(room_id, profile):
    if request.method == 'GET':
        # if profile == 'id':
        #     return str(room_manager.getId(room_id))
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
    app.run(host='0.0.0.0',debug=True)
