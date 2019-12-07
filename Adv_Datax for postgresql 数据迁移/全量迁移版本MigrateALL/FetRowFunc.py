import psycopg2
import queue
import threading
from migrateconfigure import sourcedbname,sourcehost,sourcepassword,sourceport,sourceuser,InsertMaxThread,ResultCount
from InsertFun import StartInsert
'''  

获取数据的功能，这里使用了线程模型。其实也可以使用进程模式。但是抽取的过程只能使用单一的形式，否则的话没法保证事务唯一。
所以就成了，单进（线）程获取，多线程插入的模式。

'''
class MulitThreadInsert(threading.Thread):
    def __init__(self, result,migratequeue,tablename,threadid,tupledesc):
        threading.Thread.__init__(self)
        self.migratequeue = migratequeue
        self.result=result
        self.tablename=tablename
        self.tupledesc=tupledesc
        self.threadid=threadid
    def run(self):
        try:
            print('表名称%s  第%s号线程' %(self.tablename,self.threadid))
            StartInsert(self.result,self.tablename,self.threadid,self.tupledesc)
        except Exception as e:
            print(e)
        finally:
            self.migratequeue.get()
            self.migratequeue.task_done()
def FetchResultFromSource(tablename,GetDataSql):
    conn=psycopg2.connect(dbname=sourcedbname, user=sourceuser,password=sourcepassword, host=sourcehost, port=sourceport)
    cur=conn.cursor(name=tablename,cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(GetDataSql)
    #启动一个进程抽取数据，程启动多个线程进行插入
    migratequeue = queue.Queue(InsertMaxThread)
    while True:
        for threadnum in range(InsertMaxThread):
            migratequeue.put(threadnum)
            result = cur.fetchmany(ResultCount)
            #需要把列信息也传过去，用来生成where
            tabledesc=cur.description 
            print("获取结果%s"%len(result))
            if len(result) > 0:
                InsertTask = MulitThreadInsert(result,migratequeue,tablename,threadnum,tabledesc)
                InsertTask.start()
            else:
                print("没有记录了")
                cur.close()
                return 1