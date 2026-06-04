import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

print("開始")

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress","127.0.0.1:9527")

driver = webdriver.Chrome(options=options)

driver.get("https://www.momoshop.com.tw")

print("已連線 Chrome")

url = "https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=13920118&Area=search&mdiv=403&oid=2_17&cid=index&kw=TAKARA+TOMY"
target_time = "23:26:00.000"

# ===== 預熱頁面 =====
print("🚀 開始預熱頁面")
driver.get(url)
time.sleep(1)

# ===== 重試點擊（核心）=====
def click(selector, timeout=5, retry=20):
    for i in range(retry):
        try:
            print(f"🔁 嘗試點擊 {selector} ({i+1}/{retry})")

            el = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )

            try:
                el.click()
            except:
                driver.execute_script("arguments[0].click();", el)

            print("✅ 點擊成功")
            return True

        except Exception as e:
            print("❌ 失敗:", e)
            time.sleep(0.05)

    print("❌ 最終點擊失敗")
    return False


# ===== 等待精準時間 =====
def wait_until(target):
    print("⏳ 等待時間:", target)

    while True:
        now = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        if now >= target:
            print("🔥 時間到")
            return

        time.sleep(0.001)  # 1ms busy wait（高精度）

# ===== 自動購買流程 =====
def autoBuy(url):
    driver.get(url)
    wait_until(target_time)

    # ⚠️ 以下 selector 可能會變（電商網站常改）
    click(".buynow")          # 直接購買
    click(".checkout-btn")    # 去結帳

# ===== 執行 =====
autoBuy("https://www.momoshop.com.tw/goods/GoodsDetail.jsp?i_code=13920118&Area=search&mdiv=403&oid=2_17&cid=index&kw=TAKARA+TOMY")