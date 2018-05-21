# -*- coding: UTF-8 -*-

from preference import available_pre

'''
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

class Usr(object):
    def __init__(self, id, password):
        self.id = id  # usr's unique id, maybe given by wechat
        self.password = password
        self.preferences = []

    def getId(self):
        return self.id

    def getPassword(self):
        return self.password

    def getPre(self):
        return self.preferences

    def resetPassword(self, old_password, new_password):
        if old_password == self.password:
            self.password = new_password
            return True
        else:
            print("error: can not reset password, password is wrong!")
            return False

    # 检查偏向是否合法
    @staticmethod
    def checkPre(preference):
        if preference in available_pre:
            return True
        print("error: ", preference, " is not available!")
        return False

    def addPre(self, new_pre):
        if self.checkPre(new_pre):
            if new_pre not in self.preferences:
                self.preferences.append(new_pre)
                return True
            print("error: preference ", new_pre, " already exists!")
        print("error: can not add preference ", new_pre)
        return False

    def setPre(self, preferences):
        for preference in preferences:
            if not self.checkPre(preference):
                print("error: set preference failed!")
                return False
        self.preferences = preferences
        return True

    def deletePre(self, del_pre):
        if del_pre in self.preferences:
            self.preferences.remove(del_pre)
            return True
        print("error: delete preference failed!")
        return False
    
    def checkPassword(self, password):
        if password == self.password :
            return True
        return False

    def printUsr(self):
        print("id:", self.getId())
        print("password:", self.getPassword())
        print("preference:", self.getPre())


class Usr_manager(object):
    def __init__(self, db):
        self.db = db
        self.usrs = []
        self.next_id = 0
        self.usrid2id = {}  # 这里后一个id指在usrs这个list中的第几个

    def getNext_id(self):
        return self.next_id

    def getUsrs(self):
        return self.usrs

    def getUsrid2id(self):
        return self.usrid2id

    def getUsrbyusrid(self, usrid):
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]]
        print("error: usr id ", usrid, " does not exist!")
        return None

    def addUsr(self, id, password):
        if id in self.usrid2id:
            print("error: usr id ", id, " already exists!")
            return False
        self.usrs.append(Usr(id, password))
        user = self.db.User
        self.usrid2id = user.insert_one({"id":id, "password":password, "pre":[]}).inserted_id
        # self.usrid2id[id] = self.next_id
        # self.next_id += 1
        # print(user.insert_one({"id":id, "password":password}).inserted_id)
        return True

    def printUsrs(self):
        count = 0
        cursor = self.db.User.find({})
        for usr in cursor:
            # usr = Usr(usr_item['id'], usr_item['password'])
            # for usr in self.usrs:
            print("===================Usr ", usr["_id"], "===================")
            print("id:", usr['id'])
            print("password:", usr['password'])
            print("preference:", usr['pre'])
            # count += 1

    #下面这些函数是对usr对应函数的封装，使得所有操作都在usr manager中进行
    def getId(self, usrid):
        res = self.db.User.find({'id':usrid})['id']
        if res is not None:
            return res
        print("error: usr", usrid, "does not exist!")
        return False
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].getId()
        print("error: usr", usrid, "does not exist!")
        return False

    def getPassword(self, usrid):
        res = self.db.User.find({'id': usrid})['password']
        if res is not None:
            return res
        print("error: usr", usrid, "does not exist!")
        return False
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].getPassword()
        print("error: usr", usrid, "does not exist!")
        return False

    def getPre(self, usrid):
        res = self.db.User.find({'id': usrid})['pre']
        if res is not None:
            return res
        print("error: usr", usrid, "does not exist!")
        return False
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].getPre()
        print("error: usr", usrid, "does not exist!")
        return False

    def resetPassword(self, usrid, old_password, new_password):
        res = self.db.User.find({'id': usrid})['password']
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
        res = self.db.User.find({'id': usrid})['pre']
        if res is not None:
            return res
        print("error: usr", usrid, "does not exist!")
        return False
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].addPre(new_pre)
        print("error: usr", usrid, "does not exist!")
        return False

    def setPre(self, usrid, preferences):
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].setPre(preferences)
        print("error: usr", usrid, "does not exist!")
        return False

    def deletePre(self, usrid, del_pre):
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].deletePre(del_pre)
        print("error: usr", usrid, "does not exist!")
        return False
    
    def checkPassword(self, usrid, password):
        if usrid in self.usrid2id:
            return self.usrs[self.usrid2id[usrid]].checkPassword(password)
        print("error: usr", usrid, "does not exist!")
        return False



if __name__ == "__main__":
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
