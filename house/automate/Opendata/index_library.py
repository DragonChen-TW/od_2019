import pandas as pd
import math as m

data_folder = 'static/csv/od/'

def calMedicalIndex(codebase):
    dir = data_folder + 'medical_data.csv'
    df = pd.read_csv(dir,encoding = "utf-8")
    result = df[df['CODEBASE']==codebase]

    #醫療院所數
    medical_score = 0
    if result['H_CNT'].values >= 7:
        medical_score += 1000
    elif result['H_CNT'].values >= 4:
        medical_score += 500
    elif result['H_CNT'].values >= 1:
        medical_score += 250

    #平均每千人擁有病床數 每個級距加乘20%點數
    if result['H_SRVB'].values >= 2000:
        medical_score += 400
    elif result['H_SRVB'].values >= 1500:
        medical_score += 300
    elif result['H_SRVB'].values >= 1000:
        medical_score += 200
    elif result['H_SRVB'].values >= 500:
        medical_score += 100
    elif result['H_SRVB'].values >= 200:
        medical_score += 40
    elif result['H_SRVB'].values >= 100:
        medical_score += 20
    elif result['H_SRVB'].values >= 50:
        medical_score += 10
    elif result['H_SRVB'].values >= 10:
        medical_score += 2

    return medical_score

def calculate_distance(lng1, lat1, lng2, lat2):
    # 將十進制度數轉化為弧度
    lng1, lat1, lng2, lat2 = map(m.radians, [lng1, lat1, lng2, lat2])
    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = m.sin(dlat/2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlng/2)**2
    c = 2 * m.asin(m.sqrt(a))
    r = 6371 # 地球平均半徑，單位為公里
    return c * r * 1000

def calFreewayIndex(lng,lat):
    min_distance = 9999999999
    freeway_score = 0
    freeway_exit_name = ''

    dir = data_folder + 'freeway_data.csv'
    freeway = pd.read_csv(dir,encoding = "utf-8")

    for i in range(len(freeway)):
        dist = calculate_distance(lng,lat,freeway['Lng'][i],freeway['Lat'][i])
        if dist < min_distance:
            min_distance = dist
            freeway_exit_name = freeway['Name'][i]

        #print(freeway['Name'][i],dist)
    print("\n最近交流道: {} --> {}(m)\n".format(freeway_exit_name,min_distance))

    #以KM設定分數
    if min_distance/1000 >= 10:
        freeway_score += 100
    elif min_distance/1000 >= 7:
        freeway_score += 300
    elif min_distance/1000 >= 5:
        freeway_score += 500
    elif min_distance/1000 >= 3:
        freeway_score += 700
    else:
        freeway_score += 900

    return freeway_score

def calMRTIndex(lng,lat):
    min_distance = 9999999999
    mrt_score = 0
    station_name = ''

    dir = data_folder + 'mrt_station_data.csv'
    mrt = pd.read_csv(dir,encoding = "utf-8")

    for i in range(len(mrt)):
        dist = calculate_distance(lng,lat,mrt['車站經度'][i],mrt['車站緯度'][i])
        if dist < min_distance:
            min_distance = dist
            station_name = mrt['車站中文名稱'][i]
        #print(mrt['車站中文名稱'][i],dist)
    print("\n最近捷運站: {} --> {}(m)\n".format(station_name,min_distance))

    #以KM設定分數
    if min_distance/1000 >= 10:
        mrt_score += 100
    elif min_distance/1000 >= 7:
        mrt_score += 300
    elif min_distance/1000 >= 5:
        mrt_score += 500
    elif min_distance/1000 >= 3:
        mrt_score += 700
    else:
        mrt_score += 900

    return mrt_score

def calLightRailIndex(lng,lat):
    min_distance = 9999999999
    light_rail_score = 0
    station_name = ''

    dir = data_folder + 'light_rail_station_data.csv'
    light_rail = pd.read_csv(dir,encoding = "utf-8")

    for i in range(len(light_rail)):
        dist = calculate_distance(lng,lat,light_rail['車站經度'][i],light_rail['車站緯度'][i])
        if dist < min_distance:
            min_distance = dist
            station_name = light_rail['車站中文名稱'][i]
        #print(mrt['車站中文名稱'][i],dist)
    print("\n最近輕軌站: {} --> {}(m)\n".format(station_name,min_distance))

    #以KM設定分數，輕軌站分數是捷運站一半
    if min_distance/1000 >= 10:
        light_rail_score += 50
    elif min_distance/1000 >= 7:
        light_rail_score += 150
    elif min_distance/1000 >= 5:
        light_rail_score += 250
    elif min_distance/1000 >= 3:
        light_rail_score += 350
    else:
        light_rail_score += 450

    return light_rail_score

def calPoliceIndex(lng,lat):
    min_distance = 9999999999
    police_score = 0
    police_station = ''

    dir = data_folder + 'police_result_data.csv'
    police_result_data = pd.read_csv(dir,encoding = "big5")

    for i in range(len(police_result_data)):
        dist = calculate_distance(lng,lat,police_result_data['Lng'][i],police_result_data['Lat'][i])
        if dist < min_distance:
            min_distance = dist
            police_station = police_result_data['中文單位名稱'][i]
        #print(mrt['車站中文名稱'][i],dist)
    print("\n最近警察局: {} --> {}(m)\n".format(police_station,min_distance))

    if min_distance/1000 >= 10:
        police_score += 100
    elif min_distance/1000 >= 7:
        police_score += 300
    elif min_distance/1000 >= 5:
        police_score += 500
    elif min_distance/1000 >= 3:
        police_score += 700
    else:
        police_score += 900

    return police_score

def search(lng, lat):
    stat_code = 'A6401-0025-00'

    lng = 120.259825
    lat = 22.6173789

    medical_score = calMedicalIndex(stat_code)
    # print("醫療分數: {}\n".format(medical_score))

    freeway_score = calFreewayIndex(lng,lat)
    # print("高速公路分數: {}".format(freeway_score))

    mrt_score = calMRTIndex(lng,lat)
    # print("捷運站分數: {}".format(mrt_score))

    light_rail_score = calLightRailIndex(lng,lat)
    # print("輕軌站分數: {}".format(light_rail_score))

    police_score = calPoliceIndex(lng,lat)
    # print("警察局分數: {}".format(police_score))

    return {
        'medical_score': medical_score,
        'freeway_score': freeway_score,
        'mrt_score': mrt_score,
        'light_rail_score': light_rail_score,
        'police_score': police_score
    }
