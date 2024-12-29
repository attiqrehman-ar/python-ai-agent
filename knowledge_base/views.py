from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import KnowledgeBaseDocument
from django.core.files.storage import FileSystemStorage

def document_list(request):
    """
    View to list all uploaded documents in the knowledge base.
    """
    documents = KnowledgeBaseDocument.objects.all()
    return render(request, 'knowledge_base/document_list.html', {'documents': documents})

def upload_document(request):
    """
    View to handle document uploads by admin.
    """
    if request.method == 'POST' and request.FILES['document']:
        document = request.FILES['document']
        fs = FileSystemStorage()
        filename = fs.save(document.name, document)
        file_url = fs.url(filename)
        
        # Save to the database
        KnowledgeBaseDocument.objects.create(
            title=document.name,
            file=filename
        )
        return redirect('knowledge_base:document_list')
    
    return render(request, 'knowledge_base/upload_document.html')
