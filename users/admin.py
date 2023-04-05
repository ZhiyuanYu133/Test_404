from django.contrib import admin
from .models import Profile, FriendRequest, Inbox,Follower

# Register your models here.
admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(FriendRequest)
admin.site.register(Inbox)