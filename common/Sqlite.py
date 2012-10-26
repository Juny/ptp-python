'''
@author: jun
'''

import sqlite3
import random
import string
import os

class Sqlite(object):
    
    #def __init__(self):
    
    initDbSql = '''
        CREATE TABLE TranPerSecond(Time LONG, TranName TEXT, Value REAL);
        CREATE TABLE ResponseTime(Time LONG, TranName TEXT, Value REAL);
        CREATE TABLE Summary(Time LONG, TranName TEXT, Pass INTEGER, Fail INTEGER);
        CREATE TABLE SystemResources(Time LONG, ResourcesName TEXT, Value REAL);
        '''
        #CREATE TABLE Trans(Time LONG, TranName TEXT, Duration REAL, Status INTEGER);
            
    con = None
    cur = None
    
    """
    初始化数据库，创建相关的表
    """
    def initDB(self,path):
        #self.con = sqlite3.connect(":memory:")
        self.con = sqlite3.connect(path, check_same_thread = False)
        self.cur = self.con.cursor()
        self.cur.executescript(self.initDbSql)
        
    def emptyDB(self,path):
        pass
        
    def connect(self,path):
        if os.path.exists(path) == False:
            self.initDB(path)
            return
        self.con = sqlite3.connect(path, check_same_thread = False)
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
                self.cur.execute("INSERT INTO Trans VALUES (%s,'%s',%2.2f,%d)" % ("strftime('%s','now')","Reg1",random.uniform(0,1),0))
                self.cur.execute("INSERT INTO Trans VALUES (%s,'%s',%2.2f,%d)" % ("strftime('%s','now')","Reg2",random.uniform(0,10),0))
                self.cur.execute("INSERT INTO Trans VALUES (%s,'%s',%2.2f,%d)" % ("strftime('%s','now')","Reg3",random.uniform(0,100),0))
                self.cur.execute("INSERT INTO Trans VALUES (%s,'%s',%2.2f,%d)" % ("strftime('%s','now')","Reg4",random.uniform(0,50),0))
                self.cur.execute("INSERT INTO Trans VALUES (%s,'%s',%2.2f,%d)" % ("strftime('%s','now')","Reg5",random.uniform(0,200),0))
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
    def getResponseTimeWithJson(self, tran_name, limit, min_time=0, max_time=0):
        sql = None
        if min_time == max_time and max_time == 0:
            sql = "select datetime(Time,'unixepoch'),Duration from Trans where TranName = '%s' limit %s" % (tran_name, limit)
        else:
            sql = "select datetime(Time,'unixepoch'),Duration from Trans where TranName = '%s' and Time >= %s and Time <= %s limit %s" % (tran_name, min_time, max_time, limit)
        
        tmpList = []
        for row in self.executeSql(sql):
            tmpList.append("{Time:'%s',Value:%s}" % (row[0], row[1]))   
        return '[%s]' % string.join(tmpList,',')
    
    """
    [{Time:0,Value:0.8},{Time:1,Value:0.98}]
    """
    def getTranPerSecondWithJson(self, tran_name, limit, min_time=0, max_time=0):
        sql = None
        if min_time == max_time and max_time == 0:
            sql = "select datetime(Time,'unixepoch'),Value from TranPerSecond where TranName = '%s' limit %s" % (tran_name, limit)
        else:
            sql = "select datetime(Time,'unixepoch'),Value from TranPerSecond where TranName = '%s' and Time >= %s and Time <= %s limit %s" % (tran_name, min_time, max_time, limit)
        
        tmpList = []
        for row in self.executeSql(sql):
            tmpList.append("{Time:'%s',Value:%s}" % (row[0], row[1]))   
        return '[%s]' % string.join(tmpList,',')

    """
    [{TranName:0,Max:0.8,Avg:0.8},{TranName:0,Max:0.8,Avg:0.8}]
    """        
    def getTranTpsSummary(self):
#        if summary_type == 'tps':
        tableName = 'TranPerSecond'
#        else:
#            tableName = 'ResponseTime'
            
        transName = []
        sql = 'select distinct TranName from %s'%tableName
        for row in self.executeSql(sql):
            transName.append(row[0])
        print transName
        
        summary = []
        for tran in transName:
            sql = "select TranName,max(Value),min(Value),avg(Value),0 from %s where TranName = '%s'"%(tableName,tran)
            row = self.executeSql(sql).fetchone()
            print row
            summary.append("{TranName:'%s',Max:%s,Min:%s,Avg:%s,Last:%s}"%row)
        print summary
        return '[%s]' % string.join(summary,',')

    def getTranRpsSummary(self,summary_type):
        transName = []
        sql = 'select distinct TranName from Trans'
        for row in self.executeSql(sql):
            transName.append(row[0])
        print transName
        
        summary = []
        for tran in transName:
            sql = "select TranName,max(Duration),min(Duration),avg(Duration),0 from Trans where TranName = '%s'"%(tran)
            row = self.executeSql(sql).fetchone()
            print row
            summary.append("{TranName:'%s',Max:%s,Min:%s,Avg:%s,Last:%s}"%row)
        print summary
        return '[%s]' % string.join(summary,',')
            
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
#    db = DbPorxy.getInstance("d:\TestByGJY.db")
#    for row in db.executeSql("select time(),date(),strftime('%Y-%M-%d %H:%m:%f'),datetime('now','localtime'),datetime(1349677432,'unixepoch'),strftime('%s','now')"):
#        print row
#    for row in db.executeSql('select count(*) from Trans'):
#        print row  
#    for row in db.executeSql('select count(*) from TranPerSecond'):
#        print row  
#    for row in db.executeSql("select TranName,max(Value),min(Value),avg(Value),0 from %s where TranName = '%s'"%('TranPerSecond','Test1')):
#        print row
#    for row in db.executeSql('select * from TranPerSecond limit 10'):
#        print row
#    for row in db.executeSql('select * from ResponseTime'):
#        print row        
#    for row in db.executeSql("select avg(Value),max(Value) from TranPerSecond where TranName = 'Test1'"):
#        print row    


#    import time
#    sqlite = Sqlite()
#    sqlite.connect("d:\Test100W.db")
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.initLargeData(1000000,200)
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.cur.execute("SELECT COUNT(*) as 'c' FROM Trans")
#    print sqlite.cur.fetchone()[0]

 
    import time
    db = DbPorxy.getInstance("d:\Test100W.db")
##    for row in db.executeSql("create index Index_Trans_Time on Trans(Time);"):
##        print row
##    for row in db.executeSql("create index Index_Trans_Time_TranName on Trans(Time,TranName);"):
##        print row
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    for row in db.executeSql("select TranName,max(Duration),min(Duration),avg(Duration),0 from Trans where TranName = 'Reg1'"):
#        print row
    for row in db.executeSql("select * from Trans order by Time asc limit 2"):
        print row
    for row in db.executeSql("select * from Trans order by Time desc limit 2"):
        print row
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

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

#----------------------500W数据----------------------
#"d:\Test100W.db"  500W数据
#2012-10-15 16:40:34
#5000000
#2012-10-15 16:42:52

#没索引
#2012-10-15 16:48:30
#"select TranName,max(Duration),min(Duration),avg(Duration),0 from Trans where TranName = 'Reg1'"
#2012-10-15 16:48:32



