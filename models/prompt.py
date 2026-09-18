from pydantic import BaseModel, ConfigDict, Field


# validate câu prompt của người dùng 
class Prompt(BaseModel):
    model_config = ConfigDict(
        strict=True,                 # Yêu cầu đúng kiểu dữ liệu
        str_strip_whitespace=True,   # Bỏ khoảng trắng đầu và cuối
        extra="forbid",               # Không nhận trường ngoài khai báo
    )

    input: str = Field(min_length=1, max_length=10000)
 
