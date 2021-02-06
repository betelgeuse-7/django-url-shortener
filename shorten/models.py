from django.db import models


class URL(models.Model):
    raw_url = models.URLField(max_length=400)
    shortened_url = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shortened_url
