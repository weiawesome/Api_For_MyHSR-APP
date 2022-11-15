from flask import *
import time, json
import datetime
import random
import json
import socket
import struct
def proc(a,d=-1):
    b=[]
    r=1
    index=1
    for i in range(len(a)):
        if (a[i]=='{'):
            d+=1
        elif (a[i]=='}'):
            d-=1
        elif (a[i]=="'"):
            r*=-1
        if((r==1 and d==0 and a[i]==',') or i==len(a)-1):
            c=a[index:i]
            b.append([c[0:c.find(':')].strip()[1:-1],c[c.find(':')+1:].strip()[1:-1]])
            index=i+1
    return b

app = Flask(__name__)
chiness_weeksate = ['零', '一', '二', '三', '四', '五', '六', '日']


@app.route('/user/', methods=['GET'])
def request_page():
    user_query = str(request.args.get('user'))
    # print(user_query)
    data_set = {'Page': 'Request', 'Messege': f'Sucess got the request for {user_query}', 'Timestamp': time.time()}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/test/', methods=['POST'])
def test_page():
    HOST = '140.136.151.128'
    PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    input = request.get_json()
    start = input['StartStation']
    end = input['ArriveStation']
    oneway_return = input['OnewayReturn']
    gotime = input['StartTime']
    returntime = input['BackStartTime']
    traintype = input['Type']
    people = input['Tickets']
    prefer = input['Prefer']
    print(oneway_return)
    j = {
        "CommandType": "GetTrains",
        "StartStation": start,
        "ArriveStation": end,
        "OneWayReturn": 'True',
        "StartDate": gotime[0:10],
        "StartTime": gotime[16:],
        "BackStartDate": returntime[0:10],
        "BackStartTime": returntime[16:],
        "Type": traintype,
        "Prefer": prefer
    }
    HOST = '140.136.151.128'
    PORT = 10001

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    outdata = json.dumps(j)
    print(outdata)
    data = bytearray(outdata, "utf8")
    size = len(data)
    s.sendall(struct.pack("!H", size))
    s.sendall(data)
    print('has do it')
    indata = s.recv(1024)
    print(type(indata))
    a = indata.decode('unicode_escape')[2:]
    a = proc(a)
    print(a)
    ord,a[1][1]=(a[1][1][0:a[1][1].find(',')]).split(':'),a[1][1][a[1][1].find(',')+1:]
    print(ord[1].strip()[1:-1])
    atime,a[1][1]=(a[1][1][0:a[1][1].find(',')]),a[1][1][a[1][1].find(',')+1:]
    print(atime[atime.find(':')+1:].strip()[1:-4])
    sco,a[1][1]=(a[1][1][0:a[1][1].find(',')]),a[1][1][a[1][1].find(',')+1:]
    sb,a[1][1]=(a[1][1][0:a[1][1].find('0\'')]),a[1][1][a[1][1].find(',')+1:]
    sb=(sb[sb.find(':')+1:].strip()[1:-1]).split(',')
    for i in range(len(sb)):
        if(sb[i]=='00:00:00'):
            sb[i]=''
        else:
            sb[i]=sb[i][:5]
    print(sb)
    st,a[1][1]=(a[1][1][0:a[1][1].find(',')]),a[1][1][a[1][1].find(',')+1:]
    print(st[:5])
    datas=[]
    backdatas=[]
    for i in range(1):
        datas.append({'StartTime': st[:5], 'ArriveTime': atime[atime.find(':')+1:].strip()[1:-4], 'TotalTime': '2時 06分', 'Order': (ord[1].strip()[1:-1]),
                      'StationsBy': sb[:12]})
    ord,a[2][1]=(a[2][1][0:a[2][1].find(',')]).split(':'),a[2][1][a[2][1].find(',')+1:]
    print(ord[1].strip()[1:-1])
    atime,a[2][1]=(a[2][1][0:a[2][1].find(',')]),a[2][1][a[2][1].find(',')+1:]
    print(atime[atime.find(':')+1:].strip()[1:-4])
    sco,a[2][1]=(a[2][1][0:a[1][1].find(',')]),a[2][1][a[2][1].find(',')+1:]
    sb,a[2][1]=(a[2][1][0:a[1][1].find('0\'')]),a[2][1][a[2][1].find(',')+1:]
    sb=(sb[sb.find(':')+1:].strip()[1:-1]).split(',')
    for i in range(len(sb)):
        if(sb[i]=='00:00:00'):
            sb[i]=''
        else:
            sb[i]=sb[i][:5]
    print(sb)
    st,a[2][1]=(a[2][1][0:a[2][1].find(',')]),a[2][1][a[2][1].find(',')+1:]
    print(st[:5])
    for i in range(1):
        backdatas.append({'StartTime': st[:5], 'ArriveTime': atime[atime.find(':')+1:].strip()[1:-4], 'TotalTime': '2時 06分', 'Order': (ord[1].strip()[1:-1]),
                      'StationsBy': sb[:12]})
    retrundata = {
        'Price': (a[3][1]).split(','),
        'Datas': datas,
        'BackDatas': backdatas
    }
    json_dump = json.dumps(retrundata)
    return json_dump


