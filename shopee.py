from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

print("開始")

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")

driver = webdriver.Chrome(options=options)

print("已連線 Chrome")

# 🔥 強制開新 tab（避免卡在 Gemini）
driver.switch_to.new_window("tab")

driver.get("https://shopee.tw/product/21092156/48504983081/")

#最大等待時間設定為15分鐘(900秒)，也就是可以讓你提前執行程式，掛著等待的緩衝時間。
#等"直接購買"avaliable後點選
def do():
    WebDriverWait(driver, 900).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='btn btn-solid-primary btn--l rvHxix']"))).click()
    print('------do')

#等"去買單"avaliable後點選，需強制睡一秒最順
def do2():
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='shopee-button-solid shopee-button-solid--primary']"))).click()
    print('-----do2')

