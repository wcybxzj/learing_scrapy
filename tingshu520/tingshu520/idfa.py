# -*- coding: utf-8 -*-  
  
import time
import MySQLdb
import pprint 
import traceback 
class DB:
  def __init__(self, host, port, user, passwd, db):
    self.conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db) 
    self.cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
    #self.cur = self.conn.cursor()
    self.conn.set_character_set('utf8')
    self.cur.execute("SET NAMES utf8")
    self.cur.execute("SET CHARACTER SET utf8")
    self.cur.execute("SET character_set_connection=utf8")
  
  def __delete__(self):
    self.conn.close()
    
  def query(self, sql, params):
    self.cur.execute(sql, params)
    return self.cur.fetchall()
    
  def execute(self, sql, params):
    try:
      rows = self.cur.execute(sql, params)
      if(rows>0):
        self.conn.commit()    
        pass
      return rows
    except Exception, e:
      print dir(e)
      pass
      
  def executeMany(self, sql, params):
    try:
      rows = self.cur.executemany(sql, params)
      if(rows>0):
        self.conn.commit()    
        pass
      return rows
    except Exception, e:
      print dir(e)
      pass
  
  def insert(self, sql, params):
    try:
      rows = self.cur.execute(sql, params)
      if(rows>0):
        id = self.cur.lastrowid
        self.conn.commit()    
        pass
      return id
    except Exception, e:
      print dir(e)
      pass  

class Idfa:
    def __init__(self):
        self.db = DB("hide", 3377, "reborn", "newlife", "test")
    def createTable(self, t_name):
        sql = """CREATE TABLE if not exits `%s_suc` (
                  `id` int(11) NOT NULL ,
                  `udid` varchar(50) DEFAULT NULL COMMENT '苹果老用户唯一标识',
                  `mac` varbinary(100) DEFAULT NULL COMMENT '设标MAC地址',
                  `asid` varchar(50) DEFAULT NULL,
                  `addtime` datetime DEFAULT NULL COMMENT '添加时间',
                  `ip` varchar(20) DEFAULT '' COMMENT 'ip',
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""%(t_name)
        params = ()
        res = self.db.execute(sql, params) 
        return res

    def checkMobile(self, type, item):
        if(not item[type]):
            return False
        sql = "select asid, udid, mac, addtime from client.mobile_new where "+type+" = %s and addtime > %s and addtime < date_add(%s, interval 3 day) limit 1"
        params = (item[type], item["addtime"], item["addtime"])
        res = self.db.query(sql, params) 
        return res
        
    def checkSuc(self, type, t_name, value):    
        sql = "select asid, udid, mac, addtime, ip from " + t_name + "_suc where " + type + " = %s limit 1"
        params = (value)
        res = self.db.query(sql, params) 
        return res

    def insertSuc(self, t_name, item):
        sql = "insert into " + t_name + "_suc(id, asid, udid, mac, addtime, ip) values (%s, %s, %s, %s, %s, %s)"
        params = (item["id"], item["asid"], item["udid"], item["mac"], item["addtime"], item["ip"])
        res = self.db.insert(sql, params) 
        return res
        
    def getList(self, t_name, page=0, per=3000):
        sql = "select id, asid, udid, mac, addtime, ip from " + t_name + " limit %s, %s"
        params = (page*per, per)
        res = self.db.query(sql, params) 
        return res

    def dealOne(self, t_name):
        for page in range(100):
          print t_name, page
          ret = self.getList(t_name, page)
          for item in ret:
              for type in ["asid", "udid", "mac"]:
                  if self.checkMobile(type, item):
                      if not self.checkSuc(type, t_name, item[type]):
                          self.insertSuc(t_name, item)                  
      
if '__main__' == __name__:
    list = [
        {"t_name" :"tmp_jie"  },
        {"t_name" :"tmp_bizhi"    },
        {"t_name" :"tmp_jie_hd" },
        {"t_name" :"tmp_koushu" },
        {"t_name" :"tmp_mimi"   },
        {"t_name" :"tmp_mimi_hd"},
    ]
    idfa = Idfa()
    for item in list:
        t_name = item["t_name"]
        idfa.dealOne(t_name)
    
