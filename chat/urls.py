from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.chat_home, name='chat_home'),  # Chat interface
    path('ask/', views.ask_question, name='ask_question'),
    # path('dashboard/', views.dashboard, name='dashboard') # Handle user query
]
