import os
import json
import pandas as pd  # 這是專門處理 Excel 的強大工具
from gtts import gTTS

# ================= 設定區 =================
excel_filename = "vietnam_data.xlsx"       # 您的 Excel 檔名
audio_folder = "vietnam_audio"     # 存放 MP3 的資料夾
js_filename = "data.js"            # 給網頁用的資料檔
# ==========================================

# 1. 準備路徑 (自動抓取桌面路徑)
# 為了保險起見，我們強制讓程式在「檔案所在的資料夾」運作
base_path = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.join(base_path, excel_filename)
folder_path = os.path.join(base_path, audio_folder)
js_path = os.path.join(base_path, js_filename)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 2. 讀取 Excel
print(f"📊 正在讀取 Excel: {excel_filename} ...")

try:
    # 讀取 Excel 檔案，並將所有內容轉為字串 (避免數字被當成浮點數)
    df = pd.read_excel(excel_path, dtype=str)
    
    # 去除空值 (如果有空行就刪掉)
    df = df.dropna(how='all') 
    
    # 將欄位名稱統一轉小寫，避免打錯 (例如 Category 變成 category)
    df.columns = df.columns.str.lower().str.strip()

    words_data = []
    existing_mp3s = set(os.listdir(folder_path))
    count = 0

    print("🚀 開始製作語音...")

    # 逐行處理 Excel 資料
    for index, row in df.iterrows():
        # 取得資料 (使用 .get 避免欄位是空的報錯)
        category = str(row.get('category', '未分類')).strip()
        vi_text = str(row.get('vietnamese', '')).strip()
        zh_text = str(row.get('chinese', '')).strip()

        # 如果越南文是空的，就跳過
        if not vi_text or vi_text.lower() == 'nan':
            continue

        # 檔名處理：去除特殊符號 (Windows 檔名不接受問號、斜線等)
        safe_filename = vi_text.replace(" ", "_").replace("?", "").replace("/", "").replace(":", "")
        safe_filename = safe_filename[:50] + ".mp3" # 限制檔名長度避免報錯

        # 加入資料清單
        words_data.append({
            "category": category,
            "vi": vi_text,
            "zh": zh_text,
            "file": safe_filename
        })

        # 檢查 MP3 是否已經存在
        if safe_filename not in existing_mp3s:
            print(f"🎙️ ({index+1}) 新增錄音: {vi_text}")
            try:
                tts = gTTS(text=vi_text, lang='vi')
                save_path = os.path.join(folder_path, safe_filename)
                tts.save(save_path)
            except Exception as e:
                print(f"⚠️ 錯誤: {vi_text} 轉檔失敗 - {e}")
        else:
            # print(f"⏩ 已存在跳過: {vi_text}") # 想看詳細可以把這行打開
            pass
        
        count += 1

    # 3. 輸出 data.js
    print("📝 正在寫入網頁資料庫...")
    js_content = f"const wordList = {json.dumps(words_data, ensure_ascii=False)};"
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print("-" * 30)
    print(f"✅ 大功告成！")
    print(f"共處理了 {len(words_data)} 筆資料")
    print(f"請直接打開 index.html 觀看成果")

except FileNotFoundError:
    print(f"❌ 錯誤：找不到 {excel_filename}")
    print("請確認 Excel 檔名是否正確，且跟程式放在同一個地方。")
except Exception as e:
    print(f"❌ 發生未預期的錯誤: {e}")
    print("提示：請確認 Excel 已經關閉 (不要開啟著執行程式)")