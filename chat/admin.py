from django.contrib import admin
from .models import UserQuery

class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at')  # Customize columns in admin list view
    search_fields = ('question', 'answer')              # Enable search for questions and answers
    list_filter = ('created_at',)                       # Add a filter by creation date

admin.site.register(UserQuery, UserQueryAdmin)
