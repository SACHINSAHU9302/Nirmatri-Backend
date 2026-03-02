from django.db import models


class GoogleUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(blank=True, null=True)
    auth_provider = models.CharField(max_length=50, default="google")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "google_users"
        ordering = ["-created_at"]