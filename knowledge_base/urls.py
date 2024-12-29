from django.urls import path
from . import views

app_name = "knowledge_base"

urlpatterns = [
    path('', views.document_list, name='document_list'),  # List all documents
    path('upload/', views.upload_document, name='upload_document'),  # Upload a document
]
