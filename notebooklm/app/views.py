from distutils.command.config import config
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, ChatFile, ChatUrl, Message
from .forms import ChatForm, ChatFileForm
from .file_controller import fetch_website_content, extract_pdf_content, extract_excel_content
import requests
from dotenv import load_dotenv
import os

# Model settings
load_dotenv()
API_URL = os.getenv("API_URL")

MAX_HISTORY_LENGTH = 10  # Maximum number of messages in history

# ------------------------- Helper functions -------------------------

def build_prompt(context, history, query):
    """
    Construct the prompt to send to the model.
    """
    return f"""
You are a Persian-speaking AI assistant that must reply only in Persian.
### Very important and mandatory rules:
1. Use of **no other language** such as English, Spanish, or any other is allowed.
2. Any specialized foreign term must be translated or explained in Persian.
3. If you cannot provide an exact answer, simply write: "The answer was not found in the provided data."
4. Even if the provided content includes other languages, you must reply only in Persian.

### Conversation history:
{history}

### Related content:
{context}

### Question:
{query}

Your final response must:
1. Be fully fluent and in Persian.
2. Contain no words or phrases from other languages.
3. Be accurate, understandable, and flawless.
Please respond only in Persian.
"""


def get_response_from_model(prompt):
    """
    Send the prompt to the model and receive the response.
    """
    try:
        response = requests.post(API_URL, json={
            "model": "llama3.2:latest",
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.5,
            "top_p": 1
        })
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to the model: {str(e)}"
    except ValueError:
        return "Error parsing the model's response."
    except Exception as e:
        return f"Unknown error: {str(e)}"


def update_history(chat, user_input, assistant_response):
    """
    Update the conversation history for a specific chat.
    """
    Message.objects.create(chat=chat, text=user_input, response=assistant_response)


def extract_context(chat):
    """
    Extract related content from the chat's files and URLs.
    """
    files_content = "\n".join(file.pdf_content or file.excel_content or "" for file in chat.files.all())
    urls_content = "\n".join(url.content or "" for url in chat.urls.all())
    return f"{files_content}\n{urls_content}"


def build_history(chat):
    """
    Build the conversation history as a string.
    """
    return "\n".join(
        f"User: {msg.text}\nAssistant: {msg.response}" for msg in
        Message.objects.filter(chat=chat).order_by('created_at')
    )

# ------------------------- Views -------------------------

def home(request):
    """
    Render the homepage displaying the list of chats.
    """
    chats = Chat.objects.all()
    return render(
        request,
        'RAG/home.html',
        {'chats': chats}
    )


def chat_detail(request, chat_id):
    """
    Display chat details and handle new questions.
    """
    chat = get_object_or_404(Chat, pk=chat_id)
    context = extract_context(chat)  # Extract content from the chat's files and URLs
    history = build_history(chat)    # Build history

    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            prompt = build_prompt(context, history, query)
            response = get_response_from_model(prompt)
            update_history(chat, query, response)
            return render(request, 'RAG/chat_detail.html', {'chat': chat, 'response': response, 'query': query})

    return render(request, 'RAG/chat_detail.html', {'chat': chat})


def create_chat(request):
    """
    Create a new chat and handle file and URL uploads.
    """
    if request.method == 'POST':
        chat_form = ChatForm(request.POST)
        if chat_form.is_valid():
            chat = chat_form.save()
            save_uploaded_files(chat, request.FILES.getlist('file'))
            save_urls(chat, request.POST.getlist('url'))
            return redirect('chat_detail', chat_id=chat.id)

    return render(request, 'RAG/create_chat.html', {'chat_form': ChatForm()})


def save_uploaded_files(chat, files):
    """
    Save uploaded files and extract their content.
    """
    for file in files:
        if file.name.endswith('.pdf'):
            pdf_content = extract_pdf_content(file)
            ChatFile.objects.create(chat=chat, file=file, pdf_content=pdf_content)
        elif file.name.endswith(('.xlsx', '.xls')):
            excel_content = extract_excel_content(file)
            ChatFile.objects.create(chat=chat, file=file, excel_content=excel_content)
        else:
            ChatFile.objects.create(chat=chat, file=file)


def save_urls(chat, urls):
    """
    Save URLs and extract their content.
    """
    for url in urls:
        if url:
            content = fetch_website_content(url)
            ChatUrl.objects.create(chat=chat, url=url, content=content)

@csrf_exempt
def chat_content_json(request, chat_id):
    """
    API endpoint to get chat content as JSON.
    """
    try:
        chat = Chat.objects.get(pk=chat_id)
        data = {
            'chat_name': chat.name,
            'files': [
                {'file_name': file.file.name, 'file_url': file.file.url, 'pdf_content': file.pdf_content,
                 'excel_content': file.excel_content}
                for file in chat.files.all()
            ],
            'urls': [{'url': url.url, 'content': url.content} for url in chat.urls.all()],
        }
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Chat.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Chat not found'}, status=404)
