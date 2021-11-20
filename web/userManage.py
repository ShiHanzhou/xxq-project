import pymysql

conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                       db='shi_pin_xxq', charset='utf8')
cur = conn.cursor()
sql = "SELECT username,if_online,ban FROM user WHERE type = 'user'"
cur.execute(sql)
u = cur.fetchall()
conn.close()
