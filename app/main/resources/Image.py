import os
from io import BytesIO

from PIL import Image as PILImage, Image
import random
import string
from datetime import datetime

from app.main.resources.JSON import JsonObject
from config import config


class FileProcessor:
    def __init__(self, img, name_prefix):
        img = JsonObject(img)
        self.ext = None
        self.e = None
        self.name = img.filename
        self.tmp_name = img.content
        self.extn()
        self.ratio = None
        self.new_name = self.name
        self.type = self.getFileType()

        self.getratio()
        if self._is("vid") or self._is("img"):
            prefix = "Img" if self._is("img") else "Vid"
            self.new_name = f"{name_prefix}{prefix}-{self.generate_unique_id()}-{self.get_current_date()}.{self.ext}"

    def extn(self):
        ext = os.path.splitext(self.name)[1][1:]
        self.ext = self.e = ext.lower() if ext else ext

    def getratio(self):
        self.ratio = "200/800"
        if self._is("img"):
            image = Image.open(BytesIO(self.tmp_name))
            width, height = image.size
            self.ratio = f"{width}/{height}"

    def upload(self, _dir):
        d = _dir
        ext = self.ext
        dirs = "Hesadocs"

        if self._is("img"):
            dirs = "HesaImages"
        if self._is("vid"):
            dirs = "HesaVids"

        base_path = config["base_path"]
        directory = os.path.join(base_path, "app", "main", "static", "media", "hesa-media", "data", dirs, _dir, "h")
        os.makedirs(directory, exist_ok=True)

        with open(os.path.join(directory, self.new_name), "wb") as file:
            file.write(self.tmp_name)

        if self._is("img"):
            l = self.generate_low_quality_image(d, os.path.join(directory, self.new_name), base_path)

    def _is(self, type_):
        refs = {
            "vid": {"r": ["mkv", "mp4"], "a": "vid"},
            "img": {"r": ["jpg", "png", "jpeg", "webp", "svg"], "a": "vid"},
        }
        if type_ in refs:
            return self.ext in refs[type_]["r"]
        return False

    def generate_low_quality_image(self, _dir, high_quality_image_path, u):
        ext = os.path.splitext(self.name)[1][1:]
        vids = ["mkv", "mp4"]
        imgs = ["jpg", "png", "jpeg", "webp", "svg"]
        dirs = "Hesadocs"

        if ext in imgs:
            dirs = "HesaImages"
        if ext in vids:
            dirs = "HesaVids"

        directory = os.path.join(u, "app", "main", "static", "media", "hesa-media", "data", dirs, _dir, "l")
        os.makedirs(directory, exist_ok=True)

        target_path = os.path.join(directory, self.new_name)
        high_quality_image = PILImage.open(high_quality_image_path)
        width, height = high_quality_image.size
        new_width = 40
        new_height = (height / width) * new_width
        low_quality_image = high_quality_image.resize((int(new_width), int(new_height)))
        low_quality_image.save(target_path, quality=50)
        return target_path

    @staticmethod
    def generate_unique_id():
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d")

    def getFileType(self):
        if self._is("img"):
            return "img"
        elif self._is("vid"):
            return "vid"
        return "file"
