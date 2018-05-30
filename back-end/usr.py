# -*- coding: UTF-8 -*-

from preference import available_pre
import json
from bson.json_util import dumps
'''
ver 1.1
连接MongoDB 完成

ver 1.0
功能：
1.用户信息包含id、密码、偏好
2.增加用户
3.修改密码
4.修改偏好
5.根据用户id查询用户
6.用户登陆

需要添加功能：
1.更多的用户信息（例如认证信息）
2.用户拥有的房间
'''
class Usr_manager(object):
    def __init__(self, db):
        self.db = db
        self.usrs = []
        self.next_id = 0
        self.usrid2id = {}  # 这里后一个id指在usrs这个list中的第几个

    def getUsrbyusrid(self, usrid):
        res = self.db.User.find_one({'id': usrid})
        if res is not None:
            return dumps([{'response_code':1},res])
        print("error: usr id ", usrid, " does not exist!")
        return dumps({'response_code':0})

    def addUsr(self, id, sex, pre):
        # if id in self.usrid2id:
        #     print("error: usr id ", id, " already exists!")
        #     return False
        # self.usrs.append(Usr(id, password))
        user = self.db.User

        self.usrid2id = user.insert_one({"id":id, "sex":sex, "pre":pre}).inserted_id
        # self.usrid2id[id] = self.next_id
        # self.next_id += 1
        # print(user.insert_one({"id":id, "password":password}).inserted_id)
        return True

    #下面这些函数是对usr对应函数的封装，使得所有操作都在usr manager中进行
    def getId(self, usrid):
        res = self.db.User.find_one({'id':usrid})
        if res is not None:
            return res['id']
        # print("error: usr", usrid, "does not exist!")
        return False

    def getPre(self, usrid):
        res = self.db.User.find_one({'id': usrid})
        if res is not None:
            return res['pre']
        print("error: usr", usrid, "does not exist!")
        return False
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].getPre()
        print("error: usr", usrid, "does not exist!")
        return False

    def resetPassword(self, usrid, old_password, new_password):
        res = self.db.User.find_one({'id': usrid})['password']
        if res is None:
            print("error: usr", usrid, "does not exist!")
            return False
        self.db.User.update({'id': usrid},{"$set":{'password':new_password}})
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].resetPassword(old_password, new_password)
        print("error: usr", usrid, "does not exist!")
        return False

    def addPre(self, usrid, new_pre):
        res = self.db.User.find_one({'id': usrid})['pre']
        if res is None:
            print("error: usr", usrid, "does not exist!")
            return False
        self.db.User.update({'id': usrid}, {"$set": {'pre': res + new_pre}})
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].addPre(new_pre)
        print("error: usr", usrid, "does not exist!")
        return False

    def setPre(self, usrid, preferences):
        res = self.db.User.find_one({'id': usrid})['pre']
        if res is None:
            print("error: usr", usrid, "does not exist!")
            return False
        self.db.User.update({'id': usrid}, {"$set": {'pre': preferences}})
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].setPre(preferences)
        print("error: usr", usrid, "does not exist!")
        return False

    def setSex(self, usrid, sex):
        res = self.db.User.find_one({'id': usrid})['sex']
        if res is None:
            print("error: usr", usrid, "does not exist!")
            return False
        self.db.User.update({'id': usrid}, {"$set": {'sex': sex}})
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].setPre(preferences)
        print("error: usr", usrid, "does not exist!")
        return False

    def deletePre(self, usrid, del_pre):
        res = self.db.User.find_one({'id': usrid})['pre']
        if res is None:
            print("error: usr", usrid, "does not exist!")
            return False
        if del_pre not in res:
            print("error: pre", del_pre, "does not exist!")
            return False
        self.db.User.update({'id': usrid}, {"$set": {'pre': res.remove(del_pre)}})
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].deletePre(del_pre)
        print("error: usr", usrid, "does not exist!")
        return False

    def checkPassword(self, usrid, password):
        return True
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].checkPassword(password)
        print("error: usr", usrid, "does not exist!")
        return False



if __name__ == "__main__":
    '''
    # test add usr
    usr_manager = Usr_manager()
    usr_manager.addUsr(7, 123)
    usr_manager.addUsr(9, 123)
    usr_manager.addUsr(9, 123)
    usr_manager.addUsr(3, 123)
    usr_manager.printUsrs()

    # test getUsrbyusrid
    usr1 = usr_manager.getUsrbyusrid(1)
    usr2 = usr_manager.getUsrbyusrid(3)
    usr2.printUsr()
    usr3 = usr_manager.getUsrbyusrid(7)
    usr3.printUsr()

    # test preference
    '''
