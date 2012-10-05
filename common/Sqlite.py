'''
Created on 2012-9-18

@author: jun
'''

import sqlite3
import random
import point
import string

class Sqlite(object):
    
    #def __init__(self):
    
    initDbSql = '''
        CREATE TABLE stocks (date text, trans text, symbol text, qty real, price real);
        CREATE TABLE TranPerSecond(TranName TEXT, Time LONG, Value REAL);
        CREATE TABLE Summary(TranName TEXT, Time LONG, Pass INTEGER, Fail INTEGER);
        CREATE TABLE ResponseTime(TranName TEXT, Time LONG, Value REAL);
        CREATE TABLE SystemResources(ResourcesName TEXT, Time LONG, Value REAL);
        '''
    
    con = None
    cur = None
    
    def initDB(self):
        #self.con = sqlite3.connect(":memory:")
        self.con = sqlite3.connect("d:\example.db")
        self.cur = self.con.cursor()
        self.cur.executescript(self.initDbSql)
        
    def emptyDB(self):
        pass
        
    def connect(self):
        self.con = sqlite3.connect("d:\example.db")
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


class DbPorxy(object):
    
    db = Sqlite()
    
    def __init__(self):
        print 'DbPorxy init,connect db.'
        self.db.connect()
    
    def executeSqlToJson(self,sql):
        points = {}
        for row in self.db.executeSql(sql):
            points[row[1]] = points.get(row[1],point.Point()).setValue(row[2])
        
        tmpList = []
        for key in points.keys():
            tmpList.append('{Time:%s,%s}' % (key,string.join(points.get(key).vlist,',')))
        return '[%s]' % string.join(tmpList,',')







if __name__ == '__main__':
#    sqlite = Sqlite()
#    sqlite.initDB()
#    sqlite.connect()
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.initLargeData(10000,100)
#    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
#    sqlite.cur.execute("SELECT COUNT(*) as 'c' FROM TranPerSecond ORDER BY Value")
#    print sqlite.cur.fetchone()[0]


    db = DbPorxy()
    print db.executeSqlToJson("SELECT * FROM ResponseTime WHERE TranName = 'Reg4' limit 2000")


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
