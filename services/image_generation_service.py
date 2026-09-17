from fastapi import HTTPException

from models.prompt import Prompt
from services.image_generator import ImageGenerator
from storage.image_storage import ImageStorage

class ImageGenerationService:
    def __init__ (self,image_generator: ImageGenerator,image_storage:ImageStorage):
        self.image_storage = image_storage
        self.image_generator = image_generator
    
    def generate(self,prompt:Prompt)->str:
        image_generator = self.image_generator.generate(
            text=prompt.input,
            width=prompt.width,
            height=prompt.height,
        )
        return self.image_storage.save(
            data=image_generator,
            width=prompt.width,
            height=prompt.height
        )