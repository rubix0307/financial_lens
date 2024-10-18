from django.db import models
from django.contrib.auth import get_user_model


class Section(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    users = models.ManyToManyField(get_user_model(), through='SectionUser', related_name='sections', blank=True)

    def __str__(self):
        return self.name


class SectionUser(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    is_base = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} in {self.section}"
