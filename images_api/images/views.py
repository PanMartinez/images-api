# images/views.py
from rest_framework import viewsets
from .models import Image
from .serializers import ImageCreateSerializer, ImageRetrieveSerializer
from .pagination import StandardImagePagination
from drf_spectacular.utils import extend_schema


class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageRetrieveSerializer
    pagination_class = StandardImagePagination
    search_fields = ["title"]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return ImageCreateSerializer
        return self.serializer_class

    @extend_schema(
        summary="Upload Image",
        request=ImageCreateSerializer,
        responses={201: ImageRetrieveSerializer},
        description="Endpoint to upload image, and resize it based on dimensions provided in the request.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
