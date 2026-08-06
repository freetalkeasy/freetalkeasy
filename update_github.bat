@echo off
chcp 65001 >nul
echo ==========================================
echo [STEP 1] 準備強制同步上傳到 GitHub...
echo ==========================================

:: 1. 切換到正確目錄
cd /d "%~dp0"

:: 2. 加入所有變更 (包含音檔和資料庫)
echo 📦 正在加入所有檔案...
git add .

:: 3. 提交紀錄
echo 📝 正在建立提交紀錄...
git commit -m "Force update all files to latest version"

:: 4. 強制覆蓋上傳 (這是關鍵！)
echo 🚀 正在強制覆蓋 GitHub 雲端檔案...
git push origin main --force

echo ==========================================
echo ✅ 強制上傳完成！
echo 請打開 GitHub 網頁檢查檔案修改時間是否已變成「剛剛」。
echo 接著等 1-2 分鐘，再用手機無痕模式查看網頁。
echo ==========================================
pause