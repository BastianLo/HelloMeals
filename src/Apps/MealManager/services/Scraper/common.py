import re
import uuid
from io import BytesIO
from tempfile import NamedTemporaryFile

import requests
from PIL import Image
from django.core.files.base import File
from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()


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
            image = image.resize((max_width, new_height), Image.LANCZOS)
        # Save the resized image to a temporary file
        img_tmp = NamedTemporaryFile(delete=True)
        image.save(img_tmp, format='JPEG')
        # Create a Django File object from the temporary file
        img = File(img_tmp)
        return img
    except Exception as e:
        print(e)
        return None


def maybe_save_image(instance, image_url, preference_key):
    """Download and attach `image_url` to `instance.image` unless it already has one or the
    given global preference (e.g. 'scraper__Download_Recipe_Images') disables it."""
    if instance.image and instance.image.file:
        return
    if not global_preferences[preference_key]:
        return
    image = get_image(image_url)
    if image is not None:
        instance.image.save(str(uuid.uuid4()) + ".png", image)
