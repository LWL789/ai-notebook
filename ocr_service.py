import os
import tempfile
from PIL import Image
import easyocr

# 初始化 easyocr（只加载中文和英文）
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

def ocr_image(image_file) -> str:
    try:
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            img = Image.open(image_file)
            img.save(tmp.name)
            tmp_path = tmp.name
        
        # 调用 easyocr 识别
        result = reader.readtext(tmp_path, detail=0)
        os.unlink(tmp_path)
        
        # 合并识别结果
        text = "\n".join(result)
        return text if text else "未识别到文字，请确认图片清晰"
    except Exception as e:
        return f"OCR识别失败: {str(e)}"