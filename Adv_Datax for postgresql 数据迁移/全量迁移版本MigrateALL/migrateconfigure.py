#需要迁移的表清单
MoveTableList=['tablename']
#获取数据的sql
DataFetchRuleSql="select * from %s "
#最大抽取数据进程数
SourceMaxThread=4
#最大插入数据线程数
InsertMaxThread=30
#一次抽取数据的结果集
ResultCount=2000
#源端DB
sourceuser="sourceusername"
sourcepassword="password"
sourcehost="hostname or ip"
sourceport=5432
sourcedbname="sourcedbname"
#目标端DB
destuser="destusername"
destpassword="password"
desthost="hostname or ip"
destport=5432
destdbname="destdbname"