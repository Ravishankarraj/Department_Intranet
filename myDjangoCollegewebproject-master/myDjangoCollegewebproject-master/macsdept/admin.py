from django.contrib import admin
from .models import NoticeText
from .models import UserProfile

# Register your models here.
admin.site.register(NoticeText)
admin.site.register(UserProfile)
