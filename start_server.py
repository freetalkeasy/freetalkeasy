import http.server
import socketserver
import socket
import os
import qrcode
import webbrowser

# ================= 設定區 =================
PORT = 8000 
# 👇 這裡是關鍵！我把您的路徑直接寫進去了
TARGET_PATH = r"C:\Users\jerem\Desktop\freetalkeasy"
# ==========================================

# 1. 強制切換到指定資料夾 (這是解決您問題的關鍵)
try:
    if os.path.exists(TARGET_PATH):
        os.chdir(TARGET_PATH)
        print(f"✅ 成功鎖定資料夾: {TARGET_PATH}")
    else:
        print(f"❌ 找不到資料夾: {TARGET_PATH}")
        print("請檢查路徑是否有字打錯？")
except Exception as e:
    print(f"❌ 切換路徑失敗: {e}")

# 2. 自動取得電腦 IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# 3. 準備網址
ip_address = get_ip()
url = f"http://{ip_address}:{PORT}"

print("="*40)
print(f"🚀 越南語學習伺服器啟動中...")
print(f"📂 目前讀取位置: {os.getcwd()}") # 再次確認目前位置
print(f"🏠 網址: {url}")
print("📱 請用手機掃描下方的 QR Code")
print("="*40)

# 4. 產生 QR Code
qr = qrcode.QRCode()
qr.add_data(url)
qr.print_ascii(invert=True) 

# 5. 自動開啟瀏覽器
webbrowser.open(url)

# 6. 啟動伺服器
Handler = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except OSError as e:
    print(f"⚠️ 啟動失敗: {e}")
    print("請嘗試關閉所有黑色視窗(CMD)後重試。")
except KeyboardInterrupt:
    print("\n伺服器已關閉。")