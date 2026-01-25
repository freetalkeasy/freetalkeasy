import pandas as pd
import os
import sys

# --- 設定檔名 (請確認這裡跟您的檔名一致) ---
EXCEL_FILE = 'master_data.xlsx'

def check_excel():
    print(f"🔍 開始檢查檔案: {EXCEL_FILE}...\n")
    
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 找不到檔案！請確認 {EXCEL_FILE} 是否在同一個資料夾中。")
        return

    try:
        # 讀取所有分頁
        all_sheets = pd.read_excel(EXCEL_FILE, sheet_name=None, dtype=str)
        print(f"✅ 成功開啟檔案，共發現 {len(all_sheets)} 個分頁 (Worksheets)。\n")
        print("-" * 60)

        total_valid_rows = 0

        for sheet_name, df in all_sheets.items():
            print(f"📄 分頁名稱: [{sheet_name}]")
            
            # 1. 檢查欄位名稱 (顯示原始內容，包含空白)
            columns = df.columns.tolist()
            print(f"   👀 偵測到的欄位: {columns}")
            
            # 檢查是否有必要的欄位 (ID 和 中文)
            # 使用 strip() 來模擬程式碼的修正行為
            cleaned_cols = [str(c).strip() for c in columns]
            
            has_id = 'ID' in cleaned_cols
            has_cn = '中文' in cleaned_cols
            
            if has_id and has_cn:
                # 2. 檢查有效資料量
                # 模擬 build_website.py 的過濾邏輯
                df.columns = cleaned_cols # 暫時修正欄位名以進行檢查
                
                # 檢查是否有內容
                if df.empty:
                     print(f"   ⚠️ 狀態: 警告 (分頁是空的)")
                else:
                    # 嘗試過濾
                    valid_rows = df.dropna(subset=['ID', '中文'])
                    count = len(valid_rows)
                    total_valid_rows += count
                    
                    if count > 0:
                        print(f"   ✅ 狀態: 正常 (將會生成 {count} 筆單字)")
                        # 顯示前 1 筆資料確認一下
                        try:
                            first_id = valid_rows.iloc[0]['ID']
                            first_cn = valid_rows.iloc[0]['中文']
                            print(f"      範例: ID={first_id}, 中文={first_cn}")
                        except:
                            print("      (無法顯示範例資料)")
                    else:
                        print(f"   ⚠️ 狀態: 警告 (有欄位但沒有有效資料)")
                        print("      可能原因: ID 或 中文 欄位是空的")
            else:
                # 3. 診斷缺失原因
                print(f"   ❌ 狀態: **忽略 (不會讀取)**")
                missing = []
                if not has_id: missing.append("ID")
                if not has_cn: missing.append("中文")
                print(f"      缺少必要欄位: {missing}")
                print(f"      請檢查 Excel 第一列標題，是否打錯字或多了空白？")
            
            print("-" * 60)

        print(f"\n📊 總結: 預計總共會生成 {total_valid_rows} 個單字按鈕。")
        print("如果這個數字比您預期的少，請檢查上方標記為 ❌ 或 ⚠️ 的分頁。")

    except Exception as e:
        print(f"❌ 讀取時發生嚴重錯誤: {e}")
        print("建議：嘗試將 Excel 另存新檔，或是檢查是否加密。")

if __name__ == "__main__":
    try:
        check_excel()
    except Exception as e:
        print(f"程式發生未預期的錯誤: {e}")
    
    # --- 關鍵修正：讓視窗停下來 ---
    print("\n" + "="*30)
    input("執行完畢，請按 Enter 鍵離開視窗...")