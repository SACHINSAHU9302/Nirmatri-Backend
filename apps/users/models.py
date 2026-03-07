from django.db import models
from pymongo import MongoClient
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client["nirmatriDB"]

users_collection = db["users"]


class GoogleUser(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(blank=True, null=True)
    auth_provider = models.CharField(max_length=50, default="google")
    is_active = models.BooleanField(default=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Sync with MongoDB
        users_collection.update_one(
            {"email": self.email},
            {
                "$set": {
                    "django_id": self.id,
                    "name": self.name,
                    "email": self.email,
                    "picture": self.picture,
                    "mobile": self.mobile,
                    "gender": self.gender,
                    "auth_provider": self.auth_provider,
                    "is_active": self.is_active,
                }
            },
            upsert=True
        )

    def __str__(self):
        return self.email

    class Meta:
        db_table = "google_users"
        ordering = ["-created_at"]