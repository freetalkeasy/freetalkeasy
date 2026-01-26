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
    sys.exit()

# --- 配置設定 ---
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'
SEO_FOLDER = 'seo_pages'

BMC_ID = "freetalkeasy"
CONTACT_EMAIL = "tw.jeremy@gmail.com"

COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文' 

# ==========================================
# 🎤 微軟 Edge TTS 語音對照表
# ==========================================
LANG_MAP = {
    '英語': {'code': 'en', 'voice': 'en-US-AriaNeural', 'folder': 'CN_ENG', 'col_name': '英語', 'flag': '🇺🇸'},
    '日語': {'code': 'ja', 'voice': 'ja-JP-NanamiNeural', 'folder': 'CN_JP', 'col_name': '日語', 'flag': '🇯🇵'},
    '韓語': {'code': 'ko', 'voice': 'ko-KR-SunHiNeural', 'folder': 'CN_KR', 'col_name': '韓語', 'flag': '🇰🇷'},
    '越語': {'code': 'vi', 'voice': 'vi-VN-HoaiMyNeural', 'folder': 'CN_VN', 'col_name': '越語', 'flag': '🇻🇳'},
    '廣東': {'code': 'yue', 'voice': 'zh-HK-HiuGaaiNeural', 'folder': 'CN_CON', 'col_name': '廣東', 'flag': '🇭🇰'}, 
    '法語': {'code': 'fr', 'voice': 'fr-FR-DeniseNeural', 'folder': 'CN_FR', 'col_name': '法語', 'flag': '🇫🇷'},
    '德語': {'code': 'de', 'voice': 'de-DE-KatjaNeural', 'folder': 'CN_DE', 'col_name': '德語', 'flag': '🇩🇪'},
    '西語': {'code': 'es', 'voice': 'es-ES-ElviraNeural', 'folder': 'CN_ES', 'col_name': '西語', 'flag': '🇪🇸'},
    '俄語': {'code': 'ru', 'voice': 'ru-RU-SvetlanaNeural', 'folder': 'CN_RU', 'col_name': '俄語', 'flag': '🇷🇺'},
    '泰語': {'code': 'th', 'voice': 'th-TH-PremwadeeNeural', 'folder': 'CN_TH', 'col_name': '泰語', 'flag': '🇹🇭'},
    '印尼語': {'code': 'id', 'voice': 'id-ID-GadisNeural', 'folder': 'CN_ID', 'col_name': '印尼語', 'flag': '🇮🇩'},
    '中文發音': {'code': 'zh-TW', 'voice': 'zh-TW-HsiaoChenNeural', 'folder': 'CN_ZH', 'col_name': COL_CN, 'flag': '🇹🇼'}
}

# --- 輔助函式 ---
def get_audio_text(text, lang_code):
    if not isinstance(text, str): return str(text)
    text = text.replace('\n', ' ').strip()
    if lang_code == 'ja':
        match = re.search(r'[\(（](.*?)[\)）]', text)
        return match.group(1).strip() if match else text
    else:
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'（.*?）', '', text)
        return text.strip()

def safe_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", text).strip().replace(" ", "_")

async def generate_voice_file(text, voice_name, output_path):
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        await communicate.save(output_path)
    except Exception as e:
        print(f"   ⚠️ 下載失敗 (請檢查網路): {text} -> {e}")

# ==========================================
# 🏠 網頁模板系統
# ==========================================
def generate_html_header(title, is_subpage=False):
    path_prefix = "../" if is_subpage else "./"
    
    app_prompt = ""
    if not is_subpage:
        app_prompt = """
        <div id="app-prompt" class="alert alert-info alert-dismissible fade show shadow-sm mb-4" role="alert">
            <strong>📱 將 FreeTalkEasy 加入主畫面！</strong><br>
            讓網站像 App 一樣快速開啟，學習不間斷。
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FreeTalkEasy</title>
    
    <link rel="icon" href="{path_prefix}logo/logo.png" type="image/png" sizes="32x32">
    <link rel="icon" href="{path_prefix}logo/logo.png" type="image/png" sizes="192x192">
    <link rel="apple-touch-icon" href="{path_prefix}logo/logo.png">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{{font-family:'Noto Sans TC',sans-serif;background-color:#f8f9fa;padding-top:20px}}
        .container {{ max-width: 1200px; }}
        .header{{margin-bottom:30px;border-bottom:1px solid #dee2e6;padding-bottom:20px}}
        .footer{{margin-top:50px;padding:40px 0;border-top:1px solid #eee;color:#6c757d;font-size:0.9rem;background-color:#fff}}
        
        .bmc-box{{
            text-align:center;
            margin: 50px auto; 
            max-width: 600px;  
            padding: 40px 20px;
            background-color:#fff;
            border-radius:12px;
            box-shadow:0 2px 10px rgba(0,0,0,0.05); 
            border:1px solid #eee;
        }}
        
        a{{text-decoration:none;color:#0d6efd}}
        
        .table-container, .content-box {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }}
        h1 {{ color: #2c3e50; font-weight: bold; margin-bottom: 20px; }}
    </style>
</head>
<body>
<div class="container">
    {app_prompt}
    <nav class="mb-4">
        <a href="{path_prefix}index.html">🏠 回到首頁 (Home)</a> | 
        <a href="{path_prefix}seo_pages/sitemap.html">📚 分類列表</a>
    </nav>"""

