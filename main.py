from storage.image_storage import ImageStorage
from services.image_generator import ImageGenerator
from services.image_generation_service import ImageGenerationService
from models.prompt import Prompt
from config import API_KEY_MODEL_IMAGE, MODEL, ACCOUNT_ID


def generate_image(prompt: Prompt):
    image_service = ImageGenerationService(
        image_generator=ImageGenerator(
            api_key=API_KEY_MODEL_IMAGE,
            account_id=ACCOUNT_ID,
            model=MODEL,
        ),
        image_storage=ImageStorage(),
    )

    return image_service.generate(prompt)


if __name__ == "__main__":
    prompt = Prompt(
        input=input("Illustrative image: "),
        width=int(input("width: ")),
        height=int(input("height: ")),
    )

    image_path = generate_image(prompt)
    print("Đã lưu ảnh tại:", image_path)