from django_filters import FilterSet, filters
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import GenericViewSet

from images_api.images.models import Image
from images_api.images.serializers import ImageCreateSerializer, ImageRetrieveSerializer
from images_api.images.utils import resize_image


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


class ImageModelViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin
):
    queryset = Image.objects.all()
    serializer_class = ImageRetrieveSerializer
    pagination_class = ImagePagination
    filterset_class = ImageFilterset
    search_fields = ["title"]
    parser_classes = (MultiPartParser, FormParser)

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        width = serializer.validated_data.get("width")
        height = serializer.validated_data.get("height")
        image_file = serializer.validated_data.get("image_file")

        resized_image = resize_image(image_file, width, height)
        image_instance = Image.objects.create(
            image_file=resized_image,
            width=width,
            height=height,
        )

        output_serializer = ImageRetrieveSerializer(
            image_instance, context={"request": request}
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
