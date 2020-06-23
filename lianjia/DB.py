import pymysql

#数据库函数封装再类中，以类的形式调用
class DBmysql(object):
    """description of class"""
    
    #数据库初始化
    def __init__(self):
        self._db = pymysql.connect("localhost","root","root","test" )
        self._cursor = self._db.cursor()

    #获取客户登录所需信息
    def getUser(self,phone_num):
        data = None
        sql = 'select password, username, gender, age, alias from customer where phone_num = %s'
        try:
            self._cursor.execute(sql,[phone_num])
            data = self._cursor.fetchone()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data

    #获取所有管理员信息
    def getManager(self,phone_num):
        data = None
        sql = 'select password, username from manager where phone_num = %s'
        try:
            self._cursor.execute(sql,[phone_num])
            data = self._cursor.fetchone()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data

    #获取客户所有信息
    def getAllUser(self):
        data = None
        sql = 'select * from customer'
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data

    #添加新客户信息
    def setUser(self,phone_num,username,password,gender,age,alias):
        sql = "insert into customer values(%s,%s,%s,%s,%s,%s)"
        try:
            self._cursor.execute(sql,[phone_num,username,password,gender,age,alias])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #根据号码删除客户信息
    def delUser(self,phone_num):
        sql = "delete from customer where phone_num = %s"
        try:
            self._cursor.execute(sql,[phone_num])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #修改客户信息
    def updateUser(self,phoneNum,username,password,gender,age,alias):
        sql = "update customer set username = %s, password = %s, gender = %s, age = %s, alias = %s where phone_num = %s"
        try:
            self._cursor.execute(sql,[username,password,gender,age,alias,phoneNum])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)
    
    #管理员修改客户部分信息
    def modifyUser(self,phoneNum,username,gender,age,alias):
        sql = "update customer set username = %s, gender = %s, age = %s, alias = %s where phone_num = %s"
        try:
            self._cursor.execute(sql,[username,gender,age,alias,phoneNum])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #添加房源信息
    def setHouseInfo(self, url, info, info_list, price):
        id = url.split('/')[2].split('.')[0]
        area = info_list[0].split('-')[0]
        sql = 'insert into house_info values (%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self._cursor.execute(sql,[id,info,area,info_list[0],info_list[1],info_list[2],info_list[3],price])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #获取房源信息
    def getHouseInfo(self):
        data = []
        sql = 'select * from house_info'
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            print(e)
        return data

    #根据客户选择的条件来筛选房源信息
    def selectHouseInfo(self,area,rent_way,price,direction):
        data = []
        #写成这种形式是为了方便把前端传过来的条件语句拼接到sql语句中，当前端选择的是不限，传过来的就是空值，我们就以下面的形式占着一个位置
        #给你一个hint，自己再体会一下（：
        if area == '':
            area = ' area is not null '
        if rent_way == '':
            rent_way = ' rent_way is not null '
        if price == '':
            price = ' price is not null '
        if direction == '':
            direction = ' direction is not null '

        sql = 'select a.id,a.info,a.area,a.location,a.size,a.direction,a.rooms,a.price from house_info a join house_detail_info b on a.id = b.id'
        #默认的拼接顺序是 区域 ，出租方式， 价格， 方向
        sql += ' where ' + area + ' and ' + rent_way + ' and ' + price + ' and ' + direction
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            print(e)
        return data

    #获取房源所有区域
    def getHouseArea(self):
        data = []
        sql = 'select distinct area from house_info'
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            print(e)
        return data

    #添加房源详细信息
    def setHouseDetailInfo(self,id,update_time,rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,gas,water,image_nums):
        sql = 'insert into house_detail_info values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            self._cursor.execute(sql,[id,update_time,rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,water,gas,image_nums])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)
    
    #获取房源详细信息
    def getHouseDetailInfo(self,houseID):
        data = []
        sql = 'select a.id,a.info,a.price,b.update_time,b.rent_way,b.house_type,b.direction_floor,b.size,b.floor,b.parking,b.electricity,b.heating,b.check_in,b.elevator,b.water,b.gas,b.image_nums from house_info a join house_detail_info b on a.id = b.id where a.id = %s'
        try:
            self._cursor.execute(sql,[houseID])
            data = self._cursor.fetchall()
        except Exception as e:
            print(e)
        return data[0]

    #添加客户预约信息
    def reserve(self,phoneNum,houseID):
        sql = 'insert into reserve values (%s,%s)'
        try:
            self._cursor.execute(sql,[phoneNum,houseID])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)
    
    #获取所有预约信息
    def getAllReserveInfo(self):
        data = None
        sql = 'select * from reserve'
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data

    #根据房源ID 删除房源信息
    def removeHouse(self,houseID):
        sql = "delete house_info, house_detail_info from house_info left join house_detail_info on house_info.id = house_detail_info.id where house_info.id = %s"
        try:
            self._cursor.execute(sql,[houseID])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #管理员添加房源信息
    def addHouse(self,id,info,area,location,size,direction,rooms,price,rent_way,house_type,direction_floor,floor,parking,electricity,heating,check_in,elevator,water,gas,pics):
        sql = 'insert into house_info values (%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_detail = "insert into house_detail_info values (%s,date_format(now(),'%%Y-%%m-%%d'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            self._cursor.execute(sql,[id,info,area,location,size,direction,rooms,price])
            self._cursor.execute(sql_detail,[id,rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,water,gas,pics])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #获取所有房源信息
    def getHouseAllInfo(self,id):
        sql = "select a.id,a.info,a.area,a.location,a.size,a.direction,a.rooms,a.price,b.rent_way,b.house_type,b.direction_floor,b.floor,b.parking,b.electricity,b.heating,b.check_in,b.elevator,b.water,b.gas from house_info a join house_detail_info b on a.id = b.id where a.id = %s"
        try:
            self._cursor.execute(sql,[id])
            data = self._cursor.fetchall()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data[0]

    #修改房源信息
    def updateHouseInfo(self,id,info,area,location,size,direction,rooms,price,rent_way,house_type,direction_floor,floor,parking,electricity,heating,check_in,elevator,water,gas):
        sql = "update house_info set info=%s,area=%s,location=%s,size=%s,direction=%s,rooms=%s,price=%s where id=%s"
        sql_detail = "update house_detail_info set rent_way=%s,house_type=%s,direction_floor=%s,size=%s,floor=%s,parking=%s,electricity=%s,heating=%s,check_in=%s,elevator=%s,water=%s,gas=%s where id=%s"
        try:
            self._cursor.execute(sql,[info,area,location,size,direction,rooms,price,id])
            self._cursor.execute(sql_detail,[rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,water,gas,id])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #添加用户投诉
    def setComplaint(self,phoneNum,complaint):
        sql = 'insert into complaint values (%s,%s)'
        try:
            self._cursor.execute(sql,[phoneNum,complaint])
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(e)

    #获取所有客户投诉信息
    def getComplaint(self):
        data = None
        sql = 'select * from complaint'
        try:
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
        except Exception as e:
            self._db.rollback()
            print(e)
        return data
#db = DBmysql()
#print(db.getHouseInfo())





