import pandas as pd
import os
import json
import re
import sys
import asyncio # 用來執行 Edge TTS 的非同步功能
import edge_tts # 微軟語音套件
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

COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文' 

# ==========================================
# 🎤 微軟 Edge TTS 語音對照表 (神經網路真人語音)
# ==========================================
# 這裡指定了每一種語言要使用哪個「聲優」
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

# 這是專門給 Edge TTS 用的生成函式 (非同步轉同步)
async def generate_voice_file(text, voice_name, output_path):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_path)

def generate_html_header(title, is_subpage=False):
    path_prefix = "../" if is_subpage else "./"
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{title}</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>body{{font-family:'Noto Sans TC',sans-serif;background-color:#f8f9fa;padding-top:20px}}.header{{margin-bottom:30px;border-bottom:1px solid #dee2e6;padding-bottom:20px}}.vocab-table{{background:white;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.05)}}.footer{{margin-top:50px;padding:20px 0;border-top:1px solid #eee;color:#6c757d;font-size:0.9rem}}a{{text-decoration:none;color:#0d6efd}}a:hover{{text-decoration:underline}}</style></head><body><div class="container"><nav class="mb-4"><a href="../index.html">🏠 回到首頁</a> | <a href="sitemap.html">📚 分類列表</a></nav>"""

def generate_html_footer():
    year = datetime.now().year
    return f"""<footer class="footer text-center"><p>&copy; {year} FreeTalkEasy. <a href="about.html">關於</a>|<a href="privacy.html">隱私</a>|<a href="contact.html">聯絡</a></p></footer></div></body></html>"""

# --- 主要邏輯 ---
def main():
    print("🚀 App Builder (Microsoft Edge TTS 版) 啟動...")
    print("✨ 這個版本使用微軟神經網路語音，品質更好且不易被封鎖！")

    if not os.path.exists(SEO_FOLDER): os.makedirs(SEO_FOLDER)
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到 {EXCEL_FILE}"); return

    print(f"📂 讀取 Excel 中...")
    try:
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, dtype=str)
        df_list = []
        for sheet_name, sheet_df in all_sheets.items():
            sheet_df.columns = sheet_df.columns.str.strip()
            if COL_ID in sheet_df.columns and COL_CN in sheet_df.columns:
                df_list.append(sheet_df)
        
        if not df_list: print("❌ Excel 檔沒有有效資料"); return
        df = pd.concat(df_list, ignore_index=True)
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[COL_ID, COL_CN])
        print(f"✅ 成功載入 {len(df)} 筆資料")
    except Exception as e:
        print(f"❌ Excel 讀取失敗: {e}"); return

    js_data_list = []
    seo_categories = {} 
    
    total_tasks = len(df) * len(LANG_MAP)
    current_step = 0
    generated_count = 0

    print("🔄 開始處理資料 (若遇壞檔會自動修復)...")
    
    # 建立事件迴圈來跑 Edge TTS
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        main_cat = row.get(COL_CAT_MAIN, "Uncategorized")
        if main_cat not in seo_categories: seo_categories[main_cat] = []
        seo_categories[main_cat].append(row)

        item_data = {
            "id": row.get(COL_ID),
            "category": main_cat,
            "subcategory": row.get(COL_CAT_SUB),
            "cn": cn_text
        }

        for lang_key, config in LANG_MAP.items():
            current_step += 1
            target_col = config['col_name']
            if target_col not in df.columns: continue
            
            raw_text = cn_text if target_col == COL_CN else row.get(target_col)
            if pd.isna(raw_text) or str(raw_text).strip() == "":
                item_data[config['folder']] = {"audio": None, "word": "", "phonetic": "", "folder": f"{config['folder']}/{AUDIO_SUBFOLDER}"}
                continue

            text_for_audio = get_audio_text(str(raw_text), config['code'])
            match = re.search(r'[\(（](.*?)[\)）]', str(raw_text))
            phonetic_display = match.group(1).strip() if match else ""

            file_name = safe_filename(text_for_audio) + ".mp3"
            base_folder = config['folder']
            target_folder = os.path.join(base_folder, AUDIO_SUBFOLDER)
            if not os.path.exists(target_folder): os.makedirs(target_folder)
            
            full_path = os.path.join(target_folder, file_name)
            
            # 壞檔檢查
            need_download = True
            if os.path.exists(full_path):
                if os.path.getsize(full_path) < 1000: # 壞檔
                    try: os.remove(full_path); print(f"🗑️ 刪除壞檔: {file_name}")
                    except: pass
                else:
                    need_download = False

            final_audio = None
            if need_download:
                try:
                    print(f"🎤 [{current_step}] Edge TTS 生成: {text_for_audio} ({config['voice']})")
                    # 呼叫微軟生成音檔
                    loop.run_until_complete(generate_voice_file(text_for_audio, config['voice'], full_path))
                    generated_count += 1
                except Exception as e:
                    print(f"⚠️ 生成失敗: {e}")
            
            if os.path.exists(full_path) and os.path.getsize(full_path) > 1000:
                final_audio = file_name

            item_data[config['folder']] = {
                "word": str(raw_text),
                "phonetic": phonetic_display,
                "audio": final_audio,
                "folder": f"{base_folder}/{AUDIO_SUBFOLDER}"
            }

        js_data_list.append(item_data)

    # 輸出 data.js
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};")
    print("\n✅ data.js 生成完畢！")

    # 更新 SEO 頁面 (簡化版)
    print("📄 更新 SEO 頁面...")
    sitemap_html = generate_html_header("分類列表", True) + '<div class="row">'
    for cat_name, rows in seo_categories.items():
        safe_cat = safe_filename(str(cat_name))
        file_name = f"category_{safe_cat}.html"
        sitemap_html += f'<div class="col-md-4 mb-4"><div class="card p-3"><h5>{cat_name}</h5><a href="{file_name}">前往學習 ({len(rows)})</a></div></div>'
        cat_html = generate_html_header(f"{cat_name}", True) + f'<h1>{cat_name}</h1><table class="table table-bordered"><tbody>'
        for row in rows:
            c_cn = row.get(COL_CN,""); c_en = row.get(LANG_MAP['英語']['col_name'],"")
            cat_html += f'<tr><td>{c_cn}</td><td>{c_en}</td></tr>'
        cat_html += '</tbody></table>' + generate_html_footer()
        with open(os.path.join(SEO_FOLDER, file_name), "w", encoding="utf-8") as f: f.write(cat_html)
    sitemap_html += '</div>' + generate_html_footer()
    with open(os.path.join(SEO_FOLDER, "sitemap.html"), "w", encoding="utf-8") as f: f.write(sitemap_html)
    
    for p in ['privacy.html', 'about.html', 'contact.html']:
        with open(os.path.join(SEO_FOLDER, p), "w", encoding="utf-8") as f: f.write(generate_html_header(p,True)+"<h1>Content</h1>"+generate_html_footer())

    print(f"🎉 全部完成！一共生成了 {generated_count} 個新音檔。")
    input("請按 Enter 鍵結束...")

if __name__ == "__main__":
    main()