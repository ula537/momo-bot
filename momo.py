from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ===== 建立 driver =====
driver = webdriver.Chrome()

driver.get("https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=15294216&ctype=B&sourcePageType=4")

while True:
    try:
        # 等待 buy_yes 出現
        buy = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "buy_yes"))
        )

        img = buy.find_element(By.TAG_NAME, "img")
        alt = img.get_attribute("alt")

        print("目前狀態:", alt)

        if "直接購買" in alt:
            print("🟢 有貨")
            break
        elif "開賣通知我" in alt:
            print("🟡 尚未開賣")
        elif "售完補貨中" in alt:
            print("🔴 已售完")
        else:
            print("⚠️ 未知狀態")

    except Exception as e:
        print("還不能購買 / 載入中")

    time.sleep(1)
    driver.refresh()