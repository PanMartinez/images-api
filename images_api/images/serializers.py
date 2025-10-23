from rest_framework import serializers
from .models import Image


class ImageCreateSerializer(serializers.ModelSerializer):
    width = serializers.IntegerField(min_value=1, write_only=True)
    height = serializers.IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Image
        fields = ["title", "image_file", "width", "height"]


class ImageRetrieveSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["id", "url", "title", "width", "height"]
        read_only_fields = ["id", "url", "title", "width", "height"]

    def get_url(self, obj: Image) -> str | None:
        if obj.image_file:
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return None
