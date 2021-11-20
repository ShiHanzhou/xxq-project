import base64
import cv2
import socket
import threading
import numpy as np
from flask import render_template, Response, Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import pymysql
import traceback
from werkzeug.utils import secure_filename
import os
from banevent import userManage, ban, unban
import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=["POST", "GET"])
def login():
    global username
    username = 0
    return render_template("index.html")


@app.route('/register')
def register():
    global username
    username = 0
    return render_template("register.html")


@app.route('/user')
def user():
    if username == 0:
        return render_template("index.html")
    return render_template("user.html", username=username)


@app.route('/master', methods=['GET', 'POST'])
def master():
    if username == 0:
        return render_template("index.html")
    if request.method == 'POST':
        x1 = request.form["x1"]
        y1 = request.form["y1"]
        x2 = request.form["x2"]
        y2 = request.form["y2"]
        try:
            if 0 < int(x1) < 500 and 0 < int(y1) < 281 and 0 < int(x2) < 500 and 0 < int(y2) < 500:
                if int(x1) > int(x2):
                    x1, x2 = x2, x1
                if int(y1) > int(y2):
                    y1, y2 = y2, y1
                send = x1 + ' ' + y1 + ' ' + x2 + ' ' + y2
                print(send)
                if s is not None:
                    s.send(send.encode("utf-8"))
        finally:
            return render_template("master.html", username=username)
    return render_template("master.html", username=username)


@app.route('/masterecord')
def masterecord():
    if username == 0:
        return render_template("index.html")
    conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                           db='shi_pin_xxq', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM photo"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    p = []
    for i in u:
        k = list(i)
        k[2] = "data:image/jpg;base64," + str(i[2])
        p.append(k)
    p = tuple(p)
    if len(p) > 10:
        p = p[len(p) - 10:]
    return render_template("masterecord.html", u=p, username=username)


@app.route('/userecord')
def userecord():
    if username == 0:
        return render_template("index.html")
    conn = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                           db='shi_pin_xxq', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM photo"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    p = []
    for i in u:
        k = list(i)
        k[2] = "data:image/jpg;base64," + str(i[2])
        p.append(k)
    p = tuple(p)
    if len(p) > 10:
        p = p[len(p) - 10:]
    return render_template("userecord.html", u=p, username=username)


@app.route('/userstate')
def userstate():
    if username == 0:
        return render_template("index.html")
    u = userManage()
    return render_template("userstate.html", u=u, username=username)


@app.route("/banevent", methods=['GET', 'POST'])
def banevent():
    event = request.form["event"]
    user1 = request.form["user"]

    result = {'result': "fault"}
    if event == "ban":
        ban(user1)
        result['result'] = "success"
    elif event == "unban":
        unban(user1)
        result['result'] = "success"
    else:
        pass
    return jsonify(result)


# ==============================================登陆注册===================================================
@app.route('/regist', methods=["POST", "GET"])
def getRigistRequest():
    # 把用户名和密码注册到数据库中

    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                         db='shi_pin_xxq', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    f = request.files['file']

    if not (f and allowed_file(f.filename)):
        return render_template("verification.html", message="请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp")

    basepath = os.path.dirname(__file__)  # 当前文件所在路径

    upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)

    # 使用Opencv转换一下图片格式和名称
    img = cv2.imread(upload_path)
    cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%Y-%m-%d %H:%M:%S")

    # 需要改地址
    fin = open("D:/Desktop/Python/ComStudy/Web/static/images/test.jpg", 'rb')  # 'rb'加上才能将图片读取为二进制

    img = base64.b64encode(fin.read())
    fin.close()
    sql = "INSERT INTO face_recognize(photo) VALUES(%s);"
    args = img

    cursor.execute(sql, args)  # 执行相关操作
    verCode = request.form.get('verCode')
    if str(verCode) != str(code):
        message = "您输入的验证码不正确，请重新输入"
        return render_template('verification.html', message=message)

    sql = "INSERT INTO user(username, password,email,type,action,ban,if_online) VALUES(%s,%s,%s,%s,%s,%s,%s);"
    args = (username, password, email, 'user', 0, 'available', 'offline')
    try:
        # 执行sql语句
        cursor.execute(sql, args)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        message = "注册成功，请登录"
        return render_template('index.html', message=message)
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()


@app.route('/login', methods=["POST", "GET"])
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB

    db = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                         db='shi_pin_xxq', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    username1 = request.form.get("username")
    password = request.form.get("password")
    if not all([username1, password]):
        message = "用户名或者密码不能为空！请重新输入"
        return render_template('index.html', message=message)

    # SQL 查询语句
    sql = "select * from user where username = %s and password = %s "
    args = (username1, password)

    try:
        # 执行sql语句
        cursor.execute(sql, args)
        results = cursor.fetchall()
        if len(results) == 1:
            result = results[0]
            if str(result[6]) == "available":
                sql = "UPDATE user SET if_online = 'online' WHERE username = %s"
                args = username1
                global username
                username = username1
                cursor.execute(sql, args)
                db.commit()
                if str(result[4]) == "admin":
                    return render_template('master.html', username=username)
                return render_template('user.html', username=username)
            else:
                message = "该用户已被拉入黑名单，请联系管理员解封"
                return render_template('index.html', message=message)
        else:
            message = "用户名或者密码不正确"
            return render_template('index.html', message=message)
        # 提交到数据库执行
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()


code = 0000000000
username = 0
password = 0
email = 0


@app.route('/Code', methods=["POST", "GET"])
def sendEmail():
    number = []
    global username, password, email
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get('email')
    if not all([username, password, email]):
        message = "用户名,密码或邮箱不能为空！请重新输入"
        return render_template('register.html', message=message)
    if len(username) < 5 or len(password) < 5:
        message = "用户名或密码长度不能小于5"
        return render_template('register.html', message=message)

    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect(host='rm-bp12m3039u29b56w32o.mysql.rds.aliyuncs.com', user='root', password='POiu0987',
                         db='shi_pin_xxq', charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql1 = "select username from user where username = %s"
    args1 = username
    cursor.execute(sql1, args1)
    results = cursor.fetchall()
    if len(results) != 0:
        message = "该用户名已被使用，请重新输入"
        return render_template('register.html', message=message)

    for i in range(6):
        num = random.randint(0, 9)
        number.append(num)
    number = [str(j) for j in number]
    global code
    code = int(''.join(number))

    from_addr = '2569856381@qq.com'
    password1 = 'tbccpolpfohjdhgd'

    to_addr = email

    smtp_server = 'smtp.qq.com'

    msg = MIMEText('Your verification code is ' + str(code) +
                   ',please do not disclose or forward to others', 'plain', 'utf-8')

    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('[tip]')

    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)

    server.login(from_addr, password1)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    message = "验证码发送成功，请及时输入！"
    print(code)
    return render_template("verification.html", message=message)


# ==============================================视频流====================================================
outputFrame = None
lock = threading.Lock()
s = None


def generate():
    global outputFrame, lock, s

    host = '192.168.0.110'
    port = 5354
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    t = threading.Thread(target=video_feed, args=())
    t.start()

    # loop over frames from the output stream
    while True:
        outputFrame = s.recv(10240)
        msg = np.fromstring(outputFrame, np.uint8)
        img_decode = cv2.imdecode(msg, cv2.IMREAD_COLOR)
        flag = False
        try:
            shape = img_decode.shape
            img_decode = img_decode
            temp = img_decode
        except:
            pass

        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            if img_decode is not None:
                (flag, encodedImage) = cv2.imencode(".jpg", img_decode)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# start the flask app
if __name__ == "__main__":
    app.run()
