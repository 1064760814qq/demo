#coding=utf-8
import face_recognition
import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import datetime
import yagmail
import threading
# import smtplib
# from email.mime.text import MIMEText
# # # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
# # mail_host = "smtp.163.com"
# # # 用户名
# # mail_user = "*****"
# # # smpt密码
# # mail_pass = "******"
# # 邮箱的后缀，网易就是163.com
# mail_postfix = "163.com"
# def send_mail(to_list, sub, content):
# me = "<" + mail_user + "@" + mail_postfix + ">"
# msg = MIMEText(content, _subtype='plain', _charset='utf-8')
# msg['Subject'] = sub
# msg['From'] = me
# msg['To'] = ";".join(to_list) # 将收件人列表以‘；’分隔
# try:
#     server = smtplib.SMTP()
#     # 连接服务器
#     server.connect(mail_host)
#     # 登录操作
#     server.login(mail_user, mail_pass)
#     server.sendmail(me, to_list, msg.as_string())
#     server.close()
#     return True
#     # except Exception, e:
#     #     return False
# except Exception as e:
#     print(e)
#     return False


def sendmail(filename):
    yag = yagmail.SMTP(user='1064760814@qq.com', password='lmryjwncirzrbega', host='smtp.qq.com')
    #其中的password是需要到指定的邮箱网址中去获取的，具体去百度。
    contents = [
        '有人进入',
        yagmail.inline(filename)
    ]
    #inline可以添加指定照片，其中可以是filename。

    yag.send(['2215290365@qq.com'], subject='检测到人脸', contents=contents)


class Recorder:
    pass


record_pic={}
unknown_pic=[]

#定时去保存对比图像信息，并且将未知人员的图像保存下来
flag_over = 0#定义一个是否进行来访记录的标记
def save_record(name, frame):
    global record_pic
    global flag_over
    global unkown_pic

    if flag_over == 1:
        return
    try:
        record = record_pic[name]
        seconds_diff = (datetime.datetime.now() - record.times[-1]).total_seconds()
        if seconds_diff < 600:
            return
        record.times.append(datetime.datetime.now())
        print('更新记录', record_pic, record.times)
    except KeyError:
        newRect = Recorder()
        newRect.times = [datetime.datetime.now()]
        record_pic[name] = newRect
        print('添加新增记录', record_pic, newRect.times)
    if name == '迪丽热巴':
        s = str(record_pic[name].times[-1])
        # print(s)
        # 未知人员的图片名称
        filename = s[:10] + s[-6:] + '.jpg'
        print(filename)
        cv2.imwrite(filename, frame)
        unknown_pic.append(filename)
        sendmail(filename)

#解析出已有人员的所有图片并得到照片名和人物编码信息
def load_image(path):
            print('已知图片正在加载')
            for dirpath, dirnames, filenames in os.walk(path):
                print(dirpath, dirnames, filenames)
                im = []
                for filename in filenames:
                    filepath = os.sep.join([dirpath, filename])
                    # 加载图片
                    face_image = face_recognition.load_image_file(filepath)
                    face_encodings = face_recognition.face_encodings(face_image)[0]
                    im.append(face_encodings)
                return im,filenames

im, facenames = load_image('facelib')
print(facenames)
# 调用摄像头
cap = cv2.VideoCapture(0)
while True:
    # 返回一帧的数据
    ret, frame = cap.read()
    # 通过缩小图片增加对比率
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # 将bgr格式转为rgb
    rgb_small_frame = small_frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    # 循环多张人脸
    # print('xxx', ret)
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(im, face_encoding, tolerance=0.48)
        name = '未知头像'
        if True in matches:
            #如果摄像头的头像匹配了已知人物的头像，则取出第一个True的位置
            # 取出第一个匹配到的
            first_match_index = matches.index(True)
            # 取出文件上的人名
            name = facenames[first_match_index][:-4]
        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
            # 还原
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            start = (left, top)
            end = (right, bottom)
            # 标注人脸
            cv2.rectangle(frame, start, end, (0, 0, 255), thickness=2)
            img_PIL = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            font = ImageFont.truetype('simhei.ttf', 40)
            draw = ImageDraw.Draw(img_PIL)
            draw.text((left + 6, bottom - 6), name, font=font, fill=(255, 255, 255))
            frame = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
            save_record(name, frame)
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()