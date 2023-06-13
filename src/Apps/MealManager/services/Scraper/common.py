import re
from io import BytesIO
from tempfile import NamedTemporaryFile

import requests
from PIL import Image
from django.core.files.base import File


def is_valid_iso_duration(duration_str):
    pattern = r'^P(?:\d+Y)?(?:\d+M)?(?:\d+W)?(?:\d+D)?(?:T(?:\d+H)?(?:\d+M)?(?:\d+S)?)?$'
    return re.match(pattern, duration_str) is not None


def get_image(url):
    if url is None:
        return None
    try:
        image_data = requests.get(url).content
        # Open the image using Pillow
        image = Image.open(BytesIO(image_data))
        # Resize the image
        max_width = 720
        if image.width > max_width:
            ratio = max_width / float(image.width)
            new_height = int(image.height * ratio)
            image = image.resize((max_width, new_height), Image.ANTIALIAS)
        # Save the resized image to a temporary file
        img_tmp = NamedTemporaryFile(delete=True)
        image.save(img_tmp, format='JPEG')
        # Create a Django File object from the temporary file
        img = File(img_tmp)
        return img
    except Exception as e:
        print(e)
        return None
