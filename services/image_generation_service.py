from services.image_generator import ImageGenerator
from storage.image_storage import ImageStorage

class ImageGenerationService:
    def __init__ (self,image_generator: ImageGenerator,image_storage:ImageStorage):
        self.image_storage = image_storage
        self.image_generator = image_generator
    def generate(
        self,
        prompt: str,
        size: str,
        temperature: float,
        top_p: float,
        image_paths: list[str] | None = None,
        document_paths: list[str] | None = None,
    ) -> str:
        image_bytes = self.image_generator.generate(
            text=prompt,
            size=size,
            image_paths=image_paths,
            document_paths=document_paths,
            temperature=temperature,
            top_p=top_p,
        )

        return self.image_storage.save(data=image_bytes)
