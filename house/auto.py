from selenium import webdriver
import time

def get_stat_code(lng, lat=None):
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open input location's field
    driver.get('https://semap.moi.gov.tw/STATViewer/Web/Map/STATViewer_Map.aspx')
    driver.find_element_by_id('Locate').click()

    time.sleep(1)
    driver.find_element_by_id('ui-id-12').click()
    driver.find_element_by_css_selector("label[for='LocateBox_Coord_WGS84']").click()

    res_list = []
    if not lat: # if input is list
        lnglat_list = lng
    else:
        lnglat_list = [(lng, lat)]

    for lng, lat in lnglat_list:
        lng = str(lng)
        lat = str(lat)
        driver.find_element_by_id('LocateBox_Coord_Work_WGS84_lng').clear()
        driver.find_element_by_id('LocateBox_Coord_Work_WGS84_lat').clear()
        driver.find_element_by_id('LocateBox_Coord_Work_WGS84_lng').send_keys(lng)
        driver.find_element_by_id('LocateBox_Coord_Work_WGS84_lat').send_keys(lat)
        driver.find_element_by_id('LocateBox_Coord_Work_WGS84_Locate').click()
        time.sleep(1)
        driver.find_element_by_css_selector("img[class='PointStatInfo']").click()

        # search
        time.sleep(1)
        res = driver.find_element_by_class_name('PointStatInfoBox_STUnitBts')
        tds = res.find_elements_by_tag_name('td')

        print('Loading {},{}'.format(lng, lat))
        while tds[1].text == '讀取中...':
            time.sleep(5)

        res_list.append({tds[i].text: tds[i + 1].text for i in range(0, len(tds), 2)})
    return res_list

if __name__ == '__main__':
    lnglat_list = [('120.269139', '22.621194'), ('121.4220826', '24.98953'), (121.42, 24.98)]
    print(get_stat_code(lnglat_list))
