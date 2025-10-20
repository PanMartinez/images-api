from django_filters import FilterSet, filters
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from images_api.images.models import Image
from images_api.images.serializers import ImageCreateSerializer, ImageRetrieveSerializer


class ImagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ImageFilterset(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Image
        fields = [
            "title",
        ]


class ImageModelViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageRetrieveSerializer
    pagination_class = ImagePagination
    filterset_class = ImageFilterset
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
