import numpy as np
import pandas as pd
import requests, lxml
import os
from datetime import datetime
import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

PEOPLE_FOLDER = os.path.join('static', 'images/icons')

import os
def images(code):
    if(code=='800'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'clearsky.svg')
    elif(code=='801'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'fcloud.svg')
    elif(code=='802'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'scloud.svg')
    elif(code=='803' or code =='804'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'bcloud.svg')
    elif(code=='701' or code=='711' or code=='721' or code=='741' or code=='771'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'mist.svg')
    elif(code=='731' or code=='751' or code=='761' or code=='762' or code=='781'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'dust.svg')
    elif(code=='600' or code=='601' or code=='611' or code=='612' or code=='615' or code=='616' or code=='620' or code=='621'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'snow.svg')
    elif(code=='602' or code=='613' or code=='615' or code=='622'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'hsnow.svg')
    elif(code=='500' or code=='501' or code=='520' or code=='522' or code=='521'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'rain.svg')
    elif(code=='502' or code=='503' or code=='504' or code=='511' or code=='531'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'hrain.svg')
    elif(code=='300' or code=='301' or code=='302' or code=='310' or code=='311' or code=='312'or code=='313' or code=='314' or code=='321'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'drizzle.svg')
    elif(code=='210' or code=='211' or code=='212' or code=='221'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'thunder.svg')
    elif(code=='200' or code=='201' or code=='202' or code=='230' or code=='231' or code=='232'):
        image = os.path.join(app.config['UPLOAD_FOLDER'], 'rthunder.svg')
    
    return image

def getdata(url): 
    r = requests.get(url) 
    return r.text

def mytemp(loc):
    api_temp = "6668a2bd341d1aabd28a6f92a7eaf33c"
    other_link = "https://api.openweathermap.org/data/2.5/weather?q="+loc+"&appid="+api_temp
    other_link1 = requests.get(other_link)
    other_data = other_link1.json()
    t = str(round(other_data['main']['temp'] - 273.15)) + "°C"
    return t

def air(lat, lon):
    today = datetime.datetime.utcnow()
    end = datetime.datetime.utcnow()
    start = today - datetime.timedelta(hours=1)
    start1 = str(start.timestamp())
    end1 = str(end.timestamp())
    start = start1.split(".")[0]
    end = end1.split(".")[0]
    api = "5c85c89af95531169bff581a6d85ce44"
    alert_link = "http://api.openweathermap.org/data/2.5/air_pollution/history?lat="+lat+"&lon="+lon+"&start="+start+"&end="+end+"&appid="+api
    alert_api_link = requests.get(alert_link)
    alert_api_data = alert_api_link.json()
    main1 = alert_api_data["list"][0]['main']['aqi']
    main_list=['', 'Good', 'Fair', 'Moderate', 'Poor', 'Very Poor']
    main = main_list[main1]
    co = alert_api_data["list"][0]['components']['co']
    no = alert_api_data["list"][0]['components']['no']
    no2 = alert_api_data["list"][0]['components']['no2']
    o3 = alert_api_data["list"][0]['components']['o3']
    so2 = alert_api_data["list"][0]['components']['so2']
    pm2 = alert_api_data["list"][0]['components']['pm2_5']
    pm10 = alert_api_data["list"][0]['components']['pm10']
    nh3 = alert_api_data["list"][0]['components']['nh3']
    return main, co, no, no2, o3, so2, pm2, pm10, nh3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
