"""
ｄｉｃｔ 所有数据库交互
提供数据库连接，以及功能交互
"""
import  pymysql
import hashlib

#加密专用盐
salt =b'*#06#'

#加密处理函数
def encryption(passwd):
    hash = hashlib.md5(salt)
    hash.update(passwd.encode())
    return hash.hexdigest()

class Database:
    def __init__(self):
        self.db = pymysql.connect(host = 'localhost',
                                  port = 3306,
                                  password = '123456',
                                  database = 'dict',
                                  charset = 'utf8')
        self.cur = self.db.cursor()
    def close(self):
        self.cur.close()
        self.db.close()
    #注册
    def register(self,name,passwd):
        sql = "select * from user where name = '%s'"%name
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return  False
        passwd =encryption(passwd)
        try:
            sql = "insert into user(name,passwd)values (%s,%s)"
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return  True
        except:
            self.db.rollback()
            return  False
    #登录
    def login(self,name,passwd):
        passwd =encryption(passwd)
        sql = "select * from user where name ='%s'and passwd = '%s'"%(name,passwd)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return  True
        else:
            return False
    #查单词
    def query(self,word):
        sql = "select mean from words where word = '%s'"%word
        self.cur.execute(sql)
        r = self.cur.fetchone()
        if r:
            return r[0]

    #插入记录
    def insert_history(self,name,word):
        sql = "insert into hist(name,word)values(%s,%s)"
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except:
            self.db.rollback()
    #历史记录
    def history(self,name):
        sql = "select name.word,time from hist where name='%s' order by time desc limit 10"%name
        self.cur.execute(sql)
        return self.cur.fetchall()



