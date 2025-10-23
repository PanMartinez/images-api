from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def resize_image(image_field, width: int, height: int) -> ContentFile:
    image = Image.open(image_field)

    # We need to convert an image to RGB in case of PNG with transparency
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGB")

    # ImageOps.fit maintains the aspect ratio of an image and crops it to fit the specified dimensions
    resized_image = ImageOps.fit(
        image,
        (width, height),
        method=Image.Resampling.LANCZOS,
        bleed=0.0,
        centering=(0.5, 0.5),
    )

    image_io = BytesIO()
    image_format = (image.format or "JPEG").upper()

    if image_format == "PNG" and image.mode == "RGBA":
        resized_image.save(image_io, format="PNG", optimize=True)
    else:
        resized_image = resized_image.convert("RGB")
        resized_image.save(image_io, format="JPEG", quality=85, optimize=True)

    file_ext = image_format.lower()
    file_name = f"{image_field.name.rsplit('.', 1)[0]}_{width}x{height}.{file_ext}"
    image_content = ContentFile(image_io.getvalue(), name=file_name)

    return image_content
