from django.contrib import admin
from .models import User, Listing,Comment,Achievelist,Allblogs

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Achievelist)
admin.site.register(Allblogs)
