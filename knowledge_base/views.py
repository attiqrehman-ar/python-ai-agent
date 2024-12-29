from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import KnowledgeBaseDocument
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages

# Check if user is superuser
def is_superuser(user):
    return user.is_superuser

@login_required(login_url='login/')  # Redirect to login page if not logged in
@user_passes_test(is_superuser)  # Only allow superusers
def document_list(request):
    """
    View to list all uploaded documents in the knowledge base.
    Accessible only by superusers.
    """
    documents = KnowledgeBaseDocument.objects.all()
    return render(request, 'knowledge_base/document_list.html', {'documents': documents})

@login_required(login_url='login/')  # Redirect to login page if not logged in
@user_passes_test(is_superuser)  # Only allow superusers
def upload_document(request):
    """
    View to handle document uploads by admin.
    Accessible only by superusers.
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


def login_view(request):
    """
    Custom login view that allows only superusers (admins) to log in.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                login(request, user)  # Log in the superuser
                next_url = request.GET.get('next', '/')  # Redirect to the 'next' page or homepage
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, "You must be a superuser to log in.")
                return render(request, 'knowledge_base/login.html')
        else:
            messages.error(request, "Invalid login credentials.")
            return render(request, 'knowledge_base/login.html')

    return render(request, 'knowledge_base/login.html')