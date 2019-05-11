from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.get('http://www.sunriver.com.tw/taiwanmap/grid_tm2_convert.php')
driver.maximize_window()
#driver.find_element_by_id('crsSource').click()
#time.sleep(1)