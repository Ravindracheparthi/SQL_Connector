import mysql.connector as db
import sys


def chk_dataBase(db_name):
        cur.execute('show schemas')
        results = cur.fetchall()
        if  (db_name,) in results:                         #checking is schema is already existed
                     print('DataBase existed')
                     return True
        else:
                return False

def schema():
        schema_name=input('enter schema name to use:')#using schema
        res=chk_dataBase(schema_name)
        if res==True:
                cur.execute('use {}'.format(schema_name))
                print('using ',schema_name)
        else:
                return False
        return schema_name
        
def showTables():
        cur.execute('show tables')
        result=cur.fetchall()
        return result
       
def chk_Tables(tb_name):
        res=showTables()
        if (tb_name,) in res:
                print(tb_name,' existed')                #showing tables
                return True
        else:
                return False
def col_list(table_name):
          cur.execute('desc {}'.format(table_name))    #checking how many colums in table
          res=cur.fetchall()
          i=0
          for desc in res:
                  i=i+1         #counting the columns
                  print(desc[0],' ',desc[1],',',end='' )
          print()
          return i
def callProcedure(schema_name):
        cur.execute("show procedure status where db='{}' ".format(schema_name))
        print('procedure list in ',schema_name)
        procedure=cur.fetchall()
        for pro in procedure:
                print(pro[1],' ,',end='')
        print()
        pro_name=input('enter procedure name:')
        cur.callproc('{}'.format(pro_name))#calling the procedure
        res=cur.stored_results()
        for result in res:
                for re in result:
                        print(re)
                        
def file_open(fp_name):
        fp=open('{}.txt'.format(fp_name),'r')
        res=fp.read()
        data=res.split(input('enter delimiter to seperate the records:'))               #file opening
        split_d=input('enter delimiter to sperate the values:')
        k=''
        for req_data in data:
                insert_query='('
                x=req_data.split(split_d)
                for i in x:
                        if i!=x[-1]:
                                 insert_query+=i+','
                        else:
                                insert_query+=i   
                insert_query+=')'
                k+=insert_query+','
        fp.close()
        if k[-1]==',':
                k=k[0:-1]        
        return k
               
