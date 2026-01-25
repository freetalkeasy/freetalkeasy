import os
from PIL import Image

def resize_image_for_logo(input_path, output_path, target_pixel_width=500):
    """
    將圖片調整為適合 Logo 的大小 (預設寬度 500px)，並優化檔案大小。
    """
    try:
        with Image.open(input_path) as img:
            # 1. 計算新的高度，保持比例
            aspect_ratio = img.height / img.width
            new_height = int(target_pixel_width * aspect_ratio)
            
            # 2. 調整解析度 (Resizing)
            # 使用 LANCZOS 濾鏡保持高品質縮小
            resized_img = img.resize((target_pixel_width, new_height), Image.Resampling.LANCZOS)
            
            # 3. 儲存圖片
            # optimize=True 會在保持品質的前提下盡量減少檔案大小
            resized_img.save(output_path, optimize=True, quality=85)
            
            print(f"成功！圖片已儲存至: {output_path}")
            print(f"新尺寸: {target_pixel_width}x{new_height}")

    except Exception as e:
        print(f"處理失敗: {e}")

# --- 使用範例 ---
# 請將 'earth.png' 改為您下載下來的圖片檔名
source_file = 'earth.png' 
output_file = 'earth_logo_small.png'

# 設定您要的寬度 (網頁 Logo 通常不需要太大，建議 200-500px 即可)
# 如果您指的 "1M" 是 100萬畫素，那寬度大約設為 1000
resize_image_for_logo(source_file, output_file, target_pixel_width=500)