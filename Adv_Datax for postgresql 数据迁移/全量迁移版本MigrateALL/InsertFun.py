import psycopg2
from GenerStr import *
from psycopg2.extras import RealDictCursor, execute_values
from migrateconfigure import destdbname,desthost,destpassword,destport,destuser
from time import strftime, localtime
'''
如果是初次初始化，没有重复数据的情况下。DuplicateCheck DeleteDuplicate GetPkey
函数都是用不到的。所以此处做了注释，这些代码放在了 支持“upsert”的那套程序里。

并不想通过参数来区分。完全是多出一些无意义的判断。

实际用的时候，比如增量模式，可能以后再也不需要判断到底是不是要增量。

还不如分成两套程序


def DuplicateCheck(cur,tablename,wherestr):
    checkstr="select 1 from %s where %s"%(tablename,wherestr)
    cur.execute(checkstr)
    checkresult=cur.fetchone()
    if checkresult:
        return 1  
    return 0
    pass
def DeleteDuplicate(cur,tablename,wherestr):
    delstr="delete from %s where %s"%(tablename,wherestr)
    cur.execute(delstr)
    return delstr 
def GetPkey(cur,tablename):
    #用来返回这表的主键列id,如果pg的数据字典变了，修改这段sql就行
    cur.execute("select pg_constraint.conkey from pg_constraint  inner join pg_class on pg_constraint.conrelid = pg_class.oid where pg_class.oid = '%s' :: regclass and pg_constraint.contype='p'"%tablename)
    pkeyidresult=cur.fetchall()
    print(len(pkeyidresult))
    if len(pkeyidresult)==0:
        print("空")
    else:
  
        return pkeyidresult[0][0]


'''

def StartInsert(result,tablename,id,tupledesc):
    conn = psycopg2.connect(dbname=destdbname, user=destuser,password=destpassword, host=desthost, port=destport)
    conn.set_session( autocommit=False)
    cur=conn.cursor()
    if len(result)>0:
        try:
            cur.execute(GenerInsertALL(result,tablename))
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            return 1
    print(cur.rowcount)
    conn.commit()
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print("提交%s"%tablename)
    return 0