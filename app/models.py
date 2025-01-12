from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.conf import settings
from django.utils import timezone
from moviepy import VideoFileClip
import datetime
import os


# Create your models here.


class User(AbstractUser):
    avatar = models.FileField(
        upload_to="avatars/", default=settings.DEFAULT_AVATAR_PATH
    )
    subscribers = models.IntegerField(default=0)

    def get_wallet_balance(self):
        wallet = Wallet.objects.get(user=self)
        return wallet.balance

    def has_card(self):
        wallet = Wallet.objects.get(user=self)
        return True if wallet.card else False


class Card(models.Model):
    number = models.CharField(max_length=16, blank=False)
    expiration_date = models.DateField(blank=False)
    cvv = models.CharField(max_length=3, blank=False)

    def __str__(self):
        return f"{self.number} - {self.cvv}"


class Wallet(models.Model):
    card = models.OneToOneField(Card, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance}"


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="uploads"
    )
    video = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.creator} - {self.title}"

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        video_path = self.video.path
        thumbnail_dir = os.path.join(os.path.dirname(video_path), 'thumbnails')
        thumbnail_path = os.path.join(thumbnail_dir, os.path.basename(video_path).replace('.mp4', '.jpg'))

        os.makedirs(thumbnail_dir, exist_ok=True)

        with VideoFileClip(video_path) as clip:
            clip = clip.resized(height=720)
            clip.save_frame(thumbnail_path, t=0.00)

        self.thumbnail = thumbnail_path
        self.save()

    def compress_video(self):
        video_path = self.video.path
        output_path = video_path.replace('.mp4', '_compressed.mp4')
        try:
            with VideoFileClip(video_path) as clip:
                clip.write_videofile(output_path, codec='libx264', preset='fast', bitrate='2500k')
            self.video = output_path
            self.save()
            os.remove(video_path)
        except Exception as e:
            print(f"Error compressing video: {e}")


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(
        "Video", on_delete=models.CASCADE, related_name="video_comments"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_comments"
    )
    content = models.TextField(blank=False, max_length=3000)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} | {self.video.title} - {self.content}"


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(
        "Video", on_delete=models.CASCADE, related_name="video_likes"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_likes"
    )

    def __str__(self):
        return f"{self.video.title} - {self.user.username}"


class Dislike(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(
        "Video", on_delete=models.CASCADE, related_name="video_dislikes"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_dislikes"
    )

    def __str__(self):
        return f"{self.video.title} - {self.user.username}"


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_subscriber"
    )
    creator = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_creator"
    )

    def __str__(self):
        return f"{self.subscriber} is subscribed to {self.creator}"
