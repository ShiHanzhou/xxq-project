import pymysql

conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                       db='shi_pin_xxq', charset='utf8')


def ban(user):
    cur = conn.cursor()
    sql = "UPDATE user SET ban = 'unavailable' WHERE type = 'user' and username = '" + str(user) + "'"
    cur.execute(sql)
    conn.commit()


def unban(user):
    cur = conn.cursor()
    sql = "UPDATE user SET ban = 'available' WHERE type = 'user' and username = '" + str(user) + "'"
    cur.execute(sql)
    conn.commit()


def userManage():
    cur = conn.cursor()
    sql = "SELECT username,if_online,ban FROM user WHERE type = 'user'"
    cur.execute(sql)
    u = cur.fetchall()
    return u
