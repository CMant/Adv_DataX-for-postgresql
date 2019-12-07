'''
这部分文件用来做字符出处理，生成where语句，insert语句，如果要支持其他版本，也能写道这里。

'''
def GenerWhere(pkeycol,rowtuple,tupledesc):
    #用来生成where语句后面的条件。可以被多次调用。减少字符串重复处理过程,这里的where只用来生成主键对应关系，其余的列不生成。
    wherestr=""
    for t in range(len(pkeycol)):
        if t==0:
            wherestr=wherestr+" %s='%s'"
            wherestr=wherestr%(tupledesc[pkeycol[t]-1][0],rowtuple[pkeycol[t]-1])             
        else:  
            wherestr=wherestr+" and %s='%s'"
            wherestr=wherestr%(tupledesc[pkeycol[t]-1][0],rowtuple[pkeycol[t]-1])
    return wherestr  
    pass


'''这个函数传入单行记录，进行解析，这个程序中已经不使用了，但是这个代码的功能没问题，先放着。通过GenerInsertALL 一次把几千个sql拼成一个事务，这样可以避免多次执行execute
def GenerInsert(row,tablename):

    substr=""
    for i in range(len(row)):
        if row[i] is None:
            substr=substr+'%s ,'%'NULL'
        else:
            rowt=str(row[i]).replace("\'","\'\'")              
            substr=substr+'\'%s\','%rowt
    substr=substr[:-1]
    insertsql="insert into  \"%s\" values(%s);"%(tablename, substr)
    return  insertsql
'''

def GenerInsertALL(result,tablename):
    insertall=""
    substr=""
    for row in result:
        for i in range(len(row)):
            if row[i] is None:
                substr=substr+'%s ,'%'NULL'
            else:
                rowt=str(row[i]).replace("\'","\'\'")              
                substr=substr+'\'%s\','%rowt 
        substr=substr[:-1]
        insertsql="insert into  \"%s\" values(%s);"%(tablename, substr)
        substr=''
        insertall=insertall+insertsql
    return  insertall



'''
#此处字符串没有使用join的原因有
 for i in result:
        bb.append("'")
        for s in i:        
            x=str(s).replace("\'","\'\'")
             #这里字符串中的单引号全部替换成两个单引号进行转义，这一步是没问题的
            #print(x)
            if x=="None":
                bb.append("NULL")
               #对空值进行转换
            else:           
                bb.append(x)       
        bb.append("'")
        #print(bb)
        qq=""
        qq='\',\''.join(bb)  
         #通过join之后，list中含有的双引号，单引号会自动去除，然后在join的过程中需要在此添加单引号
          #关键的问题也是在这里。之前的None已经替换为NULL了。现在又被加上了单引号，在insert中  'NULL'语法错误
          #但是如果后面使用replace对整个字符串进行 'NULL'替换是肯定不正确的，假如有一行记录为 "饺子''None''盒'"  字符串中偏偏就写入了None 而且还是包含单引号的None，那么进行替换肯定是不正确的。
          #所以无论怎么处理，最后仍然会回到字符串上面。此处对结果集处理要注意，一个tuple，一定要一次处理完毕，不能整行合并完毕之后再处理，很容易产生错误。
          #呐，如果你又说，“对 ('None',   ,'None')  ,'None',  替换不就可以了吗？” 年轻人，你太大意了。难道记录就不能写成这样吗？    '饺子,''None'',盒' 
          #所以这个问题暂时无解，字符串处理的速度大概是 1万/s  大部分的性能都消耗在 execute(insert)当中。



          if row[i] is None:
                substr=substr+'%s ,'%'NULL'
            else:
                rowt=str(row[i]).replace("\'","\'\'")              
                substr=substr+'\'%s\','%rowt
                比如这段代码就不存在上面的问题，字符串转换在一个tuple中完成，后面只需要++++就可以了。

                insertall=insertall+insertsql
                对于最后的这段代码没有采用 append 再 join的方法，因为测试过以后发现比直接++++还要慢
        
            
        print(qq)
        xs="insert into xxx values (%s);"%qq[:-3][3:]
        tt.append(xs)
       # print(xs)
        bb=[]
    allin=''.join(tt)
  #  print(allin)

'''