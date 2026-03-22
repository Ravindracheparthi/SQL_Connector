import mysql.connector as db

'''
def count(p_name,t_name,schema_name,in_count,out_count,inout_count):
    with open('{}.txt'.format(schema_name),'a') as fp:
        fp.write('Table name:-{}\n'.format(t_name))
        fp.write('procedure name:-{}\n'.format(p_name))
        fp.write('in count:-{}\n'.format(in_count))
        fp.write('out count:-{}\n'.format(out_count))
        fp.write('inout count:-{}\n\n'.format(inout_count))
'''

def schema():
        schema_name=input('enter schema name to use:')   #using schema
        cur.execute('show schemas')
        results = cur.fetchall()
        if  (schema_name,) in results:                         #checking is schema is already existed
                     print('DataBase existed')
                     cur.execute('use {}'.format(schema_name))
                     print('using ',schema_name)
                     return schema_name
        else:
                print(schema_name,'not existed')
                return False

def pro_list(p_name,schema_name):        
        cur.execute("show procedure status where db='{}' ".format(schema_name))
        for pro in cur.fetchall():
                if pro[1]==(p_name):
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


def procedureInout(adding_procedure,p_name,t_name,res):
                in_count=0
                out_count=0
                inout_count=0
                while True:                                                                                      #passing parameters to procedure in ,out,inout
                        opt=int(input('1.in\n2.out\n3.inout\nenter your choice:'))
                        var_name=input('enter variable name:')
                        var_type=input('Variable type:')
                        if opt==1:
                                in_count+=1
                                adding_procedure+='in'+' '+var_name+' '+var_type
                                cnt=input('do u want to add more(y/n):')
                                if cnt=='y':
                                        adding_procedure+=', '
                                else:
                                    break    
                        elif opt==2:
                                out_count+=1
                                adding_procedure+='out'+' '+var_name+' '+var_type
                                cnt=input('do u want to add more(y/n):')
                                if cnt=='y':
                                        adding_procedure+=', '
                                else:
                                    break                                     
                        elif opt==3:
                                inout_count+=1
                                adding_procedure+='inout'+' '+var_name+' '+var_type
                                cnt=input('do u want to add more(y/n):')
                                if cnt=='y':
                                        adding_procedure+=', '
                                else:
                                    break
                adding_procedure+=')'
                count(p_name,t_name,res,in_count,out_count,inout_count)
                return adding_procedure

def procedure():
        res=schema()
        if res!=False:
                p_name=input('enter procedure name:')
                catch=pro_list(p_name,res)#creating a procedure
                if catch==True:
                        print('Procedure already existed')
                        return False
                else:
                        t_name=input('enter table name:')
                        cur.execute('show tables')
                        result=cur.fetchall()
                        if (t_name,) in result:                       
                                create_procedure='drop procedure if exists {};\ncreate procedure {}('.format(p_name,p_name)
                                ch=input('you want to give any parameters(in or out or inout)(y/n):')
                                if ch=='y':
                                        create_procedure=procedureInout(create_procedure,p_name,t_name,res)
                                else:
                                        create_procedure+=')'
                                create_procedure+='\nbegin\nselect '
                                ch=int(input('1.individual columns \n2. entire table\nEnter your choice:'))
                                if ch==1:
                                        res=col_list(t_name)
                                        while True:
                                                col_name=(input('enter column name to add:'))
                                                create_procedure+=col_name
                                                ch=input('do u want to add more columns(y/n):')
                                                if ch=='n':
                                                        break
                                                else:
                                                        create_procedure+=','
                                        create_procedure+=' from {}'.format(t_name)+';\nend;'
                                else:
                                        create_procedure+='* from {}'.format(t_name)+';\nend;'
                                return create_procedure
                        else:
                            print('Table not exist')
                            return False
        else:
                print('Database not exist')
                return False
try:
    con=db.connect(username='root',password='ravindra@123Ravi',host='localhost')
    cur=con.cursor()
    #print('DB connection open')
    #print('1.create procedure \t\t2.Table Creation/Deletion\n3.Show Table list\t\t4.Data Insert\n5.schema creation\t6.Show Table Data\n7.Import files\t\t8.call Procedure\n9.exit')
    ch=1
    if ch==1:
            res=procedure() #calling function to create a procedure
            if res!=False: 
                    cur.execute(res)
                    print('procedure created successfully')
except db.Error as e:
    print('e')
finally:
    if cur:
        cur.close()
    if con:
        con.close()

