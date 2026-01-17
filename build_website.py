import pandas as pd
from gtts import gTTS
import os
import json
import re
from datetime import datetime

# --- 配置設定 ---
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'
SEO_FOLDER = 'seo_pages'  # 存放靜態 SEO 頁面的資料夾

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
    <meta name="description" content="免費多國語言學習單字卡，涵蓋英語、日語、韓語等12種語言。{title}">
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
            <p>
                <a href="about.html">關於我們</a> | 
                <a href="privacy.html">隱私權政策 (Privacy Policy)</a> | 
                <a href="contact.html">聯絡我們</a>
            </p>
        </footer>
    </div>
</body>
</html>
"""

# --- 主要邏輯 ---

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("🚀 App Builder Started...")

    # 0. 準備資料夾
    if not os.path.exists(SEO_FOLDER):
        os.makedirs(SEO_FOLDER)

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ File not found: {EXCEL_FILE}"); return

    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[COL_ID, COL_CN])
    except Exception as e:
        print(f"❌ Excel Error: {e}"); return

    js_data_list = []
    
    # 用來收集 SEO 頁面資料
    categories = {} # { '飲食': [rows...], '交通': [rows...] }

    print("🔄 Processing Data & Audio...")
    
    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        main_cat = row.get(COL_CAT_MAIN, "Uncategorized")
        
        # 收集分類資料供 SEO 使用
        if main_cat not in categories:
            categories[main_cat] = []
        categories[main_cat].append(row)

        item_data = {
            "id": row.get(COL_ID),
            "category": main_cat,
            "subcategory": row.get(COL_CAT_SUB),
            "cn": cn_text
        }

        # 處理各語言音檔
        for lang_key, config in LANG_MAP.items():
            target_col = config['col_name']
            raw_text = cn_text if target_col == COL_CN else row.get(target_col)

            if pd.isna(raw_text) or str(raw_text).strip() == "": continue

            text_for_audio = get_audio_text(str(raw_text), config['code'])
            
            # Phonetic logic
            phonetic_display = ""
            match = re.search(r'[\(（](.*?)[\)）]', str(raw_text))
            if match: phonetic_display = match.group(1).strip()

            file_name = safe_filename(text_for_audio) + ".mp3"
            
            base_folder = config['folder']
            target_folder = os.path.join(base_folder, AUDIO_SUBFOLDER)
            if not os.path.exists(target_folder): os.makedirs(target_folder)
            
            full_path = os.path.join(target_folder, file_name)
            
            # 音檔生成 (若不存在才生成，節省時間)
            if not os.path.exists(full_path):
                try:
                    tts = gTTS(text=text_for_audio, lang=config['code'])
                    tts.save(full_path)
                    # print(f"    Generated: {file_name}") # Optional log
                except: pass

            item_data[config['folder']] = {
                "word": str(raw_text),
                "phonetic": phonetic_display,
                "audio": file_name,
                "folder": f"{base_folder}/{AUDIO_SUBFOLDER}"
            }

        js_data_list.append(item_data)

    # 1. 輸出 data.js (給 App 使用)
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};")
    print("✅ data.js generated.")

    # 2. 生成 SEO 靜態頁面 (給 AdSense 使用)
    print("📄 Generating SEO Pages...")
    
    # 2.1 生成 sitemap.html (分類列表)
    sitemap_content = generate_html_header("所有學習分類列表", True)
    sitemap_content += """
    <div class="header text-center">
        <h1>📚 語言學習分類索引</h1>
        <p class="lead">選擇一個感興趣的主題，開始學習 12 種語言的對照單字！</p>
    </div>
    <div class="row">
    """
    
    for cat_name, rows in categories.items():
        safe_cat_name = safe_filename(cat_name)
        file_name = f"category_{safe_cat_name}.html"
        word_count = len(rows)
        sitemap_content += f"""
        <div class="col-md-4 mb-4">
            <div class="card h-100">
                <div class="card-body">
                    <h5 class="card-title">{cat_name}</h5>
                    <p class="card-text">包含 {word_count} 個常用單字與發音。</p>
                    <a href="{file_name}" class="btn btn-primary btn-sm">開始學習 &rarr;</a>
                </div>
            </div>
        </div>
        """
        
        # 2.2 生成 各別分類頁面 (category_xxx.html)
        cat_html = generate_html_header(f"{cat_name} - 單字表", True)
        cat_html += f"""
        <div class="header">
            <h1>📖 {cat_name} 相關單字 ({len(rows)}個)</h1>
            <p>本頁面整理了關於「{cat_name}」的常用多國語言單字。透過表格對照，您可以一次學習中文、英文、日文等多種語言的說法。這對於準備語言檢定或出國旅遊都非常有幫助。</p>
        </div>
        <div class="table-responsive vocab-table p-3">
            <table class="table table-hover table-bordered align-middle">
                <thead class="table-light">
                    <tr>
                        <th>中文 (Chinese)</th>
                        <th>英語 (English)</th>
                        <th>日語 (Japanese)</th>
                        <th>韓語 (Korean)</th>
                        <th>越語 (Vietnamese)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for row in rows:
            c_cn = row.get(COL_CN, "")
            c_en = row.get(LANG_MAP['英語']['col_name'], "")
            c_jp = row.get(LANG_MAP['日語']['col_name'], "")
            c_kr = row.get(LANG_MAP['韓語']['col_name'], "")
            c_vn = row.get(LANG_MAP['越語']['col_name'], "")
            
            cat_html += f"<tr><td>{c_cn}</td><td>{c_en}</td><td>{c_jp}</td><td>{c_kr}</td><td>{c_vn}</td></tr>"
            
        cat_html += "</tbody></table></div>"
        
        # 增加 SEO 文字
        cat_html += f"""
        <div class="mt-4 p-4 bg-light rounded">
            <h4>💡 學習小撇步</h4>
            <p>學習「{cat_name}」類的單字時，建議您搭配 FreeTalkEasy 的語音功能進行跟讀。每天練習 10 分鐘，可以有效提升長期記憶。</p>
        </div>
        """
        cat_html += generate_html_footer()
        
        with open(os.path.join(SEO_FOLDER, file_name), "w", encoding="utf-8") as f:
            f.write(cat_html)

    sitemap_content += "</div>"
    sitemap_content += generate_html_footer()
    with open(os.path.join(SEO_FOLDER, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    # 2.3 生成 必要政策頁面 (Privacy, About, Contact)
    # 這些是 AdSense 審核必看的
    pages = {
        "privacy.html": ("隱私權政策", "<h1>隱私權政策 (Privacy Policy)</h1><p>本網站 (FreeTalkEasy) 尊重您的隱私...</p><p>我們使用 LocalStorage 來儲存您的學習進度，這些資料僅存在於您的裝置上。</p><p>本網站使用 Google AdSense 顯示廣告，Google 及其合作夥伴可能會使用 Cookie 來根據您過往的瀏覽紀錄顯示廣告。</p>"),
        "about.html": ("關於我們", "<h1>關於 FreeTalkEasy</h1><p>FreeTalkEasy 是一個致力於降低語言學習門檻的開源專案。</p><p>我們的目標是提供簡單、直覺且免費的多國語言單字卡工具，幫助旅行者和語言愛好者快速掌握基礎詞彙。</p>"),
        "contact.html": ("聯絡我們", "<h1>聯絡我們</h1><p>如果您有任何建議或發現資料錯誤，歡迎透過以下方式聯繫開發團隊：</p><p>Email: contact@example.com (請自行替換)</p>")
    }
    
    for filename, (title, content) in pages.items():
        page_html = generate_html_header(title, True)
        page_html += f"<div class='p-4 bg-white rounded shadow-sm'>{content}</div>"
        page_html += generate_html_footer()
        with open(os.path.join(SEO_FOLDER, filename), "w", encoding="utf-8") as f:
            f.write(page_html)

    print(f"🎉 Build Complete! SEO Pages generated in '{SEO_FOLDER}/'")

if __name__ == "__main__":
    main()