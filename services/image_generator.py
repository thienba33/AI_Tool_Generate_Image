import requests
from config import SYSTEM_PROMPT
import base64
import binascii
class ImageGenerator:
    def __init__ (self,api_key:str,model:str):
        self.model = model
        self.api_key = api_key
        self.url = "https://litellm.gdttech.net/v1/chat/completions"
    
    def generate(self,text:str)->bytes:
        final_prompt= SYSTEM_PROMPT.format(
            knowledge="",
            user_prompt=text,
        )
        header = {
            "Authorization":f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": final_prompt,
                }
            ],
            "stream": False,
            # "imageConfig":{
            #     "aspecRatio":"16:9"
            # },
            
            # set model có thể trả ảnh hoặc text
            "modalities": ["text", "image"],
        }
        try:
            response = requests.post(
                self.url,
                headers=header,
                json=payload,
                timeout=(10,180),
                allow_redirects=False
            )
        except requests.RequestException as exc:
            raise RuntimeError(
                "Không kết nối được model tạo ảnh."
            ) from exc

        if response.status_code != 200:
            raise RuntimeError(
                "Model không tạo được ảnh. "
                f"Mã HTTP: {response.status_code}"
            )

        # Lấy kết quả trả về của respone
        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Model trả dữ liệu không phải JSON."
            ) from exc
        
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("Model không trả ảnh ")
        

        message = choices[0].get("message") or {}
        images = message.get("images") or []

        if not images:
            content = message.get("content")
            detail = content or "Response không có nội dung giải thích."
            raise RuntimeError(
                f"Model không trả ảnh.\nNội dung model: {detail}"
            )
    
        # Lấy ra ảnh từ respone
        try:
            image_url = images[0]["image_url"]["url"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                "Phản hồi không chứa ảnh ở cấu trúc mong đợi."
            ) from exc

        if not isinstance(image_url, str):
            raise RuntimeError("Dữ liệu ảnh trả về không hợp lệ.")
        #ví dụ image_url = "data:image/png;base64,iVBORw0KGgo..."
        #tách tại dấu phẩy đầu tiên
        metadata, separator, encoded = image_url.partition(",")
        # ta được encoded = iVBORw0KGgo... (base64)
        if (
            not separator
            or not metadata.startswith("data:image/")
            or not metadata.endswith(";base64")
        ):
            raise RuntimeError(
                "Ảnh trả về không phải Base64 data URL"
            )

        # giải mã base64 ra bytes 
        try:
            image_bytes = base64.b64decode(
                encoded,
                validate=True,
            )
        except (binascii.Error, ValueError) as exc:
            raise RuntimeError(
                "Không giải mã được ảnh Base64."
            ) from exc

        if not image_bytes:
            raise RuntimeError("Dữ liệu ảnh rỗng.")

        return image_bytes
    