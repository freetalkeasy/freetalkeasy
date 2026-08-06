@echo off
chcp 65001 >nul
echo ==========================================
echo [STEP 1] 準備上傳到 GitHub...
echo ==========================================

:: 1. 切換到正確目錄
cd /d "%~dp0"

:: 2. 先將雲端的更新拉下來合併 (解決 rejected 錯誤)
echo 🔄 正在與遠端 GitHub 同步...
git pull

:: 3. 加入檔案
echo 📦 正在加入所有檔案 (包含各語言資料夾內的新音檔)...
git add .

:: 4. 提交紀錄
echo 📝 正在建立提交紀錄...
set /p commit_msg="請輸入備註 (直接按 Enter 則預設為 Update content): "
if "%commit_msg%"=="" set commit_msg="Update content"
git commit -m %commit_msg%

:: 5. 上傳
echo ☁️ 正在上傳至 GitHub...
git push

echo ==========================================
echo ✅ 處理完成！如果沒看到紅色錯誤，代表上傳成功。
echo 請等待 1-2 分鐘，然後用手機無痕模式查看。
echo ==========================================
pause