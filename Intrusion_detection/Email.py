import MySQLdb
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import base64
# 图片转字节
import pymysql
import datetime

def sendpic():
    try:
        conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', port=3306, user='root',
                               passwd='POiu0987', db='shi_pin_xxq', charset='utf8')
        print('successfully connect')
        cursor = conn.cursor()
        curr_time = datetime.datetime.now()
        time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")

        #需要改地址
        filename = 'D:/pythonCharm/Intrusion_detection/supervision/image/pic.jpg'
        fin = open(filename, 'rb')  # 'rb'加上才能将图片读取为二进制

        img = base64.b64encode(fin.read())
        #print(time_str)
        #print(img)
        fin.close()
        sql = "INSERT INTO PHOTO VALUES  (%s,%s,%s);"  # 将数据插入到mysql数据库中，指令
        args = (0, curr_time, img)

        cursor.execute(sql, args)  # 执行相关操作
        conn.commit()  # 更新数据库
        cursor.close()
        conn.close()
    except Exception as e:
        print("数据存入失败，原因为：", e)

def send_email(receiver):
    smtpserver = 'smtp.163.com'
    username = 'c82151778@163.com'
    sender = 'c82151778@163.com'
    password = 'QMAEAANJEGIKYLQZ'

    subject = '入侵检测'

    msg = MIMEMultipart('alternative')

    msg['Subject'] = subject
    msg['From'] = 'c82151778@163.com'
    msg['To'] = receiver

    # 邮件正文

    text = "有陌生人闯入"

    part1 = MIMEText(text, 'plain', _charset='utf-8')

    msg.attach(part1)

    # 开始发送
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    print('22222222222222')
    try:
        smtp.sendmail(sender, receiver, msg.as_string())
        time.sleep(2)  # 等待一分钟，防止被服务器屏蔽
    except:
        print(' 邮件发送失败！')
    print('1111111')
    smtp.quit()
    print(receiver)
    print(' 邮件发送成功！')


def Email():
    # 连接
    conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', port=3306, user='root',
                               passwd='POiu0987', db='shi_pin_xxq', charset='utf8')

    # 游标
    cur = conn.cursor()

    # 创建数据库
    sql = "SELECT email FROM user"
    cur.execute(sql)

    for row in cur.fetchall():

        for mail in row:
            send_email(mail)

            print(mail)
    # 关闭
    cur.close()
    conn.close()


def search():
    conn = pymysql.connect(host='rm-2ze8v2149pild9r0fbo.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                           db='shi_pin_xxq', charset='utf8')

    # 游标
    cur = conn.cursor()

    # 创建数据库
    sql = "SELECT email FROM user"
    cur.execute(sql)

    for row in cur.fetchall():

        for mail in row:
            send_email(mail)
            print(mail)
    # 关闭
    cur.close()
    conn.close()