forgive my poor English
this software was developed by python3 and psycopg2.
Because i need one tool to solve my problem which on data migrate.but no one could made me satisfied.those are so fat.And some softwares are not opensource,lead migrate process put in a situation 'FULL EFFORT'.It easy cause oneline database crushed. so i develop it.

this software is not focuse on 'FAST' migrate, i hopping you can approve of my opinion.'FAST' migrate are so ordinary,and 'dump' which is developed by database developer have incomparable speed. but it also have drawback aspect-----not than slower.

yes,control speed is this software's trait.you can put a code 'sleep(x)' on fetch data,insert data or anywhere you think reasonable to made a artificial block to slow down migrate speed.the word is than you have the topest authority to control presue on database services.no malloc function,no lots of memory,but it need more cpu resource to deal with character process.

fetch data need IOPS on source database,insert data need cpu resource on destnation database. i hope you can attention it.

And i develop a function that can archive upsert on all postgresql edition.
but it is slower than none-upsert edition. so i divided them in two folder and named than in diff editon.

i suppose if use address-transmission replace value-transmission,it will have better on  performance.but using address is so denger.so i am not. i have done a lot of imporvement on somewhere i can promiss.you can read this specification on source code . so i just a  DBA,not a developer. do not have more expect.

finally,i wish to diss ali's datax.it's so hard to use,unexpectly must fill a excel file??
so i named my software Adv_Datax .

i am developing a same software but use C language.maybe just dig a hole. 
and maybe develop character-process writed in C funciton.

-------Overlord DBA in TJ