con=db.connect(username='root',password='ravindra@123Ravi',host='localhost')
cur=con.cursor()
print('DB connection open')
try:
        while True:
                    print('Menu\n1.Schema creation/Deletion\t2.Table Creation/Deletion\n3.Show Table list\t\t4.Data Insert\n5.Show Table Data\t\t6.select data or call procedure\n7.Import files\t\t8.exit')
                    ch=int(input('enter your choice:'))
                    if ch==1:
                            choice=int(input('1.Create a DataBase\n2.Delete a DataBase\nEnter your choice:'))
                            if choice==1:
                                    schema_name=input('enter database name to be created:')
                                    res=chk_dataBase(schema_name)
                                    if res==False:
                                        cur.execute('create database {}'.format(schema_name))            #schema is creating if not existed
                                        print(schema_name,'schema created',)
                            else:
                                 schema_name=input('enter database name to delete:')
                                 res=chk_dataBase(schema_name)
                                 if res==True:
                                         cur.execute('drop database {}'.format(schema_name))
                                         print('Database deleted successfully')
                                 else:
                                       print('Database not existed')
                            print('-'*50)                   
                    elif ch==2:
                        choice=int(input('1.Create a table\n2.Delete a table\nEnter your choice:'))
                        res=schema()
                        if res!=False:
                                if choice==1:
                                        num_table=int(input('enter no of tables you want to create:'))
                                        for i in range(1,num_table+1):                                                                                     #creating the table
                                            table_name=input('enter table name:')
                                            res=chk_Tables(table_name)                                     #checking if table is already existed
                                            if res==False:
                                                col_num=int(input('enter no.of columns in table:'))
                                                create_table='create table {}'.format(table_name,)+'('
                                                for i in range(1,col_num+1):
                                                    col_name=input('enter column name :')                        #creating the table if not exists
                                                    col_type=input('enter data type:')
                                                    if i<col_num:
                                                        create_table+=col_name+' '+col_type+','
                                                    else:
                                                        create_table+=col_name+' '+col_type
                                                create_table+=')'
                                                cur.execute(create_table)
                                                print('Table ',table_name,' is created')
                                else:
                                        
                                        table_name=input('Enter table name to delete:')
                                        res=chk_Tables(table_name)
                                        if res==True:
                                                cur.execute('drop table {}'.format(table_name))
                                                print('table deleted successfully')
                                        else:
                                                print('table not existed')
                        else:
                                print('Database not existed')
                                print('hi')
                        print('-'*50)
                    elif ch==3:
                        result=schema()
                        if result!=False:
                                res=showTables()                       #showing the available tables in schema
                                for table_name in res:
                                    print(table_name,end='')
                                print()
                        else:
                                print('Database not existed')
                        print('-'*50)
                    elif ch==4:
                          res=schema()
                          if res!=False:
                                  table_name=input('enter table name:')
                                  record_insert=int(input('how many records to be inserting:'))     #inserting values into table
                                  ch=int(input('1.Data Into specific columns\n2.entire columns\nEnter your choice:'))
                                  if ch==1:
                                          insert_values='insert into {} ('.format(table_name)
                                          k=col_list(table_name)
                                          i=0
                                          while True:
                                                  i+=1
                                                  col_name=input('enter column name to insert:')
                                                  insert_values+=col_name
                                                  add=input('do you want to add more columns(y/n):')
                                                  if add=='y':
                                                          insert_values+=','
                                                  else:
                                                          insert_values+=') values('
                                                          break
                                  else:
                                          insert_values='insert into {} values'.format(table_name)+'('
                                          i=col_list(table_name)
                                  for k in range(1,record_insert+1):
                                           for j in range(1,i+1):
                                                 if j<i:
                                                         insert_values+=input('enter value to insert:')+','      #inserting 1 or more records
                                                 else:
                                                         insert_values+=input('enter value to insert:')
                                           if k<record_insert:
                                                 insert_values+='),('
                                           else:
                                                 insert_values+=')'
                                  cur.execute(insert_values)
                                  cur.execute('commit')
                                  print('values inserted')
                          else:
                                  print('Database not existed')
                          print('-'*50)
                    elif ch==5:
                            result=schema()
                            if result!=False:
                                    table_name=input('enter table name:')
                                    res=chk_Tables(table_name)
                                    if res==True:
                                            sql_query='select'
                                            ch=int(input('1.add need individual columns \n2. entire table\nEnter your choice:'))
                                            if ch==1:
                                                    res=col_list(table_name)
                                                    while True:
                                                        col_name=(input('enter column name to add:'))
                                                        sql_query+=' '+col_name
                                                        ch=input('do u want to add more columns(y/n):')
                                                        if ch=='n':
                                                                break
                                                        else:
                                                                sql_query+=','
                                                    sql_query+=' '+'from {};'.format(table_name)
                                            else:
                                                    sql_query+=' '+'* from {};'.format(table_name)
                                            cur.execute(sql_query)
                                            res=cur.fetchall()
                                            for i in res:
                                                   print(i,'\t')
                                    else:
                                          print(table_name,' not existed\n')
                            else:
                                  print('Database not existed')
                            print('-'*50)
                    elif ch==6:
                            pr=int(input('1.do you want to create a procedure\n 2.call a procedure\nEnter Your choice:'))
                            if pr==1:
                             import pro
                             del sys.modules['pro']
                                  #from pro import procedure,procedureInout
                            else:
                                    import callpro
                                    del sys.modules['callpro']
                                    
                             #       res=schema()
                              #      if res!=False:
                               #             s=input('enter schema name to see Procedure list:')
                                #            cur.execute('use {}'.format(s))
                                 #           callProcedure(s)      # calling function to call procedure
                                  #  else:
                                   #         print('Database not existed')
                            print('-'*50)

                    elif ch==7:
                            file_name=input('enter file name to open:')
                            insert_values=file_open(file_name)
                            result=schema()
                            if  result!=False:
                                    table_name=input('enter table name to enter values:')
                                    res=chk_Tables(table_name)
                                    if res==True:
                                            cur.execute('insert into {} values'.format(table_name)+insert_values)
                                            cur.execute('commit')
                                            print('Values inserted')
                                    else:
                                            print('Table is not existed')
                            else:
                                    print('Database not existed')
                            print('-'*50)
                    elif ch==8:
                        break
except ValueError:
        print('given value is incorrect')
except Exception:
        print('Something went wrong please run again the code')
finally :
        con.commit()
        cur.close()
        con.close()
        print('DB connection closed')


