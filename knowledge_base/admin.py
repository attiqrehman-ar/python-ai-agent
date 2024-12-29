from django.contrib import admin
from .models import KnowledgeBaseDocument

class KnowledgeBaseDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')  # Columns displayed in the admin list view
    search_fields = ('title',)              # Add search functionality

admin.site.register(KnowledgeBaseDocument, KnowledgeBaseDocumentAdmin)
