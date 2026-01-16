import pandas as pd
from gtts import gTTS
import os
import time
import json
import re

# ================= ⚙️ 設定區 =================
EXCEL_FILE = 'master_data.xlsx'
AUDIO_SUBFOLDER = 'audio'

COL_ID = 'ID'
COL_CAT_MAIN = '大分類'
COL_CAT_SUB = '子分類'
COL_CN = '中文' 

LANG_MAP = {
    '英語':   {'code': 'en',     'folder': 'CN_ENG', 'col_name': '英語'},
    '日語':   {'code': 'ja',     'folder': 'CN_JP',  'col_name': '日語'},
    '韓語':   {'code': 'ko',     'folder': 'CN_KR',  'col_name': '韓語'},
    '越語':   {'code': 'vi',     'folder': 'CN_VN',  'col_name': '越語'},
    '廣東':   {'code': 'yue',    'folder': 'CN_CON', 'col_name': '廣東'}, 
    '中文發音': {'code': 'zh-TW',  'folder': 'CN_ZH',  'col_name': COL_CN}
}
# ============================================

def get_audio_text(text, lang_code):
    """
    聰明的文字處理器：
    1. 如果是日語 (ja)：優先抓取括號內的文字來發音 -> '角 (かど)' 唸 'かど'
    2. 如果是其他語言：移除括號內的文字 -> 'Zero (0)' 唸 'Zero'
    """
    if not isinstance(text, str): return str(text)
    
    # 移除換行
    text = text.replace('\n', ' ').strip()

    # --- 🇯🇵 日語特殊邏輯 ---
    if lang_code == 'ja':
        # 找尋 (...) 或 （...） 裡面的內容
        match = re.search(r'[\(（](.*?)[\)）]', text)
        if match:
            # 如果有括號，就唸括號裡面的 (例如：かど)
            return match.group(1).strip()
        else:
            # 沒括號就直接唸
            return text
            
    # --- 🌍 其他語言邏輯 (維持原樣) ---
    else:
        # 移除括號及其內容
        text = re.sub(r'\(.*?\)', '', text)
        text = re.sub(r'（.*?）', '', text)
        return text.strip()

def safe_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", text).strip()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("🚀 程式啟動 (日語發音優化版)...")

    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到檔案: {EXCEL_FILE}")
        input("🔴 請按 Enter 鍵離開...")
        return

    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
    except PermissionError:
        print("❌ 錯誤：Excel 檔案正被開啟中！請關閉 Excel。")
        input("🔴 請按 Enter 鍵離開...")
        return
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
    print(f"📊 共 {len(df)} 筆資料，準備處理...\n")

    js_data_list = []
    audio_count = 0

    for index, row in df.iterrows():
        cn_text = row.get(COL_CN, "").strip()
        
        if index % 10 == 0: print(f"➡ 處理中: {cn_text} ...")

        item_data = {
            "id": row.get(COL_ID),
            "category": row.get(COL_CAT_MAIN),
            "subcategory": row.get(COL_CAT_SUB),
            "cn": cn_text
        }

        for lang_key, config in LANG_MAP.items():
            target_col = config['col_name']
            
            if target_col == COL_CN:
                raw_text = cn_text
            else:
                if target_col not in df.columns: continue
                raw_text = row.get(target_col)

            if pd.isna(raw_text) or str(raw_text).strip() == "": continue

            # === 關鍵修改點 ===
            # 使用新的函數來決定要唸什麼
            text_for_audio = get_audio_text(str(raw_text), config['code'])
            
            # 檔名使用唸出來的字 (例如 kado.mp3 或 かど.mp3)
            file_name = safe_filename(text_for_audio) + ".mp3"
            
            base_folder = config['folder']
            target_folder = os.path.join(base_folder, AUDIO_SUBFOLDER)
            
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            full_path = os.path.join(target_folder, file_name)

            # 產生音檔
            if not os.path.exists(full_path):
                try:
                    tts = gTTS(text=text_for_audio, lang=config['code'])
                    tts.save(full_path)
                    audio_count += 1
                    print(f"   ✅ 新增 ({lang_key}): {file_name}")
                except Exception as e:
                    print(f"   ❌ 失敗 {lang_key}: {e}")
                    pass

            web_folder = f"{base_folder}/{AUDIO_SUBFOLDER}"
            item_data[config['folder']] = {
                "word": str(raw_text), # 網頁顯示原始文字 (如：角 (かど))
                "audio": file_name,
                "folder": web_folder 
            }

        js_data_list.append(item_data)

    print("-" * 30)
    print("💾 正在寫入 data.js ...")
    js_content = f"const vocabData = {json.dumps(js_data_list, ensure_ascii=False, indent=4)};"
    
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print("="*30)
    print(f"🎉 全部完成！")
    print(f"🎉 新增音檔數: {audio_count}")
    
    input("\n✅ 請按 Enter 鍵關閉視窗...")

if __name__ == "__main__":
    main()