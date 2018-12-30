import re
import os
import sqlite3
import random
import datetime
import time

def create_table(db_name):
    conn = sqlite3.connect(db_name)
    try:
        create_tb_cmd='''
        CREATE TABLE IF NOT EXISTS DAODEZHENJING_CONTENT
        (word CHAR(20),
        word_count INT    
        );
        '''
        conn.execute(create_tb_cmd)
    except:
        print( "Create table failed")
        return False 
    conn.commit()
    conn.close() 

def exists_in_db(data,db_name):
   (word,word_count)=data
   sql = "select count(*)  from DAODEZHENJING_CONTENT where word='%s' "%word
   conn = sqlite3.connect(db_name)
   c = conn.cursor()
   try:
       counts = 0 
       cursor = c.execute(sql)
       for row in cursor:
           counts = row[0]
           break
       #print('counts=%s'%counts)
       if counts > 0 :
           conn.close()
           return True
       else:
           conn.close()
           return False
   except:
        print ("select table failed\n SQL:%s"%sql)
        conn.close()
        return False

def get_word_counts_By_word(data,db_name):
   (word,word_count)=data
   sql = "select word_count  from DAODEZHENJING_CONTENT  where word='%s' "%(word)
   conn = sqlite3.connect(db_name)
   c = conn.cursor()
   try:
        counts = 0 
        cursor = c.execute(sql)
        for row in cursor:
           counts = row[0]
           break
        conn.close()
        return counts
   except:
        print ("select word_count failed\n SQL:%s"%sql)
        conn.close()
        return 0
    
def update_into_db(data,db_name):
    (word,word_count)=data
    sql = "UPDATE DAODEZHENJING_CONTENT    SET word_count = word_count+1 WHERE word = '%s'; " % (word)
    #print(sql)
    conn = sqlite3.connect(db_name)
    try:
        conn.execute(sql)
        conn.commit()
    except:
        print("update table failed\n SQL:%s"%sql)
        conn.close()
    conn.close()
    
def insert_into_db(data,db_name):
    conn = sqlite3.connect(db_name)
    try:
        sql = "insert into DAODEZHENJING_CONTENT values(?,?)" 
        conn.execute(sql,data)
    except:
        print ("Insert table failed")
        return False 
    conn.commit()
    conn.close()     

def init_data(name=''):
    if name == '':
        sf = r'./道德真经.txt'
    else:
        sf = r'./%s'%name
    sfcontent = ''
    result = []
    with open(sf,'r') as fn:
        sfcontent_list = fn.read().split('\n')
        fn.close()
        for i in range(2,len(sfcontent_list)):
            if(i%2 == 1):
                print(sfcontent_list[i])
                result.append(sfcontent_list[i])
        
    return "\n".join(result)

def filter_qut(content):     
    filter_r = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，；：#1。？『』《》、~@#￥%……&*（）]+", "",content)
    return filter_r

def get_all_words(db_name):
   sql = "select count(*)  from DAODEZHENJING_CONTENT " 
   conn = sqlite3.connect(db_name)
   c = conn.cursor()
   try:
       counts = 0 
       cursor = c.execute(sql)
       for row in cursor:
           counts = row[0]
           break
       if counts > 0 :
           conn.close()
           return counts
       else:
           conn.close()
           return 0
   except:
        print ("select count(*) failed\n SQL:%s"%sql)
        conn.close()
        return 0    

def save_to_file(filename=''):
        s_to_f = ''
        only_one=[]
        len_word = get_all_words('data.db')
        sql = "select word,word_count  from DAODEZHENJING_CONTENT order by word_count desc" 
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        try:
            cursor = c.execute(sql)
            for row in cursor:
               s_to_f += '%s|%s\n'%(row[0],row[1])
               only_one.append({row[0] : row[1]})
               
            with open('./re.csv','w',encoding='utf-8')as fn:
                fn.write(s_to_f)
                fn.close()               
        except:
            print ("select count(*) failed\n SQL:%s"%sql)
            conn.close()
            
        print('===============================')
        for i in range(len(only_one)):
            print(  only_one[i])
        print('总单字:%s'%len_word)    

if __name__=="__main__":
    names_list = ['道德真经.txt']
    create_table('data.db')
    for name in names_list:
        sc = init_data(name)
        clean_content= filter_qut(sc)
        lenth_content = len(clean_content)
        for i in range(lenth_content):
            char = clean_content[i]
            data =(char,1)
            if not exists_in_db(data,'data.db'):
                insert_into_db(data,'data.db') 
            else:
                update_into_db(data,'data.db')          
        save_to_file(name)

    

    
