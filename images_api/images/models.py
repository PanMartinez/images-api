from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=255, help_text="Title for the image.")
    image_file = models.ImageField(
        upload_to="uploads/",
    )
    width = models.PositiveIntegerField(
        editable=False, help_text="Width of the image after resizing."
    )
    height = models.PositiveIntegerField(
        editable=False, help_text="Height of the image after resizing."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title
