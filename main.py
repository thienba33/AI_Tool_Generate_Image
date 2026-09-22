from storage.image_storage import ImageStorage
from services.image_generator import ImageGenerator
from services.image_generation_service import ImageGenerationService
from config import MODEL,API_KEY_HOST



def generate_image(
    prompt: str,
    size: str,
    temperature: float,
    top_p: float,
    image_paths: list[str] | None = None,
    document_paths: list[str] | None = None,
) -> str:

    image_service = ImageGenerationService(
        image_generator=ImageGenerator(
            api_key=API_KEY_HOST,
            model=MODEL,
        ),
        image_storage=ImageStorage(),
    )

    return image_service.generate(
        prompt=prompt,
        size=size,
        image_paths=image_paths,
        document_paths=document_paths,
        temperature=temperature,
        top_p=top_p,
    )

if __name__ == "__main__":
    try:
        output_path = generate_image(
            prompt="Tạo poster cho sản phẩm trong ảnh theo tài liệu đính kèm.",
            size = "16:9",
            document_paths=["inputs/demo_brief_nuoc_hoa.pdf"],
            temperature=1.0,
            top_p=0.95,
        )

        print(f"File ảnh đã được lưu tại: {output_path}")

    except (ValueError, RuntimeError, OSError) as exc:
        print(f"Lỗi: {exc}")