def generate_html_footer(category_name="general"):
    year = datetime.now().year
    tracking_id = f"freetalkeasy_{category_name}"

    text_zh = "如果您覺得 <b>FreeTalkEasy</b> 幫您省下了大量整理資料與學習的時間，歡迎請我喝杯咖啡。您的每一份支持，都是我維持伺服器運作、持續擴充資料庫的動力。"
    text_en = "If <b>FreeTalkEasy</b> has saved you valuable time, consider buying me a coffee! Your support fuels the continuous update of our database."

    return f"""
    <div class="bmc-box">
        <p style="color:#333; font-size:1.1rem; line-height:1.6; margin-bottom:15px;">{text_zh}</p>
        <p style="color:#666; font-size:0.9rem; font-style:italic; margin-bottom:25px;">{text_en}</p>
        <a href="https://www.buymeacoffee.com/{BMC_ID}?via={tracking_id}" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;">
        </a>
    </div>

    <footer class="footer text-center mt-5">
        <p>&copy; {year} FreeTalkEasy. 
            <a href="about.html">關於本站</a> | 
            <a href="mailto:{CONTACT_EMAIL}">建議與回報</a> | 
            <a href="privacy.html">隱私政策</a>
        </p>
        <p class="small text-muted">聯絡信箱：{CONTACT_EMAIL}</p>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</div>
</body>
</html>"""

