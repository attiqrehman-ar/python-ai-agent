from django.shortcuts import render
from django.http import JsonResponse
from sentence_transformers import SentenceTransformer, util
from .models import UserQuery
from knowledge_base.models import KnowledgeBaseDocument
import os


model = SentenceTransformer('all-MiniLM-L6-v2')


def chat_home(request):
    """
    View to render the chat interface.
    """
    return render(request, 'chat/chat_home.html')

def ask_question(request):
    if request.method == 'POST':
        user_query = request.POST.get('question', '').strip()
        default_response = "Sorry, I couldn't find an answer to your question."

        # Fetch all knowledge base documents
        documents = KnowledgeBaseDocument.objects.all()
        knowledge_base = []

        for doc in documents:
            try:
                with doc.file.open('r') as file:
                    content = file.read()
                    paragraphs = content.split('\n\n')  # Split into smaller sections
                    knowledge_base.extend(paragraphs)
            except Exception as e:
                print(f"Error reading file {doc.file.name}: {e}")

        if knowledge_base:
            query_embedding = model.encode(user_query, convert_to_tensor=True)
            doc_embeddings = model.encode(knowledge_base, convert_to_tensor=True)
            scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)

            # Log similarity scores for debugging
            print(f"Similarity scores: {scores}")

            best_score_index = scores.argmax().item()
            if scores[0][best_score_index] > 0.3:  # Adjusted threshold
                best_answer = knowledge_base[best_score_index]
            else:
                best_answer = default_response
        else:
            best_answer = default_response

        # Return the question, answer, and formatted response message as JSON
        response_message = f"**Your Question:** {user_query}\n\n**Answer:** {best_answer}"

        return JsonResponse({'question': user_query, 'answer': best_answer, 'response_message': response_message})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