@app.route('/')
def view():
    api = "822394f01306a89ed92a1896ee25a8ac"
    location = "Mumbai"
    link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api
    api_link = requests.get(link)
    api_data = api_link.json()
    name = api_data['name']
    temp = str(round(api_data['main']['temp'] - 273.15)) + "°C"
    max_temp = str(round(api_data['main']['temp_max'] - 273.15)) + "°C"
    pressure = str(api_data['main']['pressure']) + "hPa"
    speed = str(round(api_data['wind']['speed'] * 18/5)) + " km/h"
    deg = api_data['wind']['deg']
    val=int(round(deg / 45) % 8)
    arr=["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
    degree = arr[val]
    weather = api_data['weather'][0]['main']
    descrip = api_data['weather'][0]['description']
    humidity = str(api_data['main']['humidity']) + "%"
    cloud = str(api_data['clouds']['all']) + "%"
    code = str(api_data['weather'][0]['id'])
    image = images(code)

    min_list = []
    max_list = []
    id_list = []

    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])
    api_week = "2bd2e9278a2ae1d65db7c9f670aa69e5"
    weeklink= "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude=current,minutely,hourly,alerts&appid="+api_week
    week_link = requests.get(weeklink)
    week_data= week_link.json()

    for i in week_data['daily']:
        min_list.append(str(round(i['temp']['min']-273.15)) + "°C")
        max_list.append(str(round(i['temp']['max']-273.15)) + "°C")
        id_list.append(str(i['weather'][0]['id']))

    min1 = min_list[1]
    min2 = min_list[2]
    min3 = min_list[3]
    min4 = min_list[4]
    min5 = min_list[5]
    min6 = min_list[6]
    max1 = max_list[1]
    max2 = max_list[2]
    max3 = max_list[3]
    max4 = max_list[4]
    max5 = max_list[5]
    max6 = max_list[6]
    image1 = images(id_list[1])
    image2 = images(id_list[2])
    image3 = images(id_list[3])
    image4 = images(id_list[4])
    image5 = images(id_list[5])
    image6 = images(id_list[6])
    ln = mytemp("london")
    to = mytemp("tokyo")
    db = mytemp("dubai")
    ny = mytemp("new york")

    return render_template('index.html', name=name, temp=temp, max_temp=max_temp, cloud=cloud, pressure=pressure, speed=speed, humidity=humidity, degree=degree, weather=weather, descrip=descrip, image=image, min1=min1, min2=min2, min3=min3, min4=min4, min5=min5, min6=min6, max1=max1, max2=max2, max3=max3, max4=max4, max5=max5, max6=max6, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6, ln=ln, to=to, ny=ny, db=db)

@app.route('/home')
def home():
    api = "fe186690556a0bab85e59adf88c49fa4"
    location = "Mumbai"
    link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api
    api_link = requests.get(link)
    api_data = api_link.json()
    name = api_data['name']
    temp = str(round(api_data['main']['temp'] - 273.15)) + "°C"
    max_temp = str(round(api_data['main']['temp_max'] - 273.15)) + "°C"
    pressure = str(api_data['main']['pressure']) + "hPa"
    speed = str(round(api_data['wind']['speed'] * 18/5)) + " km/h"
    deg = api_data['wind']['deg']
    val=int(round(deg / 45) % 8)
    arr=["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
    degree = arr[val]
    weather = api_data['weather'][0]['main']
    descrip = api_data['weather'][0]['description']
    humidity = str(api_data['main']['humidity']) + "%"
    cloud = str(api_data['clouds']['all']) + "%"
    code = str(api_data['weather'][0]['id'])
    image = images(code)

    min_list = []
    max_list = []
    id_list = []

    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])
    api_week = "a7f80be97f5751f017b083c64e1cb77b"
    weeklink= "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude=current,minutely,hourly,alerts&appid="+api_week
    week_link = requests.get(weeklink)
    week_data= week_link.json()

    for i in week_data['daily']:
        min_list.append(str(round(i['temp']['min']-273.15)) + "°C")
        max_list.append(str(round(i['temp']['max']-273.15)) + "°C")
        id_list.append(str(i['weather'][0]['id']))

    min1 = min_list[1]
    min2 = min_list[2]
    min3 = min_list[3]
    min4 = min_list[4]
    min5 = min_list[5]
    min6 = min_list[6]
    max1 = max_list[1]
    max2 = max_list[2]
    max3 = max_list[3]
    max4 = max_list[4]
    max5 = max_list[5]
    max6 = max_list[6]
    image1 = images(id_list[1])
    image2 = images(id_list[2])
    image3 = images(id_list[3])
    image4 = images(id_list[4])
    image5 = images(id_list[5])
    image6 = images(id_list[6])
    ln = mytemp("london")
    to = mytemp("tokyo")
    db = mytemp("dubai")
    ny = mytemp("new york")

    return render_template('index.html', name=name, temp=temp, max_temp=max_temp, cloud=cloud, pressure=pressure, speed=speed, humidity=humidity, degree=degree, weather=weather, descrip=descrip, image=image, min1=min1, min2=min2, min3=min3, min4=min4, min5=min5, min6=min6, max1=max1, max2=max2, max3=max3, max4=max4, max5=max5, max6=max6, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6, ln=ln, to=to, ny=ny, db=db)