@app.route('/edit/', methods=['POST'])
def edit_page():
    input = request.get_json()
    start = input['StartStation']
    end = input['ArriveStation']
    gotime = input['StartTime']
    traintype = input['Type']
    people = input['Tickets']

    Fees = []
    price = []
    for i in (people.split(',')):
        price.append(int(i) * 100)
        Fees.append(int(i) * 10)

    num = random.randint(0, 100)
    datas = []
    for i in range(num):
        datas.append({'StartTime': '10:34', 'ArriveTime': '11:40', 'TotalTime': '1時 06分', 'Order': '616',
                      'StationsBy': ['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']})
    num = random.randint(0, 100)
    retrundata = {
        'Price': price,
        'Datas': datas,
        'Fees': Fees
    }
    json_dump = json.dumps(retrundata)
    return json_dump


@app.route('/getlose/', methods=['POST'])
def getlose_page():
    input = request.get_json()
    ID=input['ID']
    BookID=input['BookID']

    retrundata = {
        'Status':'True',
        'StartStation':'左營',
        'ArriveStation':'板橋',
        'OnewayReturn':'True',
        'Type':'商務車廂',
        'Start':{
            'Date':'2022/10/13',
            'StartTime':'10:10',
            'ArriveTime':'12:00',
            'TotalTime':'1時5分',
            'Order':'987',
            'Seat':[['5車3A'],['3車4A','6車9A'],[],[],[]],
            'StationsBy':['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']
        },
        'Arrive':{
            'Date': '2022/10/13',
            'StartTime':'13:00',
            'ArriveTime':'15:00',
            'TotalTime':'2時0分',
            'Order':'987',
            'Seat': [['5車3A'], ['3車4A', '6車9A'], [], [], []],
            'StationsBy': ['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']
        },
        'Tickets':[1,2,0,0,0],
        'Prices':[100,200,0,0,0],
    }

    json_dump = json.dumps(retrundata)
    return json_dump

@app.route('/timetable/', methods=['POST'])
def timetable_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']

    num = random.randint(0, 100)
    datas = []
    for i in range(num):
        datas.append({'StartTime': '08:14', 'ArriveTime': '09:20', 'TotalTime': '1時 06分', 'Order': '999',
                      'StationsBy': ['21:30','21:41','21:50','22:05','22:17','','22:43','','','23:09','23:28','23:40']})
    retrundata = {
        'data': datas,
    }
    json_dump = json.dumps(retrundata)
    return json_dump


@app.route('/pay/', methods=['POST'])
def pay_page():
    input = request.get_json()
    BookID = input['BookID']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/use/', methods=['POST'])
def use_page():
    input = request.get_json()
    BookID = input['BookID']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/checkID/', methods=['POST'])
