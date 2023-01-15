from django.db import models


class Videos(models.Model):
    video_id = models.CharField("video id", max_length=11,
                                primary_key=True)  # postgres auto creates a clustered index (useful for filtering)
    video_title = models.CharField("Video Title", max_length=255)
    description = models.TextField("Description", db_index=True)  # index will be useful for filtering on date
    published_on = models.DateTimeField("publishing datetime")
    thumb_url = models.URLField(
        "Thumbnail URL", max_length=255, help_text="The URL to the video thumbnail"
    )
    link = models.URLField(
        "Video Link", max_length=255, help_text="The URL to the video page"
    )

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"
        ordering = ["-published_on"]  # To sort in reverse chronological order

    def __str__(self):
        return self.video_title
