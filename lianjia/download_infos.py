from bs4 import BeautifulSoup
import requests
from urllib import request
import os
import lxml
from DB import DBmysql

db = DBmysql()

#获取房屋基本信息 返回列表 参数是想要获取的页数，一页三十条，默认为2页
def getHouseInfo(pages=1):
    divs = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    for i in range(1,pages+1):
        url = 'https://nj.lianjia.com/zufang/pg'+str(i)
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.content,'lxml')
        divs += soup.find_all('div',class_='content__list--item--main')

    return list(set(divs))

#获取每个房屋的基本信息
def getEachInfo(houseInfo):
    print(len(houseInfo))
    for house in houseInfo:
        url = house.find('p',class_='content__list--item--title twoline').find('a').get('href')
        info = house.find('p',class_='content__list--item--title twoline').find('a').get_text().strip()
        if info[0] == '独':
            continue
        infos = house.find('p','content__list--item--des').get_text().split('/')[0:4]
        info_list = [i.strip() for i in infos]
        price = house.find('em').get_text()
        if getHouseDetailInfo(url) == -1:
            continue
        db.setHouseInfo(url,info,info_list,price)
            

#获取房屋的详细信息
def getHouseDetailInfo(url):
    id = url.split('/')[2].split('.')[0]
    print(id)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    url = 'https://nj.lianjia.com' + url
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.content,'lxml')
    if not soup.find('ul', class_='piclist'):
        return -1
    #获取网页中对应的房源基本信息
    update_time = soup.find('div',class_='content__subtitle').get_text()[16:26]
    rent_way = soup.find('ul',class_='content__aside__list').find_all('li')[0].get_text()[5:]
    house_type = soup.find('ul',class_='content__aside__list').find_all('li')[1].get_text()[5:]
    direction_floor = soup.find('ul',class_='content__aside__list').find_all('li')[2].get_text()[5:]
    size = soup.find('div',class_='content__article__info').find_all('li')[1].get_text()[3:]
    floor = soup.find('div',class_='content__article__info').find_all('li')[7].get_text()[3:]
    parking = soup.find('div',class_='content__article__info').find_all('li')[10].get_text()[3:]
    electricity = soup.find('div',class_='content__article__info').find_all('li')[13].get_text()[3:]
    heating = soup.find('div',class_='content__article__info').find_all('li')[16].get_text()[3:]
    check_in = soup.find('div',class_='content__article__info').find_all('li')[5].get_text()[3:]
    elevator = soup.find('div',class_='content__article__info').find_all('li')[8].get_text()[3:]
    gas = soup.find('div',class_='content__article__info').find_all('li')[14].get_text()[3:]
    water = soup.find('div',class_='content__article__info').find_all('li')[11].get_text()[3:]
    imgurls = soup.find('ul', class_='piclist').find_all('img')
    
    db.setHouseDetailInfo(id,update_time,rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,gas,water,len(imgurls))
    #print(update_time,rent_way,house_type,direction_floor,size,floor,parking,electricity,heating,check_in,elevator,gas,water)
    #获取房间图片并保存到项目静态文件中
    root_dir = os.getcwd()
    path = os.path.join(root_dir,'lianjia','static','images')
    if(not os.path.exists(path)):
        os.makedirs(path)
    path = os.path.join(path,id)
    if(not os.path.exists(path)):
        os.makedirs(path)
    i = 1
    for imgurl in imgurls:
        src = imgurl.get('src')
        request.urlretrieve(src,os.path.join(path, str(i) + '.jpg'))
        i=i+1
    return 0


getEachInfo(getHouseInfo())
