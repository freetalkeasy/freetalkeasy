import pandas as pd
import os
import json
import re
import sys
import asyncio 
import edge_tts 
from datetime import datetime

# ==========================================
# 🧭 自動導航系統
# ==========================================
current_file_path = os.path.abspath(__file__)
correct_folder = os.path.dirname(current_file_path)
if os.path.exists(correct_folder):
    os.chdir(correct_folder)
    print(f"📂 工作目錄已鎖定: {correct_folder}")
else:
    print("❌ 路徑錯誤，請確認程式位置。")
    input("請按 Enter 鍵關閉視窗...")
    sys.exit()

# --- 設定區 ---
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'
SEO_FOLDER = 'seo_pages'
BMC_ID = "freetalkeasy"
CONTACT_EMAIL = "tw.jeremy@gmail.com"

COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文' 

# 語音對照表
LANG_MAP = {
    '英語': {'code': 'en', 'voice': 'en-US-AriaNeural', 'folder': 'CN_ENG', 'col_name': '英語'},
    '日語': {'code': 'ja', 'voice': 'ja-JP-NanamiNeural', 'folder': 'CN_JP', 'col_name': '日語'},
    '韓語': {'code': 'ko', 'voice': 'ko-KR-SunHiNeural', 'folder': 'CN_KR', 'col_name': '韓語'},
    '越語': {'code': 'vi', 'voice': 'vi-VN-HoaiMyNeural', 'folder': 'CN_VN', 'col_name': '越語'},
    '廣東': {'code': 'yue', 'voice': 'zh-HK-HiuGaaiNeural', 'folder': 'CN_CON', 'col_name': '廣東'}, 
    '法語': {'code': 'fr', 'voice': 'fr-FR-DeniseNeural', 'folder': 'CN_FR', 'col_name': '法語'},
    '德語': {'code': 'de', 'voice': 'de-DE-KatjaNeural', 'folder': 'CN_DE', 'col_name': '德語'},
    '西語': {'code': 'es', 'voice': 'es-ES-ElviraNeural', 'folder': 'CN_ES', 'col_name': '西語'},
    '俄語': {'code': 'ru', 'voice': 'ru-RU-SvetlanaNeural', 'folder': 'CN_RU', 'col_name': '俄語'},
    '泰語': {'code': 'th', 'voice': 'th-TH-PremwadeeNeural', 'folder': 'CN_TH', 'col_name': '泰語'},
    '印尼語': {'code': 'id', 'voice': 'id-ID-GadisNeural', 'folder': 'CN_ID', 'col_name': '印尼語'},
    '中文發音': {'code': 'zh-TW', 'voice': 'zh-TW-HsiaoChenNeural', 'folder': 'CN_ZH', 'col_name': COL_CN}
}

# --- 核心函式 ---

def get_audio_text(text, lang_code):
    if not isinstance(text, str): return str(text)
    text = text.replace('\n', ' ').strip()
    if lang_code == 'ja':
        match = re.search(r'[\(（](.*?)[\)）]', text)
        return match.group(1).strip() if match else text
    return re.sub(r'[\(（].*?[\)）]', '', text).strip()

def safe_filename(text):
    safe_text = re.sub(r'[\\/*?:"<>|]', "", text).strip().replace(" ", "_")
    reserved_words = {
        "CON", "PRN", "AUX", "NUL",
        "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
        "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    }
    if safe_text.upper() in reserved_words:
        safe_text += "_"
    return safe_text

async def generate_voice_file(text, voice_name, output_path):
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_path)
    except:
        pass

# --- HTML 生成 ---

def generate_html_header(title, is_subpage=False):
    path_prefix = "../" if is_subpage else "./"
    app_prompt = ""
    if not is_subpage:
        app_prompt = """<div id="app-prompt" class="alert alert-info alert-dismissible fade show shadow-sm mb-4" role="alert">
            <strong>📱 將 FreeTalkEasy 加入主畫面！</strong><br>
            讓網站像 App 一樣快速開啟，學習不間斷。
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FreeTalkEasy</title>
    <link rel="icon" href="{path_prefix}logo/logo.png" type="image/png" sizes="32x32">
    <link rel="apple-touch-icon" href="{path_prefix}logo/logo.png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{{font-family:'Noto Sans TC',sans-serif;background-color:#f8f9fa;padding-top:20px}}
        .container {{ max-width: 1200px; }}
        .bmc-box{{text-align:center;margin:50px auto;max-width:600px;padding:40px 20px;background-color:#fff;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05);border:1px solid #eee;}}
        .content-box {{background: white;padding: 30px;border-radius: 12px;box-shadow: 0 2px 4px rgba(0,0,0,0.05);margin-bottom: 20px;}}
        a{{text-decoration:none;color:#0d6efd}}
        .table-container {{background: white;padding: 30px;border-radius: 12px;box-shadow: 0 2px 4px rgba(0,0,0,0.05);margin-bottom: 20px;}}
    </style>
</head>
<body>
<div class="container">
    {app_prompt}
    <nav class="mb-4"><a href="{path_prefix}index.html">🏠 回到首頁</a> | <a href="{path_prefix}seo_pages/sitemap.html">📚 分類列表</a></nav>"""