@app.route('/location', methods=['POST'])
def location():
    api = "af9cd16546be760826919a630c3d5de7"
    location = "Mumbai"
    if request.method == 'POST':
        location = request.form['wloc']

    link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api
    api_link = requests.get(link)
    api_data = api_link.json()
    name = api_data['name']
    temp = str(round(api_data['main']['temp'] - 273.15)) + "°C"
    max_temp = str(round(api_data['main']['temp_max'] - 273.15)) + "°C"
    pressure = str(api_data['main']['pressure']) + "hPa"
    speed = str(round(api_data['wind']['speed'] * 18/5)) + " km/h"
    deg = api_data['wind']['deg']
    val=int(round(deg / 45) % 8)
    arr=["North", "North East", "East", "South East", "South", "South West", "West", "North West"]
    degree = arr[val]
    weather = api_data['weather'][0]['main']
    descrip = api_data['weather'][0]['description']
    humidity = str(api_data['main']['humidity']) + "%"
    cloud = str(api_data['clouds']['all']) + "%"
    code = str(api_data['weather'][0]['id'])
    image = images(code)

    min_list = []
    max_list = []
    id_list = []

    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])
    api_week = "bc2ff0a13e20eeb4ddda5f360127ccfe"
    weeklink= "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&exclude=current,minutely,hourly,alerts&appid="+api_week
    week_link = requests.get(weeklink)
    week_data= week_link.json()

    for i in week_data['daily']:
        min_list.append(str(round(i['temp']['min']-273.15)) + "°C")
        max_list.append(str(round(i['temp']['max']-273.15)) + "°C")
        id_list.append(str(i['weather'][0]['id']))

    min1 = min_list[1]
    min2 = min_list[2]
    min3 = min_list[3]
    min4 = min_list[4]
    min5 = min_list[5]
    min6 = min_list[6]
    max1 = max_list[1]
    max2 = max_list[2]
    max3 = max_list[3]
    max4 = max_list[4]
    max5 = max_list[5]
    max6 = max_list[6]
    image1 = images(id_list[1])
    image2 = images(id_list[2])
    image3 = images(id_list[3])
    image4 = images(id_list[4])
    image5 = images(id_list[5])
    image6 = images(id_list[6])
    ln = mytemp("london")
    to = mytemp("tokyo")
    db = mytemp("dubai")
    ny = mytemp("new york")
    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])

    return render_template('index.html', name=name, temp=temp, max_temp=max_temp, pressure=pressure, cloud=cloud, speed=speed, humidity=humidity, degree=degree, weather=weather, descrip=descrip, image=image, min1=min1, min2=min2, min3=min3, min4=min4, min5=min5, min6=min6, max1=max1, max2=max2, max3=max3, max4=max4, max5=max5, max6=max6, image1=image1, image2=image2, image3=image3, image4=image4, image5=image5, image6=image6, ln=ln, to=to, ny=ny, db=db)

