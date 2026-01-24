import pandas as pd
from gtts import gTTS
import os
import json
import re
import sys
import time
from datetime import datetime

# ==========================================
# 🧭 自動導航系統：強制鎖定程式所在位置
# ==========================================
# 讓 Python 自動找到 master_data.xlsx，不管你在哪裡執行
current_file_path = os.path.abspath(__file__)
correct_folder = os.path.dirname(current_file_path)

if os.path.exists(correct_folder):
    os.chdir(correct_folder)
    print(f"📍 程式位置: {current_file_path}")
    print(f"📂 工作目錄已鎖定至: {correct_folder}")
else:
    print("❌ 路徑錯誤，無法定位資料夾。")
    sys.exit()

print("-" * 50)

# --- 配置設定 ---
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'
SEO_FOLDER = 'seo_pages'

# Excel 欄位對應
COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文' 

# 語言設定
LANG_MAP = {
    '英語': {'code': 'en', 'folder': 'CN_ENG', 'col_name': '英語', 'flag': '🇺🇸'},
    '日語': {'code': 'ja', 'folder': 'CN_JP', 'col_name': '日語', 'flag': '🇯🇵'},
    '韓語': {'code': 'ko', 'folder': 'CN_KR', 'col_name': '韓語', 'flag': '🇰🇷'},
    '越語': {'code': 'vi', 'folder': 'CN_VN', 'col_name': '越語', 'flag': '🇻🇳'},
    '廣東': {'code': 'yue', 'folder': 'CN_CON', 'col_name': '廣東', 'flag': '🇭🇰'}, 
    '法語': {'code': 'fr', 'folder': 'CN_FR', 'col_name': '法語', 'flag': '🇫🇷'},
    '德語': {'code': 'de', 'folder': 'CN_DE', 'col_name': '德語', 'flag': '🇩🇪'},
    '西語': {'code': 'es', 'folder': 'CN_ES', 'col_name': '西語', 'flag': '🇪🇸'},
    '俄語': {'code': 'ru', 'folder': 'CN_RU', 'col_name': '俄語', 'flag': '🇷🇺'},
    '泰語': {'code': 'th', 'folder': 'CN_TH', 'col_name': '泰語', 'flag': '🇹🇭'},
    '印尼語': {'code': 'id', 'folder': 'CN_ID', 'col_name': '印尼語', 'flag': '🇮🇩'},
    '中文發音': {'code': 'zh-TW', 'folder': 'CN_ZH', 'col_name': COL_CN, 'flag': '🇹🇼'}
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

def generate_html_header(title, is_subpage=False):
    path_prefix = "../" if is_subpage else "./"
    return f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FreeTalkEasy</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Noto Sans TC', sans-serif; background-color: #f8f9fa; padding-top: 20px; }}
        .header {{ margin-bottom: 30px; border-bottom: 1px solid #dee2e6; padding-bottom: 20px; }}
        .vocab-table {{ background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .footer {{ margin-top: 50px; padding: 20px 0; border-top: 1px solid #eee; color: #6c757d; font-size: 0.9rem; }}
        a {{ text-decoration: none; color: #0d6efd; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="mb-4">
            <a href="../index.html">🏠 回到首頁 (App)</a> | 
            <a href="sitemap.html">📚 所有分類列表</a>
        </nav>
"""

def generate_html_footer():
    year = datetime.now().year
    return f"""
        <footer class="footer text-center">
            <p>&copy; {year} FreeTalkEasy Project. All rights reserved.</p>
            <p><a href="about.html">關於我們</a> | <a href="privacy.html">隱私權政策</a></p>
        </footer>
    </div>
</body>
</html>
"""

# --- 主要邏輯 ---

def main():
    print("🚀 App Builder 啟動 (包含自動修復與防封鎖機制)...")

    # 0. 準備資料夾
    if not os.path.exists(SEO_FOLDER):
        os.makedirs(SEO_FOLDER)

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 錯誤：找不到檔案 {EXCEL_FILE}")
        return

    # --- 1. 讀取 Excel (全分頁讀取) ---
    print(f"📂 正在讀取 Excel: {EXCEL_FILE} ...")
    try:
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, dtype=str)
        
        df_list = []
        for sheet_name, sheet_df in all_sheets.items():
            # 清洗欄位 (去空白)
            sheet_df.columns = sheet_df.columns.str.strip()
            # 檢查必要欄位
            if COL_ID in sheet_df.columns and COL_CN in sheet_df.columns:
                df_list.append(sheet_df)
            else:
                print(f"   ⚠️ 跳過無效分頁: {sheet_name}")
            
        if not df_list:
            print("❌ Excel 檔沒有有效資料"); return
            
        df = pd.concat(df_list, ignore_index=True)
        
    except Exception as e:
        print(f"❌ Excel 讀取錯誤: {e}"); return

    # 清洗合併後的資料
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=[COL_ID, COL_CN])
    print(f"✅ 成功載入 {len(df)} 筆有效資料")
    print("-" * 50)

    js_data_list = []
    seo_categories = {} 
    
    # 統計進度用
    total_steps = len(df) * len(LANG_MAP)
    current_step = 0
    generated_count = 0
    skipped_count = 0

    print("🔄 開始處理資料與音檔 (請耐心等待)...")
    
    # --- 2. 處理每一行資料 ---
    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        main_cat = row.get(COL_CAT_MAIN, "Uncategorized")
        
        # 收集分類資料
        if main_cat not in seo_categories:
            seo_categories[main_cat] = []
        seo_categories[main_cat].append(row)

        item_data = {
            "id": row.get(COL_ID),
            "category": main_cat,
            "subcategory": row.get(COL_CAT_SUB),
            "cn": cn_text
        }

        # 處理各語言
        for lang_key, config in LANG_MAP.items():
            target_col = config['col_name']
            
            # 若 Excel 沒這欄位，直接跳過
            if target_col not in df.columns:
                current_step += 1
                continue

            raw_text = cn_text if target_col == COL_CN else row.get(target_col)

            # 空值檢查
            if pd.isna(raw_text) or str(raw_text).strip() == "":
                item_data[config['folder']] = {
                    "word": "",
                    "phonetic": "",
                    "audio": None,
                    "folder": f"{config['folder']}/{AUDIO_SUBFOLDER}"
                }
                current_step += 1
                continue

            text_for_audio = get_audio_text(str(raw_text), config['code'])
            
            phonetic_display = ""
            match = re.search(r'[\(（](.*?)[\)）]', str(raw_text))
            if match: phonetic_display = match.group(1).strip()

            file_name = safe_filename(text_for_audio) + ".mp3"
            
            base_folder = config['folder']
            target_folder = os.path.join(base_folder, AUDIO_SUBFOLDER)
            if not os.path.exists(target_folder): os.makedirs(target_folder)
            
            full_path = os.path.join(target_folder, file_name)
            
            # ==========================================
            # 🛡️ 核心機制：壞檔檢查與停等機制
            # ==========================================
            need_download = True
            
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                if file_size < 1000: # 小於 1KB 視為壞檔
                    try:
                        os.remove(full_path) # 刪除壞檔
                        print(f"🗑️ 自動修復壞檔: {file_name}")
                    except: pass
                    need_download = True
                else:
                    need_download = False # 檔案正常，跳過
                    skipped_count += 1

            final_audio = None
            
            if need_download:
                try:
                    # 顯示進度
                    print(f"🎤 [{current_step}/{total_steps}] 下載中: {text_for_audio} ({lang_key})...")
                    
                    tts = gTTS(text=text_for_audio, lang=config['code'])
                    tts.save(full_path)
                    generated_count += 1
                    
                    # ✅ 停等機制：成功後休息 1.5 秒
                    time.sleep(1.5)
                    
                except Exception as e:
                    print(f"⚠️ 下載失敗: {e}")
                    # ✅ 避險機制：如果是 429 (太多請求)，休息久一點
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        print("⏳ 觸發 Google 限制，暫停 20 秒冷卻...")
                        time.sleep(20)
            
            # 確認檔案最終狀態
            if os.path.exists(full_path) and os.path.getsize(full_path) > 1000:
                final_audio = file_name
            
            item_data[config['folder']] = {
                "word": str(raw_text),
                "phonetic": phonetic_display,
                "audio": final_audio,
                "folder": f"{base_folder}/{AUDIO_SUBFOLDER}"
            }
            
            current_step += 1

        js_data_list.append(item_data)

    print("-" * 50)
    print(f"📊 統計：跳過 {skipped_count} 個舊檔，新生成 {generated_count} 個檔案。")

    # 輸出 data.js
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};")
    print("✅ data.js 生成完畢！")

    # --- 3. 生成 SEO 靜態頁面 ---
    print("📄 更新 SEO 頁面...")
    
    sitemap_content = generate_html_header("所有學習分類列表", True)
    sitemap_content += """
    <div class="header text-center"><h1>📚 語言學習分類索引</h1></div>
    <div class="row">
    """
    
    for cat_name, rows in seo_categories.items():
        safe_cat_name = safe_filename(str(cat_name))
        file_name = f"category_{safe_cat_name}.html"
        sitemap_content += f"""
        <div class="col-md-4 mb-4"><div class="card h-100"><div class="card-body">
            <h5 class="card-title">{cat_name}</h5>
            <a href="{file_name}" class="btn btn-primary btn-sm">開始學習 ({len(rows)}) &rarr;</a>
        </div></div></div>
        """
        
        cat_html = generate_html_header(f"{cat_name}", True)
        cat_html += f'<div class="header"><h1>{cat_name} ({len(rows)})</h1></div>'
        cat_html += '<div class="table-responsive vocab-table p-3"><table class="table table-hover table-bordered"><thead><tr><th>中文</th><th>英語</th><th>日語</th></tr></thead><tbody>'
        
        for row in rows:
            c_cn = row.get(COL_CN, "")
            c_en = row.get(LANG_MAP['英語']['col_name'], "") if '英語' in LANG_MAP else ""
            c_jp = row.get(LANG_MAP['日語']['col_name'], "") if '日語' in LANG_MAP else ""
            cat_html += f"<tr><td>{c_cn}</td><td>{c_en}</td><td>{c_jp}</td></tr>"
            
        cat_html += "</tbody></table></div>" + generate_html_footer()
        with open(os.path.join(SEO_FOLDER, file_name), "w", encoding="utf-8") as f:
            f.write(cat_html)

    sitemap_content += "</div>" + generate_html_footer()
    with open(os.path.join(SEO_FOLDER, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    # 政策頁面
    for page in ['privacy.html', 'about.html', 'contact.html']:
        with open(os.path.join(SEO_FOLDER, page), "w", encoding="utf-8") as f:
            f.write(generate_html_header(page, True) + "<div class='p-4'><h1>Page Content</h1></div>" + generate_html_footer())

    print(f"🎉 全部執行完畢！")
    print("="*50)
    input("請按 Enter 鍵結束視窗...")

if __name__ == "__main__":
    main()