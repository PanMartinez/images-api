import pytest
from django.urls import reverse


class TestImagesViewSet:
    images_list_url = reverse("image-list")

    def test_get_images_list(self, client, test_image):
        response = client.get(self.images_list_url)
        assert response.status_code == 200
        assert response.data["count"] == 1
        response_data = response.data["results"]
        assert response_data
        assert response_data[0]["title"] == test_image.title

    def test_get_images_detail(self, client, test_image):
        url = reverse("image-detail", args=[test_image.id])
        response = client.get(url)
        assert response.status_code == 200
        assert response.data["title"] == test_image.title
        assert response.data["width"] == test_image.width
        assert response.data["height"] == test_image.height
        assert "url" in response.data

    @pytest.mark.parametrize(
        "file_format,file_name",
        [
            ("JPEG", "jpg"),
            ("PNG", "png"),
            ("GIF", "gif"),
            ("WEBP", "webp"),
        ],
    )
    def test_create_images_with_different_image_types(
        self, client, dummy_image_file, file_format, file_name
    ):
        file = dummy_image_file(f"test.{file_name}", file_format=file_format)
        payload = {
            "title": f"Test {file_format} Image",
            "image_file": file,
            "width": 320,
            "height": 240,
        }
        response = client.post(self.images_list_url, data=payload, format="multipart")
        assert response.status_code == 201

    @pytest.mark.parametrize(
        "file_format,file_name",
        [
            ("PDF", "pdf"),
            ("TXT", "txt"),
            ("XLSX", "xlsx"),
        ],
    )
    def test_create_images_with_non_image_types(
        self, client, dummy_file, file_format, file_name
    ):
        file = dummy_file(
            f"test.{file_name}", content_type=f"application/{file_format.lower()}"
        )
        payload = {
            "title": f"Test {file_format} Image",
            "image_file": file,
            "width": 320,
            "height": 240,
        }
        response = client.post(self.images_list_url, data=payload, format="multipart")
        assert response.status_code == 400

    def test_filter_images_by_name(self, client, dummy_image, dummy_image_file):
        test_image_1 = dummy_image_file("test_file1.jpg", file_format="JPEG")
        test_image_2 = dummy_image_file("test_file2.png", file_format="PNG")
        test_image_3 = dummy_image_file("test_file3.webp", file_format="WEBP")
        dummy_image(title="Test file 1", image_file=test_image_1, width=64, height=64)
        dummy_image(title="Test file 2", image_file=test_image_2, width=64, height=64)
        dummy_image(title="Another file", image_file=test_image_3, width=64, height=64)

        response = client.get(self.images_list_url, {"title": "Test file"})
        assert response.status_code == 200
        assert response.data["count"] == 2
        titles = [item["title"] for item in response.data["results"]]
        assert "Test file 1" in titles
        assert "Test file 2" in titles
        assert all("test" in t.lower() for t in titles)
