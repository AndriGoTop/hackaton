from django.contrib import admin
from .models import CustomUser,News,Tags,Subs
admin.site.register(CustomUser)
admin.site.register(News)
admin.site.register(Tags)
admin.site.register(Subs)