@app.route('/news')
def news():
    location = "Mumbai"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    q = location + " Weather"
    params = {
        "q": q,
        "hl": "en",
        "tbm": "nws",
	"tbs": "qdr:w"
    }

    response = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    news_dict = []
    c = 0
    for result in soup.select('.dbsr'):
        news  = {
            'title' : result.select_one('.nDgy9d').text,
            'link' : result.a['href'],
            'source' : result.select_one('.WF4CUc').text,
            'snippet' : result.select_one('.Y3v8qd').text,
            'date_published' : result.select_one('.WG9SHc span').text,
            }
        news_dict.append(news)
        c = c + 1
        if c==5:
            break

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    q1 = "Weather News Worldwide"
    params = {
        "q": q1,
        "hl": "en",
        "tbm": "nws",
    }

    response1 = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup1 = BeautifulSoup(response1.text, 'lxml')
    news_dict1 = []
    c = 0
    for result in soup1.select('.dbsr'):
        news  = {
            'title' : result.select_one('.nDgy9d').text,
            'link' : result.a['href'],
            }
        news_dict1.append(news)
        c = c + 1
        if c==6:
            break
    title = location.upper()

    url_img = "https://www.google.com/search?q="+location+"+weather&tbm=isch&ved=2ahUKEwjYhcrQ8OrxAhUmn0sFHTnzAIgQ2-cCegQIABAA&oq=mumbai+we&gs_lcp=CgNpbWcQARgAMgcIABCxAxBDMgQIABBDMgIIADIECAAQQzICCAAyAggAMgQIABBDMgIIADICCAAyAggAOgcIIxDqAhAnOgQIIxAnOggIABCxAxCDAToFCAAQsQM6CggAELEDEIMBEENQ8ypYsz9g43FoAXAAeACAAZoBiAHLCJIBAzAuOZgBAKABAaoBC2d3cy13aXotaW1nsAEKwAEB&sclient=img&ei=6DTzYNjxJaa-rtoPueaDwAg&bih=625&biw=1366&rlz=1C1SQJL_enIN920IN920"
    htmldata = getdata(url_img) 
    img_post = []
    soup = BeautifulSoup(htmldata, 'html.parser') 
    for item in soup.find_all("div", class_="NZWO1b"):
        post = {
            "link": 'https://www.google.com' + item.parent['href'],
            "src": item.findChild()['src'],
	    "name": item.parent.findNext('a').text.split('...')[1]
        }
        img_post.append(post)
    img_post1 = img_post[:6]
    return render_template('news.html', news_dict=news_dict, news_dict1=news_dict1, title=title, img_post1=img_post1)

@app.route('/loc', methods=['POST'])
def loc():
    location = "Mumbai"
    if request.method == 'POST':
        location = request.form['nloc']

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    q = location + " Weather"
    params = {
        "q": q,
        "hl": "en",
        "tbm": "nws",
	"tbs": "qdr:w"
    }

    response = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    news_dict = []
    c = 0
    for result in soup.select('.dbsr'):
        news  = {
            'title' : result.select_one('.nDgy9d').text,
            'link' : result.a['href'],
            'source' : result.select_one('.WF4CUc').text,
            'snippet' : result.select_one('.Y3v8qd').text,
            'date_published' : result.select_one('.WG9SHc span').text,
            }
        news_dict.append(news)
        c = c + 1
        if c==5:
            break

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    q1 = "Weather News Worldwide"
    params = {
        "q": q1,
        "hl": "en",
        "tbm": "nws",
    }

    response1 = requests.get("https://www.google.com/search", headers=headers, params=params)
    soup1 = BeautifulSoup(response1.text, 'lxml')
    news_dict1 = []
    c = 0
    for result in soup1.select('.dbsr'):
        news  = {
            'title' : result.select_one('.nDgy9d').text,
            'link' : result.a['href'],
            }
        news_dict1.append(news)
        c = c + 1
        if c==6:
            break
    title = location.upper()

    url_img = "https://www.google.com/search?q="+location+"+weather&tbm=isch&ved=2ahUKEwjYhcrQ8OrxAhUmn0sFHTnzAIgQ2-cCegQIABAA&oq=mumbai+we&gs_lcp=CgNpbWcQARgAMgcIABCxAxBDMgQIABBDMgIIADIECAAQQzICCAAyAggAMgQIABBDMgIIADICCAAyAggAOgcIIxDqAhAnOgQIIxAnOggIABCxAxCDAToFCAAQsQM6CggAELEDEIMBEENQ8ypYsz9g43FoAXAAeACAAZoBiAHLCJIBAzAuOZgBAKABAaoBC2d3cy13aXotaW1nsAEKwAEB&sclient=img&ei=6DTzYNjxJaa-rtoPueaDwAg&bih=625&biw=1366&rlz=1C1SQJL_enIN920IN920"
    htmldata = getdata(url_img) 
    img_post = []
    count = 0
    soup = BeautifulSoup(htmldata, 'html.parser') 
    for item in soup.find_all("div", class_="NZWO1b"):
        post = {
            "link": 'https://www.google.com' + item.parent['href'],
            "src": item.findChild()['src'],
	    "name": item.parent.findNext('a').text.split('...')[1]
        }
        img_post.append(post)
    img_post1 = img_post[:6]
    return render_template('news.html', news_dict=news_dict, news_dict1=news_dict1, title=title, img_post1=img_post1)

