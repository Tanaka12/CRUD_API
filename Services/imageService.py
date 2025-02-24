import os

class ImageService:

    def __init__(self):
        pass

    def save_image(self, image:str, path: str):
        with open(path, 'w') as file_handle:
            file_handle.write(image)

    def load_image(self, image_path:str) -> str:
        with open(image_path, 'r') as file_handle:
            return file_handle.read()

    def delete_image(self, image_path:str):
        os.remove(image_path)