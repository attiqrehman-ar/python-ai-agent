from django.shortcuts import render
from django.http import JsonResponse
from .models import UserQuery
from knowledge_base.models import KnowledgeBaseDocument
import os

def chat_home(request):
    """
    View to render the chat interface.
    """
    return render(request, 'chat/chat_home.html')

def ask_question(request):
    """
    API endpoint to handle user queries.
    """
    if request.method == 'POST':
        user_query = request.POST.get('question', '').strip()
        
        # Default response if no knowledge base document matches
        default_response = "Sorry, I couldn't find an answer to your question."

        # Check if there's a match in the knowledge base
        documents = KnowledgeBaseDocument.objects.all()
        answer_found = None

        for doc in documents:
            file_path = os.path.join(doc.file.path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check if the query matches a question in the document
                if user_query.lower() in content.lower():
                    # Extract the answer after the matching question
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        if user_query.lower() in line.lower():
                            # Assuming the next line is the answer
                            if i + 1 < len(lines):
                                answer_found = lines[i + 1]  # Get the next line as the answer
                            break
                    if answer_found:
                        break
        
        # Log the query and response
        UserQuery.objects.create(
            question=user_query,
            answer=answer_found or default_response
        )

        # Respond to the user
        return JsonResponse({
            'question': user_query,
            'answer': answer_found or default_response
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)