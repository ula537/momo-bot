from datetime import datetime
import time
import requests
from playwright.sync_api import sync_playwright

# ===== Telegram =====
TOKEN = "8183572724:AAH8H7-VQwfkQZm4DCCNiwaC9oAWt6E_3SQ"
CHAT_ID = "8806826310"

# ===== 商品網址 =====
PRODUCT_URL = "https://www.finders.com.tw/products/owala-freesip-tritan-25oz"

# ===== Telegram =====
def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# ===== 檢查庫存 =====
def check_stock():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(5000)

        html = page.content()

        browser.close()

        in_stock = (
            "加入購物車" in html
            and "售完" not in html
            and "貨到通知" not in html
        )

        return in_stock

# ===== 防止重複通知 =====
already_notified = False

print("開始監控 Owala 補貨...")

# ===== 固定檢查間隔 =====
CHECK_INTERVAL = 900  # 15分鐘

while True:

    start_time = time.time()

    try:

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{now}] 檢查中...")

        in_stock = check_stock()

        if in_stock:

            print(f"[{now}] 🔥 有貨！")

            if not already_notified:

                send_telegram(
                    f"🔥 Owala 補貨啦！\n\n"
                    f"時間：{now}\n"
                    f"{PRODUCT_URL}"
                )

                print("✅ 已發送 Telegram")

                already_notified = True

        else:

            print(f"[{now}] ❌ 沒貨")

            already_notified = False

    except Exception as e:

        print(f"[{now}] 錯誤：{e}")

    # ===== 精準等待 =====
    elapsed = time.time() - start_time

    sleep_time = max(0, CHECK_INTERVAL - elapsed)

    print(f"等待 {int(sleep_time)} 秒...\n")

    time.sleep(sleep_time)