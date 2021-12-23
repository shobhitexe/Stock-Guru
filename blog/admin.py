from django.contrib import admin
from .models import Post,Donation ,Stock,Wishlist , Comment

admin.site.register(Post)
# admin.site.register(Category)
admin.site.register(Donation)
admin.site.register(Stock)
admin.site.register(Wishlist)
admin.site.register(Comment)