def generate_html_footer(cat_name="general"):
    year = datetime.now().year
    return f"""
    <div class="bmc-box">
        <p>如果您覺得 <b>FreeTalkEasy</b> 幫您省下了時間，歡迎請我喝杯咖啡 ☕</p>
        <a href="https://www.buymeacoffee.com/{BMC_ID}" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" style="height: 60px !important;"></a>
    </div>
    <footer class="text-center mt-5"><p>&copy; {year} FreeTalkEasy. <a href="about.html">關於</a> | <a href="privacy.html">隱私</a></p></footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script></div></body></html>"""

# --- 主程式 ---
def main():
    print(f"🚀 啟動 Builder (v12.3 視窗防閃退版)...")
    if not os.path.exists(SEO_FOLDER): os.makedirs(SEO_FOLDER)
    
    # 1. 讀取 Excel
    print(f"📂 讀取 Excel 中...")
    try:
        if EXCEL_FILE.endswith('.csv'):
            df = pd.read_csv(EXCEL_FILE, dtype=str)
        else:
            df = pd.concat(pd.read_excel(EXCEL_FILE, sheet_name=None, dtype=str).values(), ignore_index=True)
        
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[COL_ID, COL_CN])
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        print("⚠️  請檢查：")
        print("   1. Excel 檔案是否已經關閉？")
        print("   2. 檔案名稱是否正確？")
        input("🔴 請按 Enter 鍵結束...")
        return

    js_data_list = []
    seo_categories = {} 
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("🔄 開始處理資料 (請耐心等待)...")

    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        main_cat = row.get(COL_CAT_MAIN, "Uncategorized")
        sub_cat = str(row.get(COL_CAT_SUB, "")).strip()
        if sub_cat == "nan": sub_cat = ""

        if main_cat not in seo_categories: seo_categories[main_cat] = []
        seo_categories[main_cat].append(row)

        item_data = {"id": row.get(COL_ID), "category": main_cat, "subcategory": sub_cat, "cn": cn_text}

        for lang_key, config in LANG_MAP.items():
            target_col = config['col_name']
            if target_col not in df.columns: continue
            raw_text = cn_text if target_col == COL_CN else row.get(target_col)
            if pd.isna(raw_text) or str(raw_text).strip() == "": continue

            text_audio = get_audio_text(str(raw_text), config['code'])
            fname = safe_filename(text_audio) + ".mp3"
            fpath = os.path.join(config['folder'], AUDIO_SUBFOLDER, fname)
            
            if not os.path.exists(os.path.dirname(fpath)): os.makedirs(os.path.dirname(fpath))

            if not os.path.exists(fpath):
                try:
                    loop.run_until_complete(generate_voice_file(text_audio, config['voice'], fpath))
                except: pass

            item_data[config['folder']] = {"word": str(raw_text), "audio": fname, "folder": f"{config['folder']}/{AUDIO_SUBFOLDER}"}

        js_data_list.append(item_data)

    # 2. 存檔 data.js
    print("💾 儲存 data.js ...")
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};")

    # 3. 頁面更新
    print("📄 更新頁面...")
    
    # Sitemap
    sitemap = generate_html_header("網站地圖", True) + '<div class="content-box"><h1 class="text-center">📚 分類列表</h1><div class="list-group">'
    for cat, rows in seo_categories.items():
        s_cat = safe_filename(str(cat))
        c_html = generate_html_header(f"{cat}", True) + f'<div class="table-container"><h1>{cat}</h1><table class="table"><tbody>'
        for r in rows: c_html += f'<tr><td>{r.get(COL_CN,"")}</td><td>{r.get("英語","")}</td></tr>'
        c_html += '</tbody></table></div>' + generate_html_footer(cat)
        with open(os.path.join(SEO_FOLDER, f"category_{s_cat}.html"), "w", encoding="utf-8") as f: f.write(c_html)
        sitemap += f'<a href="category_{s_cat}.html" class="list-group-item">{cat} <span class="badge bg-primary rounded-pill">{len(rows)}</span></a>'
    sitemap += '</div></div>' + generate_html_footer("sitemap")
    with open(os.path.join(SEO_FOLDER, "sitemap.html"), "w", encoding="utf-8") as f: f.write(sitemap)

    # About / Privacy
    about = generate_html_header("關於本站", True) + '<div class="content-box"><h1>關於 FreeTalkEasy</h1><p>免費語言學習平台。</p></div>' + generate_html_footer("about")
    with open(os.path.join(SEO_FOLDER, "about.html"), "w", encoding="utf-8") as f: f.write(about)
    privacy = generate_html_header("隱私權政策", True) + '<div class="content-box"><h1>隱私權政策</h1><p>本站使用 Cookie 與 GA4。</p></div>' + generate_html_footer("privacy")
    with open(os.path.join(SEO_FOLDER, "privacy.html"), "w", encoding="utf-8") as f: f.write(privacy)

    print("🎉 全部完成！")
    input("🟢 請按 Enter 鍵關閉視窗...")

if __name__ == "__main__":
    main()