# --- 主要邏輯 ---
def main():
    print(f"🚀 FreeTalkEasy Builder 啟動 (BMC ID: {BMC_ID})")

    if not os.path.exists(SEO_FOLDER): os.makedirs(SEO_FOLDER)
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到 {EXCEL_FILE}"); return

    print(f"📂 正在讀取 Excel，請稍候...")
    try:
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, dtype=str)
        df_list = []
        for sheet_name, sheet_df in all_sheets.items():
            sheet_df.columns = sheet_df.columns.str.strip()
            # 自動過濾掉沒有 ID 的空行
            if COL_ID in sheet_df.columns and COL_CN in sheet_df.columns:
                df_list.append(sheet_df)
        
        if not df_list: print("❌ Excel 檔沒有有效資料"); return
        df = pd.concat(df_list, ignore_index=True)
        df.columns = df.columns.str.strip()
        # 強制過濾空行
        df = df.dropna(subset=[COL_ID, COL_CN])
        
        # 顯示總數
        total_items = len(df)
        print(f"✅ 成功讀取資料，共發現 {total_items} 個單字。")
        
    except Exception as e:
        print(f"❌ Excel 讀取失敗，請確認檔案是否已關閉: {e}"); return

    js_data_list = []
    seo_categories = {} 
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("🔄 開始處理資料與生成音檔 (如單字量大請耐心等待)...")

    # 遍歷每一行 (加入計數器)
    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        main_cat = row.get(COL_CAT_MAIN, "Uncategorized")
        sub_cat = str(row.get(COL_CAT_SUB, "")).strip()
        if sub_cat == "nan": sub_cat = ""

        # 顯示進度
        if index % 5 == 0:
            print(f"   ⏳ 正在處理第 {index + 1}/{total_items} 筆: {cn_text} ...")

        if main_cat not in seo_categories: seo_categories[main_cat] = []
        seo_categories[main_cat].append(row)

        item_data = {
            "id": row.get(COL_ID), 
            "category": main_cat, 
            "subcategory": sub_cat,
            "cn": cn_text
        }

        # 處理多國語言音檔
        for lang_key, config in LANG_MAP.items():
            target_col = config['col_name']
            if target_col not in df.columns: continue
            
            raw_text = cn_text if target_col == COL_CN else row.get(target_col)
            if pd.isna(raw_text) or str(raw_text).strip() == "": continue

            text_for_audio = get_audio_text(str(raw_text), config['code'])
            file_name = safe_filename(text_for_audio) + ".mp3"
            target_folder = os.path.join(config['folder'], AUDIO_SUBFOLDER)
            if not os.path.exists(target_folder): os.makedirs(target_folder)
            
            full_path = os.path.join(target_folder, file_name)
            
            # 只有當檔案不存在時才生成 (避免重複下載)
            if not os.path.exists(full_path):
                try:
                    print(f"      🎙️ [新] 正在生成 {lang_key} 音檔: {text_for_audio}")
                    loop.run_until_complete(generate_voice_file(text_for_audio, config['voice'], full_path))
                except Exception as e:
                    print(f"      ❌ {lang_key} 生成失敗: {e}")

            item_data[config['folder']] = {"word": str(raw_text), "audio": file_name, "folder": f"{config['folder']}/{AUDIO_SUBFOLDER}"}

        js_data_list.append(item_data)

    # 輸出 data.js
    print(f"💾 正在儲存 data.js ...")
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};")

    # 更新 SEO 分類頁面
    print("📄 更新分類頁面...")
    for cat_name, rows in seo_categories.items():
        safe_cat = safe_filename(str(cat_name))
        file_name = f"category_{safe_cat}.html"
        
        cat_html = generate_html_header(f"{cat_name}", True)
        cat_html += f'<h1 class="my-4">{cat_name}</h1>'
        cat_html += '<div class="table-container"><table class="table table-bordered table-striped"><tbody>'
        for row in rows:
            c_cn = row.get(COL_CN,""); c_en = row.get(LANG_MAP['英語']['col_name'],"")
            cat_html += f'<tr><td>{c_cn}</td><td>{c_en}</td></tr>'
        cat_html += '</tbody></table></div>'
        cat_html += generate_html_footer(cat_name)
        with open(os.path.join(SEO_FOLDER, file_name), "w", encoding="utf-8") as f: f.write(cat_html)

    # 生成 Sitemap
    print("🗺️ 正在建立 Sitemap (目錄頁)...")
    sitemap_html = generate_html_header("網站地圖", True)
    sitemap_html += '<div class="content-box" style="max-width:800px; margin:0 auto;">'
    sitemap_html += '<h1 class="my-4 text-center">📚 所有分類列表</h1>'
    sitemap_html += '<div class="list-group">'
    for cat_name in seo_categories.keys():
        safe_cat = safe_filename(str(cat_name))
        file_name = f"category_{safe_cat}.html"
        count = len(seo_categories[cat_name])
        sitemap_html += f'<a href="{file_name}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">{cat_name} <span class="badge bg-primary rounded-pill">{count}</span></a>'
    sitemap_html += '</div></div>'
    sitemap_html += generate_html_footer("sitemap")
    with open(os.path.join(SEO_FOLDER, "sitemap.html"), "w", encoding="utf-8") as f: f.write(sitemap_html)

    # 生成 About
    print("ℹ️ 正在建立 About 頁面...")
    about_html = generate_html_header("關於本站", True)
    about_html += """
    <div class="content-box">
        <h1>關於 FreeTalkEasy</h1>
        <p class="lead">讓語言學習變得簡單、直覺、無負擔。</p>
        <hr>
        <p>FreeTalkEasy 是一個專注於提供高品質、免費語言學習資源的平台。</p>
        <h3>我們的特色</h3>
        <ul><li>✨ 完全免費</li><li>🎧 真人發音</li><li>📱 跨平台支援</li></ul>
    </div>
    """
    about_html += generate_html_footer("about")
    with open(os.path.join(SEO_FOLDER, "about.html"), "w", encoding="utf-8") as f: f.write(about_html)

    # 生成 Privacy
    print("🔒 正在建立 Privacy 頁面...")
    privacy_html = generate_html_header("隱私權政策", True)
    privacy_html += """
    <div class="content-box">
        <h1>隱私權政策 (Privacy Policy)</h1>
        <p>我們重視您的隱私，本網站使用 Google Analytics 與 Cookie 來優化學習體驗。</p>
    </div>
    """
    privacy_html += generate_html_footer("privacy")
    with open(os.path.join(SEO_FOLDER, "privacy.html"), "w", encoding="utf-8") as f: f.write(privacy_html)

    print(f"🎉 全部完成！請執行 update_site.bat 上傳更新。")

if __name__ == "__main__":
    main()