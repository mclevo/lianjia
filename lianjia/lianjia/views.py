"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template
from lianjia import app
from flask import request,session,url_for,redirect,jsonify
from DB import DBmysql
import json
import os
from random import sample

db = DBmysql()

@app.route('/')
#用户登录模块，包含客户登录和管理员登录
@app.route('/login',methods=['GET','POST'])
def login():
    messages = None
    # request.form.get 是从网页获取需要保存到数据库中的信息
    identity = request.form.get('identity')
    phoneNum = request.form.get('phoneNum')
    pwd = request.form.get('pwd')
    if phoneNum and pwd and identity:
        #身份判断
        if identity == 'customer':          
            # db.xxx()是数据库操作语句，把从网页获取的数据保存到数据库
            userInfo = db.getUser(phoneNum)
            if userInfo and userInfo[0] == pwd:
                #session用于 网页和服务器后台身份识别和保持连接
                session['phoneNum'] = phoneNum
                session['password'] = userInfo[0]
                session['username'] = userInfo[4]
                #redirect(url_for('xxx'))是网页跳转,不带参数
                return redirect(url_for('display_house'))
            else:
                messages = '用户名或者密码错误'
        #身份判断
        elif identity == 'manager':
            managerInfo = db.getManager(phoneNum)
            if managerInfo and managerInfo[0] == pwd:
                session['phoneNum'] = phoneNum
                session['password'] = managerInfo[0]
                session['username'] = managerInfo[1]
                return redirect(url_for('manage_house'))
            else:
                messages = '用户名或者密码错误'

    #render_template 也是网页跳转，可以带参数
    return render_template(
        'login.html',
        message = messages
    )

#用户注册模块
@app.route('/register',methods=['GET','POST'])
def register():
    messages = None
    alias = request.form.get('alias')
    username = request.form.get('username')
    phoneNum = request.form.get('phoneNum')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('pwd1')
    gender = request.form.get('gender')
    age = request.form.get('age')
    if alias and username and phoneNum and pwd and pwd1 and gender and age:
        if pwd == pwd1:
            db.setUser(phoneNum,username,pwd,gender,age,alias)
            messages = '注册成功！'
    return render_template(
        'login.html',
        message = messages
    )

#用户信息修改模块
@app.route('/modifyUserInfo',methods=['GET','POST'])
def modifyUserInfo():
    alias = request.form.get('alias')
    username = request.form.get('username')
    pwd = request.form.get('pwd')
    gender = request.form.get('gender')
    age = request.form.get('age')
    if username and pwd and gender and age:
        phoneNum = session['phoneNum']
        db.updateUser(phoneNum,username,pwd,gender,age,alias)
        return render_template('login.html')
    return render_template(
        'modify_userInfo.html',
        userInfo = db.getUser(session['phoneNum'])
    )

#房源展示模块，查找出所有房源信息和所有房源区域
@app.route('/display_house', methods=['Get','Post'])
def display_house():
    data = db.getHouseInfo()
    area = db.getHouseArea()
    return render_template(
        'display_house.html',
        houseInfo_list = data,
        hotHouse_list = sample(db.getHouseInfo(),10),
        areas = area
    )

#重点哦，根据前端传过来的条件筛选语句，最后在BD数据库函数中拼接 sql语句完成查询
#房源条件查找模块，根据用户选择的条件来筛选出符合条件的房源
@app.route('/select_house', methods=['Get','Post'])
def select_house():
    area = request.form.get('areas')
    rent_way = request.form.get('rent_ways')
    price = request.form.get('prices')
    direction = request.form.get('directions')
    data = db.selectHouseInfo(area,rent_way,price,direction)
    return jsonify(data)


#房源详细信息展示模块，根据房源ID查找出相关房源信息
@app.route('/display_house_detail', methods=['Get','Post'])
def display_house_detail():
    houseID = request.args.get('id')
    data = db.getHouseDetailInfo(houseID)
    return render_template(
        'display_house_detail.html',
        detailInfo = data
    )

#用户管理模块，查找出所有客户信息
@app.route('/manage_userInfo', methods=['Get','Post'])
def manage_userInfo():
    return render_template(
        'manage_userInfo.html',
        userInfos = db.getAllUser()
    )

#管理员添加客户模块
@app.route('/addUser',methods=['GET','POST'])
def addUser():
    alias = request.form.get('alias')
    username = request.form.get('username')
    phoneNum = request.form.get('phoneNum')
    gender = request.form.get('gender')
    age = request.form.get('age')
    pwd = request.form.get('pwd')
    if username and phoneNum and pwd:
        db.setUser(phoneNum,username,pwd,gender,age,alias)
    return redirect(url_for('manage_userInfo'))

