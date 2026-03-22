import mysql.connector as db
from dotenv import load_dotenv
import os
load_dotenv()

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
try:
        con = db.connect(username='root', password=os.environ.get('DB_PASSWORD'), host='localhost') 
        cur=con.cursor()
        res=schema()
        if res!=False:
            callProcedure(res)
        else:
                print('Database not existed')
except Exception as e:
        print('Error occur',e)
finally:
        con.commit()
        cur.close()
        con.close()

                    
