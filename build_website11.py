# ==========================================
# 🏠 網頁模板系統 (2026 專業升級版)
# ==========================================

def generate_html_header(title, is_subpage=False):
    path_prefix = "../" if is_subpage else "./"
    
    # 這是加入主畫面的引導區塊 (只在首頁顯示)
    app_prompt = ""
    if not is_subpage:
        app_prompt = """
        <div id="app-prompt" class="alert alert-info alert-dismissible fade show" role="alert">
            <strong>📱 將 FreeTalkEasy 加入主畫面！</strong><br>
            讓網站像 App 一樣快速開啟：<br>
            • <b>iPhone (Safari):</b> 點擊下方 <img src="https://img.icons8.com/ios/20/0d6efd/share-rounded.png"/> 分享按鈕，選擇「加入主畫面」。<br>
            • <b>Android (Chrome):</b> 點擊右上角「⋮」選單，選擇「加到主畫面」。
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FreeTalkEasy</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{{font-family:'Noto Sans TC',sans-serif;background-color:#f8f9fa;padding-top:20px}}
        .header{{margin-bottom:30px;border-bottom:1px solid #dee2e6;padding-bottom:20px}}
        .footer{{margin-top:50px;padding:40px 0;border-top:1px solid #eee;color:#6c757d;font-size:0.9rem;background-color:#fff}}
        .bmc-box{{text-align:center;margin-top:50px;padding:40px 20px;background-color:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05)}}
        a{{text-decoration:none;color:#0d6efd}}
    </style>
</head>
<body>
<div class="container">
    {app_prompt}
    <nav class="mb-4">
        <a href="{path_prefix}index.html">🏠 回到首頁</a> | 
        <a href="{path_prefix}seo_pages/sitemap.html">📚 分類列表</a>
    </nav>"""

def generate_html_footer(category_name="general"):
    """
    產生包含感性訴求、聯絡 Email 與贊助連結的頁尾
    """
    year = datetime.now().year
    bmc_id = "您的帳號ID" 
    tracking_id = f"freetalkeasy_{category_name}"
    contact_email = "tw.jeremy@gmail.com"

    # 感性訴求文字
    text_zh = "如果您覺得 <b>FreeTalkEasy</b> 幫您省下了大量整理資料與學習的時間，歡迎請我喝杯咖啡。您的每一份支持，都是我維持伺服器運作、持續擴充資料庫的動力。讓我們一起讓這個免費資源走得更遠，幫助更多語言學習者！"
    text_en = "If <b>FreeTalkEasy</b> has saved you valuable time in your learning journey, consider buying me a coffee! Your support helps cover server costs and fuels the continuous update of our database. Let’s keep this project alive and helpful for everyone together!"

    return f"""
    <div class="bmc-box">
        <p style="color:#333; font-size:1.1rem; line-height:1.6; margin-bottom:15px;">{text_zh}</p>
        <p style="color:#666; font-size:0.9rem; font-style:italic; margin-bottom:25px;">{text_en}</p>
        <a href="https://www.buymeacoffee.com/{bmc_id}?via={tracking_id}" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;">
        </a>
    </div>

    <footer class="footer text-center mt-5">
        <p>&copy; {year} FreeTalkEasy. 
            <a href="about.html">關於本站</a> | 
            <a href="mailto:{contact_email}">建議與回報</a> | 
            <a href="privacy.html">隱私政策</a>
        </p>
        <p class="small text-muted">聯絡信箱：{contact_email}</p>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</div>
</body>
</html>"""