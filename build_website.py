import pandas as pd
from gtts import gTTS
import os
import time
import json
import re

# ================= ⚙️ 設定區 =================
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'  # 新增：音檔要存放的子目錄名稱

COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文'

LANG_MAP = {
    '英語': {'code': 'en',     'folder': 'CN_ENG'},
    '日語': {'code': 'ja',     'folder': 'CN_JP'},
    '韓語': {'code': 'ko',     'folder': 'CN_KR'},
    '越語': {'code': 'vi',     'folder': 'CN_VN'},
    '廣東': {'code': 'zh-CN',  'folder': 'CN_CON'} 
}
# ============================================

def clean_text(text):
    if not isinstance(text, str): return str(text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'（.*?）', '', text)
    return text.replace('\n', ' ').strip()

def safe_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", text).strip()

def main():
    # 鎖定工作目錄
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("🚀 程式啟動 (音檔集中版)...")
    print(f"📂 工作目錄: {os.getcwd()}")

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到檔案: {EXCEL_FILE}")
        input("🔴 請按 Enter 鍵離開...")
        return

    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
    except Exception as e:
        print(f"❌ 讀取 Excel 失敗: {e}")
        input("🔴 請按 Enter 鍵離開...")
        return

    df.columns = df.columns.str.strip()
    
    if COL_ID not in df.columns or COL_CN not in df.columns:
        print(f"❌ 欄位錯誤，找不到 '{COL_ID}' 或 '{COL_CN}'")
        input("🔴 請按 Enter 鍵離開...")
        return

    df = df.dropna(subset=[COL_ID, COL_CN])
    print(f"📊 共 {len(df)} 筆資料，準備整理音檔到 '{AUDIO_SUBFOLDER}' 目錄...\n")

    js_data_list = []
    audio_count = 0

    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        
        item_data = {
            "id": row.get(COL_ID),
            "category": row.get(COL_CAT_MAIN),
            "subcategory": row.get(COL_CAT_SUB),
            "cn": cn_text
        }

        for lang_col, config in LANG_MAP.items():
            if lang_col not in df.columns: continue
            raw_text = row.get(lang_col)
            if pd.isna(raw_text) or str(raw_text).strip() == "": continue

            clean_word = clean_text(str(raw_text))
            file_name = safe_filename(clean_word) + ".mp3"
            
            # 1. 設定實體存檔路徑 (例如: CN_ENG/audio/)
            base_folder = config['folder']
            target_folder = os.path.join(base_folder, AUDIO_SUBFOLDER)
            
            # 確保資料夾存在
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
                print(f"   📁 建立目錄: {target_folder}")

            full_path = os.path.join(target_folder, file_name)

            # 2. 產生音檔
            if not os.path.exists(full_path):
                try:
                    tts = gTTS(text=clean_word, lang=config['code'])
                    tts.save(full_path)
                    audio_count += 1
                    print(f"   ✅ 新增: {target_folder}\\{file_name}")
                except Exception as e:
                    print(f"   ❌ 失敗: {e}")
                    time.sleep(1)

            # 3. 設定網頁用的路徑 (強制使用斜線 / 以符合網頁標準)
            web_folder = f"{base_folder}/{AUDIO_SUBFOLDER}"

            item_data[config['code']] = {
                "word": str(raw_text),
                "audio": file_name,
                "folder": web_folder 
            }

        js_data_list.append(item_data)

    # 輸出 data.js
    js_content = f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};"
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print("\n" + "="*30)
    print(f"🎉 整理完成！")
    print(f"   - 音檔已集中至各語言的 /{AUDIO_SUBFOLDER} 資料夾")
    print(f"   - 新增音檔: {audio_count}")
    print(f"   - data.js 路徑已更新")
    print("="*30)
    
    input("\n✅ 請按 Enter 鍵關閉視窗...")

if __name__ == "__main__":
    main()