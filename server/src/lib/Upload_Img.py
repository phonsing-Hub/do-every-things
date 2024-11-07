from pathlib import Path
from typing import List
from fastapi import UploadFile

class Img:
    def __init__(self):
        self.base_dir = Path("public")

    async def saveImage(self, name: str, images: List[UploadFile]):
        user_dir = self.base_dir / name
        user_dir.mkdir(parents=True, exist_ok=True)

        # Count existing images in the folder with a similar name pattern
        existing_images = len(list(user_dir.glob("img*")))

        for index, image in enumerate(images):
            extension = Path(image.filename).suffix

            # Use index + existing image count to avoid overwriting
            new_filename = f"img{index + existing_images}{extension}"
            image_path = user_dir / new_filename

            content = await image.read()
            with open(image_path, "wb") as f:
                f.write(content)

