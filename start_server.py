import http.server
import socketserver
import webbrowser
import os

# 設定 Port (端口)
PORT = 8000

# 確保程式在當前目錄執行
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"伺服器已啟動: http://localhost:{PORT}")
        print("請按 Ctrl+C 停止伺服器")
        
        # 自動打開瀏覽器
        webbrowser.open(f"http://localhost:{PORT}")
        
        # 讓伺服器持續運行
        httpd.serve_forever()
except OSError as e:
    print(f"錯誤: Port {PORT} 可能被佔用了，請稍後再試或更換 Port。")
except KeyboardInterrupt:
    print("\n伺服器已停止。")