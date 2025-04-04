from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "interests")  # Display user and interests in the list
    search_fields = ("user__username", "interests")  # Search by username or interests

admin.site.register(Profile, ProfileAdmin)
