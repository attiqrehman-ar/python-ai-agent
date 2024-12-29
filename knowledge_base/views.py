from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import KnowledgeBaseDocument
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout

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


def logout_view(request):
    """
    Logs the user out and redirects them to the chat_home page (landing page).
    """
    logout(request)  # Logs the user out
    return redirect('chat:chat_home') 

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect


def contact(request):
    """
    Handle the contact form submission.
    If the form is valid, send the details to the admin's email.
    """
    if request.method == 'POST':
        # Extracting form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validating input data (You can add more complex validation here)
        if not name or not email or not subject or not message:
            messages.error(request, "All fields are required!")
            return render(request, 'knowledge_base/contact.html')

        # Send an email to the admin or support team
        try:
            send_mail(
                f"Contact Us - {subject}",
                f"Message from {name} ({email}):\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,  # The sender email
                [settings.CONTACT_EMAIL],  # The recipient email (admin/support)
            )
            # Show success message and redirect to the same page or a thank you page
            messages.success(request, "Your message has been sent successfully!")
            return HttpResponseRedirect(request.path)  # Redirect to the same page after form submission
        except Exception as e:
            # In case of any error while sending email
            messages.error(request, f"An error occurred while sending your message. Please try again later. {str(e)}")
            return render(request, 'knowledge_base/contact.html')
    
    # Render the contact form page
    return render(request, 'knowledge_base/contact.html')