@app.route('/forecast')
def forecast():
    api = "3e2b05b56fdfe08ed5c5f48842deb49c"
    location = "Mumbai"
    link = "https://api.openweathermap.org/data/2.5/forecast?q="+location+"&appid="+api
    api_link = requests.get(link)
    api_data = api_link.json()
    lchart = [] 
    achart = []

    lchart.append(['Date', 'Minimum Temperature °C', 'Maximum Temperature °C', 'Feel Likes °C'])
    achart.append(['Date', "Cloudiness %", "Humidity %"])

    for item in api_data['list'] :
        date1 = datetime.datetime.utcfromtimestamp(item['dt']).strftime('%d/%m %H:%M')
        min_temp = item['main']['temp_min'] - 273.15
        max_temp = item['main']['temp_max'] - 273.15
        feel_temp = item['main']['feels_like'] - 273.15
        humidity = item['main']['humidity']
        pressure = item['main']['pressure']
        cloud = item['clouds']['all']
        sub_lchart = [date1, min_temp, max_temp, feel_temp]
        lchart.append(sub_lchart)
        sub_achart = [date1, humidity, cloud]
        achart.append(sub_achart)
    api1 = "b089c7e22e627eeb44935fb27630f2fd"
    link1 = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api1
    api_link = requests.get(link1)
    api_data = api_link.json()
    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])
    main, co, no, no2, o3, so2, pm2, pm10, nh3 = air(lat, lon)
    title=location.upper()
    return render_template('forecast.html', title=title, achart=achart, main=main, co=co, no=no, no2=no2, o3=o3, so2=so2, pm2=pm2, pm10=pm10, nh3=nh3, lchart=lchart)

@app.route('/forecasting', methods=['POST'])
def forecasting():
    api = "510103e66f3ee532466f4e769cde5e30"
    location = "Mumbai"
    if request.method == 'POST':
        location = request.form['floc']

    link = "https://api.openweathermap.org/data/2.5/forecast?q="+location+"&appid="+api
    api_link = requests.get(link)
    api_data = api_link.json()
    lchart = [] 
    achart = []

    lchart.append(['Date', 'Minimum Temperature °C', 'Maximum Temperature °C', 'Feel Likes °C'])
    achart.append(['Date', "Cloudiness %", "Humidity %"])

    for item in api_data['list'] :
        date1 = datetime.datetime.utcfromtimestamp(item['dt']).strftime('%d/%m %H:%M')
        min_temp = item['main']['temp_min'] - 273.15
        max_temp = item['main']['temp_max'] - 273.15
        feel_temp = item['main']['feels_like'] - 273.15
        humidity = item['main']['humidity']
        pressure = item['main']['pressure']
        cloud = item['clouds']['all']
        sub_lchart = [date1, min_temp, max_temp, feel_temp]
        lchart.append(sub_lchart)
        sub_achart = [date1, humidity, cloud]
        achart.append(sub_achart)
    api1 = "4487825811649567c15c5705bcf368c1"
    link1 = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api1
    api_link = requests.get(link1)
    api_data = api_link.json()
    lon = str(api_data['coord']['lon'])
    lat = str(api_data['coord']['lat'])
    main, co, no, no2, o3, so2, pm2, pm10, nh3 = air(lat, lon)
    title=location.upper()
    return render_template('forecast.html', title=title, achart=achart, main=main, co=co, no=no, no2=no2, o3=o3, so2=so2, pm2=pm2, pm10=pm10, nh3=nh3, lchart=lchart)

@app.route('/map')
def map():
    return render_template('weather.html')

if __name__ == "__main__":
    app.run()