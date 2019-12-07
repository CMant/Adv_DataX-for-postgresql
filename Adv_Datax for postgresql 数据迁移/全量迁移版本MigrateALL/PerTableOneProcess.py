import queue
import threading
from migrateconfigure import SourceMaxThread,MoveTableList,DataFetchRuleSql
from FetRowFunc import FetchResultFromSource
from multiprocessing import Pool
'''
之前用这段代码实现的，但是我忘了为什么被注释掉了。后来又选择了线程池的方式作为启动多线程的做法，代码更精简，但是这段代码还是有参考价值。
我又想起来了。因为这段代码是 多线程的，只能调用一个cpu核心，如果想利用多核心性能，应该用多进程模型，但是这种方式也有好处，就是对cpu资源压制地更好。

# class MulitTableProcess(threading.Thread):
#     def __init__(self,mulitprocessqueue,tablename,GetDataSql):
#         threading.Thread.__init__(self)
#         self.mulitprocessqueue = mulitprocessqueue
#         self.tablename=tablename
#         self.GetDataSql=GetDataSql
#     def run(self):
#         try:
#             print('正在启动%s迁移任务' %self.tablename)
#             FetchResultFromSource(self.tablename,self.GetDataSql)
#         except Exception as e:
#             print(e)
#         finally:
#             self.mulitprocessqueue.get()
#             self.mulitprocessqueue.task_done()
# def StartMigrate():
#     mulitprocessqueue = queue.Queue(SourceMaxThread)
#     for tablename in MoveTableList:
#         GetDataSql=DataFetchRuleSql%tablename
#         mulitprocessqueue.put(tablename)
#         mulitpumptable = MulitTableProcess(mulitprocessqueue,tablename,GetDataSql)
#         mulitpumptable.start()
#     mulitprocessqueue.join()
#     print('over')
下面这段程序使用了进程池
'''
def StartMigrate():
    pool = Pool(processes=SourceMaxThread)
    for tablename in MoveTableList:
        GetDataSql=DataFetchRuleSql%tablename
     
        pool.apply_async(FetchResultFromSource, args=(tablename,GetDataSql)) 
    pool.close()
    pool.join()
    
 
    print('over')