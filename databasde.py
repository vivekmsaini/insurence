import sqlite3

conn=sqlite3.connect('insurance.db')

query = """
create table project
(age integer,gender integer,bmi integer,children integer, region varchar(5),smoker integer,health integer,prediction varchar(10))"""

query_to_fetch="""
select * from project
"""
## to create table
cur=conn.cursor()
# cur = conn.cursor() # curser sql
#cur.execute(query)

cur.execute(query_to_fetch)   ## cursor iis a temperary memory
for record in cur.fetchall():
    print(record)


cur.close()
conn.close()