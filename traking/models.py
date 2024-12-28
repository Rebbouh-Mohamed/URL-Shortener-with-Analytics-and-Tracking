from os import name
from typing import DefaultDict
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.conf import settings
from user_agents import parse
import tldextract
User = get_user_model()

class TrackedLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_links")
    url = models.URLField()  # Original URL
    url_name=models.CharField(max_length=30,default=url)
    slug = models.SlugField(unique=True, blank=True)  # Unique identifier for shortened URL
    created_at = models.DateTimeField(auto_now_add=True)
    # new_link=f"{settings.SITE_DOMAIN}/track/{slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex[:8]  # Generates a short unique identifier
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tracked URL by {self.user}: {self.url}"

class Click(models.Model):
    tracked_link = models.ForeignKey(TrackedLink, on_delete=models.CASCADE, related_name="clicks")
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Click on {self.tracked_link.url} at {self.timestamp}"
    def  device(self):
        user_agent = parse(self.user_agent)
        # Determine if the source is a mobile app or a web browser
        if user_agent.is_mobile:
            return "Mobile"
        elif user_agent.is_tablet:
            return "Tablet"
        elif user_agent.is_pc:
            return "Desktop"
        else:
            return "Other"
    def ref(self):
        extracted = tldextract.extract(self.referrer)
        return extracted.domain.lower()

    def save(self,*args,**kwargs):
        if self.user_agent :
            self.user_agent=self.device()
        if self.referrer:
            self.referrer=self.ref()
        super().save(*args, **kwargs)
