@echo off
echo ==========================================
echo [STEP 1] Preparing to upload...
echo ==========================================

:: 1. 切換到正確目錄
cd /d "%~dp0"

:: 2. 加入檔案
echo Adding files...
git add .

:: 3. 提交紀錄
echo Committing changes...
set /p commit_msg="Enter message (Press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update content
git commit -m "%commit_msg%"

:: 4. 上傳
echo Uploading to GitHub...
git push

echo ==========================================
echo [SUCCESS] Upload Complete! 
echo Please wait 1-2 minutes for the update.
echo ==========================================
pause