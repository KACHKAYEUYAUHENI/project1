from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255,
                            unique_for_date="publish")

    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="author_materials")

    title_image = models.ImageField(upload_to="post/%Y/%m/%d",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_website:detailed_news",
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):

    name = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(News,
                                 on_delete=models.CASCADE,
                                 related_name='comments')

    def __str__(self):
        return '@{name} {body} for {material}'.format(name=self.name,
                                                      body=self.body,
                                                      material=self.material)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d", blank=True)


class NewsType(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    news = models.ManyToManyField(News, related_name='news')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_website:detailed_news_type',
                       args=[self.slug])
