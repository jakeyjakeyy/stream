from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Stream(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="stream", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=32, default=get_random_string(32), unique=True)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def is_live(self):
        return self.started_at is not None

    @property
    def hls_url(self):
        return reverse("hls-url", args=(self.user.username,))


@receiver(
    post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_stream_for_user"
)
def create_stream_for_user(sender, instance=None, created=False, **kwargs):
    """Create a stream for new users."""
    if created:
        Stream.objects.create(user=instance)


class Follow(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "target")

    def __str__(self):
        return f"{self.user.username} follows {self.target.username}"


class Featured(models.Model):
    stream = models.OneToOneField(
        Stream, related_name="is_featured", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.stream.user.username} is featured"
