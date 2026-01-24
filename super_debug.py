import pandas as pd
import os
import glob
import sys

def super_debug():
    print("==========================================")
    print("🕵️‍♂️ 超級偵探模式啟動...")
    print("==========================================\n")

    # 1. 告訴使用者程式現在在哪裡
    current_dir = os.getcwd()
    print(f"📂 程式目前所在的資料夾 (Working Directory):")
    print(f"   👉 {current_dir}\n")

    # 2. 列出這裡所有的檔案
    print(f"👀 程式在這個資料夾裡看到這些檔案:")
    files_in_dir = os.listdir(current_dir)
    if not files_in_dir:
        print("   (空空如也，這裡沒有任何檔案！)")
    else:
        for f in files_in_dir:
            print(f"   📄 {f}")
    print("-" * 40)

    # 3. 自動尋找任何 .xlsx 檔案
    excel_files = glob.glob("*.xlsx")

    if not excel_files:
        print("\n❌ 慘了！這裡完全找不到任何 .xlsx 結尾的 Excel 檔。")
        print("💡 解決辦法：")
        print("   1. 請確認您把 master_data.xlsx 放在上面顯示的那個資料夾裡。")
        print("   2. 或者，請把這個程式 (.py) 搬到 Excel 檔旁邊再執行一次。")
    else:
        # 抓第一個找到的 Excel 檔
        target_file = excel_files[0]
        print(f"\n✅ 太好了！找到一個 Excel 檔：【{target_file}】")
        print("🚀 現在嘗試讀取它的內容...\n")

        try:
            # 讀取所有分頁
            all_sheets = pd.read_excel(target_file, sheet_name=None, dtype=str)
            print(f"🎉 讀取成功！這個檔案有 {len(all_sheets)} 個分頁。\n")
            
            for sheet_name, df in all_sheets.items():
                print(f"   📄 分頁: [{sheet_name}]")
                # 清理欄位名稱
                df.columns = df.columns.str.strip()
                cols = df.columns.tolist()
                print(f"      欄位: {cols}")
                
                # 檢查 ID 和 中文
                if 'ID' in cols and '中文' in cols:
                    valid_count = len(df.dropna(subset=['ID', '中文']))
                    print(f"      ✅ 有效資料: {valid_count} 筆")
                else:
                    print(f"      ❌ 缺必要欄位 (ID 或 中文)")
                print("-" * 30)
                
        except Exception as e:
            print(f"❌ 雖然找到檔案，但讀取失敗：{e}")

    print("\n==========================================")

if __name__ == "__main__":
    try:
        super_debug()
    except Exception as e:
        print(f"程式發生錯誤: {e}")
    
    input("\n程式執行完畢，請按 Enter 鍵離開...")