def check_page():
    input = request.get_json()
    Name = input['Name']
    Gender = input['Gender']
    ID = input['ID']
    Phone = input['Phone']
    Email = input['Email']
    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/findnow/', methods=['POST'])
def findnow_page():
    input = request.get_json()
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    Order = input['Order']
    ID = input['ID']
    num = random.randint(1, 5)
    datas = []
    for i in range(num):
        datas.append({'Code':'12345678','State':'False','DeadLine':'False'})
    num = random.randint(1, 5)
    for i in range(num):
        datas.append({'Code':'12345678','State':'True','DeadLine':'False'})
    data_set = {'Status': 'True','Datas':datas}
    json_dump = json.dumps(data_set)
    return json_dump

@app.route('/book/', methods=['POST'])
def book_page():
    input = request.get_json()
    Name = input['Name']
    Email = input['Email']
    StartDate = input['StartDate']
    BackDate = input['BackDate']
    Tickets = input['Tickets']
    Order = input['Order']
    BackOrder = input['BackOrder']
    StartStation = input['StartStation']
    ArriveStation = input['ArriveStation']
    StartTime = input['StartTime']
    ArriveTime = input['ArriveTime']
    BackStartTime = input['BackStartTime']
    BackArriveTime = input['BackArriveTime']
    Type = input['Type']

    seat = []
    backseat = []
    n = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    t = ['A', 'B', 'C', 'D', 'E']
    v = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    for i in Tickets.split(','):
        tmp = []
        for j in range(int(i)):
            s = ''
            s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
            tmp.append(s)
        seat.append(tmp)
    if (BackOrder != 'None'):
        for i in Tickets.split(','):
            tmp = []
            for j in range(int(i)):
                s = ''
                s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
                tmp.append(s)
            backseat.append(tmp)

    # 產生八碼編號
    n = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    result = ''
    for i in range(8):
        result += random.choice(n)
    data_set = {'Status': 'True', 'Result': result, 'Seat': seat, 'BackSeat': backseat}
    json_dump = json.dumps(data_set)

    return json_dump


@app.route('/editnow/', methods=['POST'])
def editnow_page():
    input = request.get_json()
    BookID=input['BookID']
    StartDate = input['StartDate']
    BackDate = input['BackDate']
    Order = input['Order']
    BackOrder = input['BackOrder']
    StartTime = input['StartTime']
    ArriveTime = input['ArriveTime']
    BackStartTime = input['BackStartTime']
    BackArriveTime = input['BackArriveTime']
    Tickets=input['Tickets']

    seat = []
    backseat = []
    n = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    t = ['A', 'B', 'C', 'D', 'E']
    v = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    for i in Tickets.split(','):
        tmp = []
        for j in range(int(i)):
            s = ''
            s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
            tmp.append(s)
        seat.append(tmp)
    if (BackOrder != 'None'):
        for i in Tickets.split(','):
            tmp = []
            for j in range(int(i)):
                s = ''
                s = random.choice(n) + '車' + '-' + random.choice(v) + random.choice(t)
                tmp.append(s)
            backseat.append(tmp)

    data_set = {'Status': 'True', 'Seat': seat, 'BackSeat': backseat}
    json_dump = json.dumps(data_set)

    return json_dump

@app.route('/refundnow/', methods=['POST'])
def refundnow_page():
    input = request.get_json()
    BookID=input['BookID']

    data_set = {'Status': 'True'}
    json_dump = json.dumps(data_set)

    return json_dump

@app.route('/time/', methods=['GET'])
def time_page():
    t = datetime.datetime.today()
    YMD = str(t.year) + '/' + str(t.month) + '/' + str(t.day)
    HM = str(t.hour) + ':' + str(t.minute)
    W = t.isoweekday()
    data_set = {'YMD': YMD, 'HM': HM, 'W': W}
    json_dump = json.dumps(data_set)
    return json_dump
