'''
Created on 2012-9-18

@author: jun
'''

import sqlite3
import random
import string
import os

class Sqlite(object):
    
    #def __init__(self):
    
    initDbSql = '''
        CREATE TABLE TranPerSecond(TranName TEXT, Time LONG, Value REAL);
        CREATE TABLE Summary(TranName TEXT, Time LONG, Pass INTEGER, Fail INTEGER);
        CREATE TABLE ResponseTime(TranName TEXT, Time LONG, Value REAL);
        CREATE TABLE SystemResources(ResourcesName TEXT, Time LONG, Value REAL);
        '''
    
    con = None
    cur = None
    
    """
    初始化数据库，创建相关的表
    """
    def initDB(self,path):
        #self.con = sqlite3.connect(":memory:")
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.executescript(self.initDbSql)
        
    def emptyDB(self,path):
        pass
        
    def connect(self,path):
        if os.path.exists(path) == False:
            self.initDB(path)
            return
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
    
    def initTestData(self):
        tps = [('reg1', '100500', 45.00),
               ('reg2', '100501', 45.00),
               ('reg3', '100502', 45.00),
               ('reg4', '100503', 45.00),
               ('reg5', '100504', 45.00)]
        self.cur.executemany('INSERT INTO TranPerSecond VALUES (?,?,?)', tps)
        
    def initLargeData(self,rowsCount,batchCount):
        time = 0
        rows = 0
        batch = batchCount
        while rows < rowsCount:
            while batch > 0:
                #r = random.uniform(0,100)
                #self.cur.execute("INSERT INTO TranPerSecond VALUES ('reg1','100',100.0)")
                #self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%f)" % (random.choice(["Reg1", "Reg2", "Reg3", "Reg4", "Reg5"]),time,r))
                self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%2.2f)" % ("Reg1",time,random.uniform(0,1)))
                self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%2.2f)" % ("Reg2",time,random.uniform(0,10)))
                self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%2.2f)" % ("Reg3",time,random.uniform(0,100)))
                self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%2.2f)" % ("Reg4",time,random.uniform(0,50)))
                self.cur.execute("INSERT INTO ResponseTime VALUES ('%s',%d,%2.2f)" % ("Reg5",time,random.uniform(0,200)))
                time+=1
                batch-=1
            self.con.commit()
            batch = batchCount
            rows+=batchCount

    def executeSql(self,sql):
        return self.cur.execute(sql)

    def executeSqlBatch(self,sqlList):
        for sql in sqlList:
            self.cur.execute(sql)
        self.con.commit()   

class Point():
    pass

class DbPorxy(object):
    
    db = Sqlite()
    instance = None
    path = None
    
    def __init__(self,path):
        print 'DbPorxy init,connect db.', path
        DbPorxy.path = path
        self.db.connect(path)
        
    def executeSql(self,sql):
        return self.db.executeSql(sql)
    
    def executeSqlBatch(self,sqlList):
        self.db.executeSqlBatch(sqlList)
    
    """
    [{Time:0,Value:0.8},{Time:1,Value:0.98}]
    """
    def getResponseTimeToJson(self, tran_name, limit, min_time=0, max_time=0):
        sql = None
        if min_time == max_time and max_time == 0:
            sql = "select Time,Value from ResponseTime where TranName = '%s' limit %s" % (tran_name, limit)
        else:
            sql = "select Time,Value from ResponseTime where TranName = '%s' and Time >= %s and Time <= %s limit %s" % (tran_name, min_time, max_time, limit)
        
        tmpList = []
        for row in self.executeSql(sql):
            tmpList.append('{Time:%s,Value:%s}' % (row[0], row[1]))   
        return '[%s]' % string.join(tmpList,',')
    
    """
    [{Time:0,Value:0.8},{Time:1,Value:0.98}]
    """
    def getTranPerSecondToJson(self, tran_name, limit, min_time=0, max_time=0):
        sql = None
        if min_time == max_time and max_time == 0:
            sql = "select Time,Value from TranPerSecond where TranName = '%s' limit %s" % (tran_name, limit)
        else:
            sql = "select Time,Value from TranPerSecond where TranName = '%s' and Time >= %s and Time <= %s limit %s" % (tran_name, min_time, max_time, limit)
        
        tmpList = []
        for row in self.executeSql(sql):
            tmpList.append('{Time:%s,Value:%s}' % (row[0], row[1]))   
        return '[%s]' % string.join(tmpList,',')
        
    @staticmethod
    def getInstance(path):
        if DbPorxy.instance != None and DbPorxy.path != path:
            print  DbPorxy.path,path
            raise Exception('DbPorxy.path != path')
        if DbPorxy.instance == None:
            DbPorxy.instance = DbPorxy(path)
        print 'getInstance:',path
        return DbPorxy.instance


if __name__ == '__main__':
    db = DbPorxy.getInstance("d:\example.db")
    db = DbPorxy.getInstance("d:\example.db")
    for row in db.executeSqlToJson('select * from ResponseTime limit 10'):
        print row
    print db.getResponseTimeToJson('Reg1',100)
#    sqlite = Sqlite()
#    sqlite.initDB()
#    sqlite.connect()
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.initLargeData(10000,100)
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.cur.execute("SELECT COUNT(*) as 'c' FROM TranPerSecond ORDER BY Value")
#    print sqlite.cur.fetchone()[0]


#    db = DbPorxy()
#    print db.executeSqlToJson("SELECT * FROM ResponseTime WHERE TranName = 'Reg4' limit 2000")


#    points = {}
#    tName = ['Reg1','Reg2','Reg3','Reg4','Reg5']
#    index = 0
#    for t in tName:
#        print t
#        for row in sqlite.cur.execute("SELECT * FROM ResponseTime WHERE TranName = '%s' limit 2" % (t)):
#            print row
#            #print '{Time:%d,Value:%3.3f}'%(row[1],row[2])
#            points[row[1]] = points.get(row[1],point.Point()).setValue(row[2])
#        index+=1
#        
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#
#    tmpList = []    
#    for key in points.keys():
#        tmpList.append('{Time:%s,%s}' % (key,string.join(points.get(key).vlist,',')))
#    print '[%s]' % string.join(tmpList,',')








#:memory:
#2012-09-18 23:44:59
#10000000
#2012-09-18 23:45:34

#"d:\example.db"
#batch 100
#2012-09-18 23:51:38
#100000
#2012-09-18 23:51:56

#"d:\example.db"
#batch 1000
#2012-09-18 23:54:29
#100000
#2012-09-18 23:54:31
