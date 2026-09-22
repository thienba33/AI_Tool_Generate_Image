from pathlib import Path
from PIL import Image

import requests
from config import URL_HOST,SIZE_IMAGE, build_system_prompt
import base64
import binascii
from models.input_validator import InputValidator
class ImageGenerator:
    def __init__ (self,api_key:str,model:str):
        self.model = model
        self.api_key = api_key
        self.url = URL_HOST
    
    def generate(
            self,text:str,
            size: str,
            temperature: float,
            top_p: float,
            image_paths: list[str] | None = None,
            document_paths: list[str] | None = None,
        )->bytes:

        if not isinstance(size, str):
            raise ValueError("Kích thước ảnh phải là chuỗi ví dụ '1:1', '2:3', '3:2'...")
        
        size = size.strip()

        if size not in SIZE_IMAGE:
            raise ValueError(f"Kích thước ảnh không hợp lệ, vui lòng chọn trong các kích thước sau: {SIZE_IMAGE}")


        if not isinstance(text,str) or not text.strip():
                raise ValueError("Yêu cầu tạo ảnh phải là văn bản không rỗng.")

        #list các ảnh truyền vào
        image_paths = list(image_paths or [])

        #list các file txt hoặc pdf truyền vào
        document_paths = list(document_paths or [])

        # kiểm tra các tham số mặc định 
        InputValidator.validate_parameter(
            temperature=temperature,
            top_p=top_p,
        )
        # kiểm tra các ảnh hoặc file 
        validator = InputValidator(
            image_paths=image_paths,
            document_paths=document_paths,
        )
        validator.validate()

        # nội dung gửi cho model
        user_content = [
            {"type": "text", "text": text}
        ]

        image_mime_types = {
            "PNG": "image/png",
            "JPEG": "image/jpeg",
            "WEBP": "image/webp",
            "HEIC": "image/heic",
            "HEIF": "image/heif",
        }

        # đọc từng ảnh và chuyển sang dạng base64 rồi đưa và payload
        for path in image_paths:
            image_path = Path(path)

            with Image.open(image_path) as img:
                image_format = (img.format or "").upper()

            mime_type = image_mime_types.get(image_format)
            if mime_type is None:
                raise ValueError(f"Không xác định được MIME của ảnh: {path}")

            encoded = base64.b64encode(
                image_path.read_bytes()
            ).decode("ascii")

            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{encoded}"
                },
            })


        # Chuyển các file txt hoặc pdf sang dạng base64
        for path in document_paths:
            file_path = Path(path)
            extension = file_path.suffix.lower()

            if extension == ".txt":
                content = file_path.read_text(encoding="utf-8-sig")

                user_content.append({
                    "type": "text",
                    "text": (
                        f"Tài liệu tham khảo: {file_path.name}\n\n"
                        f"{content}"
                    ),
                })

            elif extension == ".pdf":
                encoded = base64.b64encode(
                    file_path.read_bytes()
                ).decode("ascii")

                user_content.append({
                    "type": "file",
                    "file": {
                        "filename": file_path.name,
                        "file_data": (
                            f"data:application/pdf;base64,{encoded}"
                        ),
                    },
                })
        
        header = {
            "Authorization":f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages":[
                {
                    "role": "system",
                    "content": build_system_prompt(knowledge=""),
                },
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
            "modalities": ["image"],
            "imageConfig": {"aspectRatio": size},
            "stream": False,
            "top_p":top_p,
            "temperature":temperature,
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
        
        print("HTTP status:", response.status_code)
        
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
    
