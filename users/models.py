from django.db import models
from django.core.cache import cache

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Cache the user credentials
        cache_key = f'user_credentials_{self.email}'
        cache_data = {
            'email': self.email,
            'password': self.password
        }
        cache.set(cache_key, cache_data, timeout=3600)  # Cache for 1 hour

    @classmethod
    def get_cached_credentials(cls, email):
        cache_key = f'user_credentials_{email}'
        return cache.get(cache_key)
