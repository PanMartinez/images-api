from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def resize_image(image_field, width, height):
    image = Image.open(image_field)

    # We need to convert image to RGB in case of PNG with transparency
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    resized_image = image.resize((width, height), Image.Resampling.LANCZOS)
    image_io = BytesIO()
    image_format = image.format if image.format else "JPEG"
    resized_image.save(image_io, format=image_format, quality=95)
    image_content = ContentFile(image_io.getvalue(), name=image_field.name)

    return image_content