#管理员修改用户信息模块
@app.route('/modifyUser',methods=['GET','POST'])
def modifyUser():
    alias = request.form.get('m_alias')
    username = request.form.get('m_username')
    phoneNum = request.form.get('m_phoneNum')
    gender = request.form.get('m_gender')
    age = request.form.get('m_age')
    if username and phoneNum:
        db.modifyUser(phoneNum,username,gender,age,alias)
    return redirect(url_for('manage_userInfo'))

#管理员删除用户模块
@app.route('/delUser',methods=['GET','POST'])
def delUser():
    phoneNum = request.form.get('d_phoneNum')
    if phoneNum:
        db.delUser(phoneNum)
    return redirect(url_for('manage_userInfo'))

#客户进行房源预约模块
@app.route('/reserve',methods=['GET','POST'])
def reserve():
    phoneNum = request.form.get('phoneNum')
    id = request.form.get('id')
    if phoneNum and id:
        db.reserve(phoneNum,id)
    return jsonify("预约成功！")

#预约信息展示模块，查找出所有客户的预约信息
@app.route('/getReserve',methods=['GET','POST'])
def getReserve():
   return render_template(
        'manage_reserveInfo.html',
        reserveInfos = db.getAllReserveInfo()
    )

#房源管理模块，查找出所有的房源信息
@app.route('/manage_house', methods=['Get','Post'])
def manage_house():
    return render_template(
        'manage_house.html',
        houseInfo_list = db.getHouseInfo()
    )

#添加房源，管理员可以输入房源基本信息并添加相关的房源图片
@app.route('/add_house', methods=['Get','Post'])
def add_house():
    #获取网页房源基本信息
    id = request.form.get('id')
    info = request.form.get('info')
    area = request.form.get('area')
    location = request.form.get('location')
    size = request.form.get('size')
    direction = request.form.get('direction')
    rooms = request.form.get('rooms')
    price = request.form.get('price')
    rent_way = request.form.get('rent_way')
    house_type = request.form.get('house_type')
    direction_floor = request.form.get('direction_floor')
    floor = request.form.get('floor')
    parking = request.form.get('parking')
    electricity = request.form.get('electricity')
    heating = request.form.get('heating')
    check_in = request.form.get('check_in')
    elevator = request.form.get('elevator')
    water = request.form.get('water')
    gas = request.form.get('gas')
    pictures = request.files.getlist('pictures')

    #保存图片到项目静态文件路径下
    root_dir = os.getcwd()
    path = os.path.join(root_dir,'lianjia','static','images')
    if(not os.path.exists(path)):
        os.makedirs(path)
    path = os.path.join(path,id)
    if(not os.path.exists(path)):
        os.makedirs(path)
    i = 1
    for pic in pictures:
        pic.save(os.path.join(path, str(i) + '.jpg'))
        i=i+1

    db.addHouse(id,info,area,location,size,direction,rooms,price,rent_way,house_type,direction_floor,floor,parking,electricity,heating,check_in,elevator,water,gas,len(pictures))
    return render_template(
        'manage_house.html',
        houseInfo_list = db.getHouseInfo()
    )

#获取所有房源信息，用于填充房源管理页面修改房源中的信息
@app.route('/getHouseAllInfo',methods=['GET','POST'])
def getHouseAllInfo():
   id = request.form.get('id')
   return jsonify(db.getHouseAllInfo(id))

#房源信息修改模块，
@app.route('/modify_house', methods=['Get','Post'])
def modify_house():

    id = request.form.get('id')
    info = request.form.get('info')
    area = request.form.get('area')
    location = request.form.get('location')
    size = request.form.get('size')
    direction = request.form.get('direction')
    rooms = request.form.get('rooms')
    price = request.form.get('price')
    rent_way = request.form.get('rent_way')
    house_type = request.form.get('house_type')
    direction_floor = request.form.get('direction_floor')
    floor = request.form.get('floor')
    parking = request.form.get('parking')
    electricity = request.form.get('electricity')
    heating = request.form.get('heating')
    check_in = request.form.get('check_in')
    elevator = request.form.get('elevator')
    water = request.form.get('water')
    gas = request.form.get('gas')

    db.updateHouseInfo(id,info,area,location,size,direction,rooms,price,rent_way,house_type,direction_floor,floor,parking,electricity,heating,check_in,elevator,water,gas)
    return redirect(url_for('manage_house'))

#房源删除模块
@app.route('/remove_house', methods=['Get','Post'])
def remove_house():
    id = request.form.get('houseID')
    db.removeHouse(id)
    return redirect(url_for('manage_house'))

#用户投诉模块
@app.route('/complaint',methods=['GET','POST'])
def complaint():
   words = request.form.get('words')
   db.setComplaint(session['phoneNum'],words)
   return jsonify("投诉成功！")

#管理员查看所有用户投诉模块
@app.route('/getComplaint',methods=['GET','POST'])
def getComplaint():
   return render_template(
        'complaint.html',
         complaints = db.getComplaint()
   )