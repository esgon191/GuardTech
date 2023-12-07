from django.db import models


class Cve(models.Model):
    name = models.CharField(max_length=128, blank=False)
    platform = models.CharField(max_length=128, blank=False)
    product = models.CharField(max_length=128, blank=False)
    updateLink = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return self.name
