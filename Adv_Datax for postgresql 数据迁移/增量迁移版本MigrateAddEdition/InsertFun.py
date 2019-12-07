import psycopg2
from GenerStr import *
from psycopg2.extras import RealDictCursor, execute_values
from migrateconfigure import destdbname,desthost,destpassword,destport,destuser
from time import strftime, localtime
'''
这个函数已经用不到了。是用来做重复记录检测的。也可以放在其他地方使用
def DuplicateCheck(cur,tablename,wherestr):
    checkstr="select 1 from %s where %s"%(tablename,wherestr)
    cur.execute(checkstr)
    checkresult=cur.fetchone()
    if checkresult:
        return 1  
    return 0
    pass

GetPkey 这个函数有点像Str的功能，但是因为涉及到对数据库的查询，所以没有放在纯粹处理字符串的generstr文件中
'''
def DeleteDuplicate(cur,tablename,wherestr):
    delstr="delete from %s where %s"%(tablename,wherestr)
    cur.execute(delstr)
    return 0 
def GetPkey(cur,tablename):
    #用来返回这表的主键列id
    cur.execute("select pg_constraint.conkey from pg_constraint  inner join pg_class on pg_constraint.conrelid = pg_class.oid where pg_class.oid = '%s' :: regclass and pg_constraint.contype='p'"%tablename)
    pkeyidresult=cur.fetchall()
    print(len(pkeyidresult))
    if len(pkeyidresult)==0:
        print("空")
    else:
  
        return pkeyidresult[0][0] 

def DeleteDuplicateAll(cur,result,tablename,tupledesc):
    pkeyid=GetPkey(cur,tablename)
    if len(result)>0:
        try:
            for row in result:
                wherestr=GenerWhere(pkeyid,row,tupledesc)
                DeleteDuplicate(cur,tablename,wherestr)
        except psycopg2.DatabaseError as e:
            print(e)
            return 1

def StartInsert(result,tablename,id,tupledesc):
    conn = psycopg2.connect(dbname=destdbname, user=destuser,password=destpassword, host=desthost, port=destport)
    conn.set_session( autocommit=False)
    cur=conn.cursor()
    #pkeyid=GetPkey(cur,tablename)
    if len(result)>0:
        try:
            DeleteDuplicateAll(cur,result,tablename,tupledesc)
            cur.execute(GenerInsertALL(result,tablename))
        except psycopg2.DatabaseError as e:
            print(e)
            conn.rollback()
            return 1
            
            '''
            if DuplicateCheck(cur,tablename,wherestr)==1:
                DeleteDuplicate(cur,tablename,wherestr)
              本来这里打算检测一下有没有重复记录，如果有的话就删除。后来觉得，检测完全就没有必要。如果重复的话，删空就行了。
              这段代码留着，作为记录。
                pass '''
           
    print(cur.rowcount)
    conn.commit()
    print(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print("提交%s"%tablename)
    return 0
