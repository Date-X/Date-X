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

    usr_id = j_data['open_id']
    sex = j_data['sex']
    pre = j_data['preference']
    avatar = j_data['avatar']
    db = mongo.db
    res = db.User.find_one({'id': usr_id})
    if res is not None:
        res = usr_manager.setPre(usr_id,pre) and usr_manager.setSex(usr_id,sex) and usr_manager.setAvatar(usr_id,avatar)
    else:
        res = usr_manager.addUsr(usr_id,sex,pre,avatar)
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
    return room_manager.getRoomByOwnID(usr_id)

@app.route('/usr/roomlist2',methods = ['POST'])
def room_info2():

    data = request.data

    j_data = yaml.safe_load(data)

    usr_id = j_data['open_id']
    return room_manager.getRoomByUsrID(usr_id)

@app.route('/usr/join',methods = ['POST'])
def room_join():
    data = request.data

    j_data = yaml.safe_load(data)

    usr_id = j_data['open_id']
    room_id = j_data['room_id']
    return room_manager.joinRoom(usr_id,room_id)

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
    openid = j_data['open_id']

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
    openid = j_data['open_id']
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

@app.route('/print', methods = ['GET'])
def myprint():
    usr_manager.printUsrs()
    room_manager.printRooms()
    return str(True)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
