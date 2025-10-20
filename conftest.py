from __future__ import annotations
from io import BytesIO
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
from rest_framework.test import APIClient

from images_api.images.models import Image


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def dummy_image_file(db):
    def _create_dummy_image_file(
        file_name: str,
        file_size=(64, 64),
        file_color=(255, 0, 0),
        file_format: str = "PNG",
    ):
        buffer = BytesIO()
        image = PILImage.new("RGB", file_size, color=file_color)
        image.save(buffer, format=file_format)
        buffer.seek(0)
        content_type_map = {
            "PNG": "image/png",
            "JPEG": "image/jpeg",
            "GIF": "image/gif",
            "WEBP": "image/webp",
        }
        return SimpleUploadedFile(
            name=file_name,
            content=buffer.read(),
            content_type=content_type_map.get(file_format, "application/octet-stream"),
        )

    return _create_dummy_image_file


@pytest.fixture
def dummy_image(db):
    def _create_dummy_image(**kwargs):
        image = Image.objects.create(**kwargs)
        return image

    return _create_dummy_image


@pytest.fixture
def test_image(db, dummy_image, dummy_image_file):
    return dummy_image(
        title="Test Image",
        width=64,
        height=64,
        image_file=dummy_image_file(file_name="test_image.jpg", file_format="JPEG"),
    )


@pytest.fixture
def dummy_file(db):
    def _create_dummy_file(file_name: str, content_type: str = "text/plain"):
        return SimpleUploadedFile(
            name=file_name,
            content=b"dummy file",
            content_type=content_type,
        )

    return _create_dummy_file
