import os
from pathlib import Path
from PIL import Image
from config import MAX_INPUT_IMAGES, MAX_INPUT_FILES, SIZE_STORAGE_IMAGES, SIZE_STORAGE_TEXT, SIZE_STORAGE_FILE, MAX_PAGES,IMAGES_FORMATS
from pypdf import PdfReader
from pypdf.errors import PyPdfError
class InputValidator:
    def __init__(
            self,
            image_paths: list[str]|None = None, 
            document_paths:list[str]| None = None
        ):
        self.image_paths = list(image_paths or [])
        self.document_paths = list(document_paths or [])
        
    def validate(self)->None:
        self._validate_counts()

        for image_path in self.image_paths:
            self._validate_image(image_path)
        for document_path in self.document_paths:
            self._validate_document(document_path)
    

    # kiểm tra số lượng ảnh và file gửi lên có vượt quá giới hạn cho phép hay không
    def _validate_counts(self)->None:
        if len(self.image_paths) > MAX_INPUT_IMAGES:
            raise ValueError(f"Chỉ được gửi tối đa {MAX_INPUT_IMAGES} ảnh,"
                             f" bạn đã gửi {len(self.image_paths)} ảnh"
                            )
        if len(self.document_paths) > MAX_INPUT_FILES:
            raise ValueError(
                f"Chỉ được gửi tối đa {MAX_INPUT_FILES} file,"
                f" bạn đã gửi {len(self.document_paths)} file"
            )
        
    # kiểm tra file xem có rỗng hay quá giới hạn cho phép ko
    def _validate_file(self,path:str, max_bytes:int)->Path:
        file_path = Path(path)
        if not file_path.is_file():
            raise ValueError(f"File {path} không tồn tại hoặc không phải là file")
        # lấy ra dung lượng của file
        file_size = file_path.stat().st_size

        if file_size == 0:
            raise ValueError(f"File rỗng: {file_path.name}")
        if file_size > max_bytes:
            raise ValueError(f"File vượt quá giới hạn dung lượng {file_size}")
        return file_path

    # kiểm tra 
    def _validate_image(self, path:str)->None:
        try:
            image_path = self._validate_file(path=path,max_bytes=SIZE_STORAGE_IMAGES)
            with Image.open(image_path) as img:
                img_format = img.format.upper()
            if img_format not in IMAGES_FORMATS:
                raise ValueError(
                    f"Định dạng ảnh không được hỗ trợ: {img_format}. "
                    f"Cho phép: {', '.join(IMAGES_FORMATS)}"
                )
            img.verify()
            with Image.open(image_path) as img:
                img.load()
            
        except OSError as exc:
            raise ValueError(
                f"Không đọc được ảnh '{path}': "
                "file không hợp lệ, bị hỏng, không có quyền đọc "
                "hoặc thiếu bộ giải mã."
            ) from exc
    
    def _validate_document(self, path:str)->None:
        #lấy ra đuôi của file 
        extension = Path(path).suffix.lower()
        if extension not in {".txt",".pdf"}:
            raise ValueError("Chỉ hỗ trợ tài liệu txt và pdf")

        if extension == ".txt":
            max_bytes = SIZE_STORAGE_TEXT
        else:
            max_bytes = SIZE_STORAGE_FILE

        try:
            #kiểm tra dung lượng có đạt quy định ko 
            file_path = self._validate_file(
                path=path,
                max_bytes=max_bytes
            )
            if extension == ".txt":
                content = file_path.read_text(encoding="utf-8-sig")
                if not content.strip():
                    raise ValueError(f"File txt không có nội dung {file_path.name}")

            else:
                with file_path.open("rb") as file:
                    reader = PdfReader(file)

                    if reader.is_encrypted:
                        raise ValueError(f"Chưa hỗ trợ pdf mã hóa {file_path.name}")
                    page_count = len(reader.pages)
                    if page_count == 0:
                        raise ValueError(f"pdf không có trang nào {file_path.name}")
                    if page_count > MAX_PAGES:
                        raise ValueError(
                        f"PDF có {page_count} trang, "
                        f"chỉ cho phép tối đa {MAX_PAGES} trang."
                    )
        except UnicodeDecodeError as exc: 
            raise ValueError(
                f"File txt phải được lưu bằng utf-8: {path}"
            ) from exc

        except PyPdfError as exc:
            raise ValueError(
                f"Không đọc được cấu trúc pdf {path}"
            ) from exc
        except OSError as exc :
            raise ValueError(f"Không đọc được file hoặc không có quyền truy cập {path}") from exc

    #kiểm tra các tham số mặc định
    def validate_parameter (
        temperature: float,
        top_p: float,
    )->None:
        parameters = [
            ("temperature", temperature, 0.0, 2.0),
            ("top_p", top_p, 0.0, 1.0),
        ]
        for name,value, minimum,maximum in parameters:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} phải là số.")

        if not minimum <= value <= maximum:
            raise ValueError(
                f"{name} phải nằm trong khoảng {minimum}–{maximum}."
            )
