from django.contrib import admin
from .models import Post,Donation ,Stock,Wishlist , Comment
from django.apps import apps

app = apps.get_app_config('blog')

for model_name, model in app.models.items():
    admin.site.register(model)