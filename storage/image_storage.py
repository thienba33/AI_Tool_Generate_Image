from pathlib import Path
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import random 
import uuid

class ImageStorage:
    def __init__(self,output_dir : str = "img"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True,exist_ok=True)
    
    def save(self,data:bytes,width:int,height:int)-> str:
        try:
        # Kiểm tra lại ảnh trả về
            with Image.open(BytesIO(data)) as image:
                if image.size != (width,height):
                    raise ValueError("Kích thước ảnh không đúng yêu cầu")
                image.verify()
            # Tạo ra ảnh từ kết quả model trả về 
            with Image.open(BytesIO(data)) as image:
                image.load()
                file_path = f"img/generate_image_{random.randint(1,10000)}_{uuid.uuid4().hex[:4]}.png"
                image.convert("RGB").save(file_path, format="PNG")
        except (
            UnidentifiedImageError,
            Image.DecompressionBombError,
            OSError,
            ValueError,
            SyntaxError,
        ) as exc:
            logger.warning("Model_image trả ảnh không hợp lệ.")

            raise HTTPException(
                status_code=502,
                detail="Model_image trả ảnh không hợp lệ.",
            ) from exc
        return file_path