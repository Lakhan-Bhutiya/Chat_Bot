from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .bot_logic import chatbot

def chat_view(request):
    return render(request, 'chat/index.html')

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            response_text = chatbot.get_response(user_message)
            return JsonResponse({'response': response_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

import csv
import io
from .models import QuestionAnswer
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(lambda u: u.is_superuser)
def upload_view(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a csv file')
        else:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string) 
            for column in csv.reader(io_string, delimiter=',', quotechar='"'):
                question = column[0]
                answer = column[1]
                if not QuestionAnswer.objects.filter(question=question).exists():
                    QuestionAnswer.objects.create(question=question, answer=answer)
            messages.success(request, 'Data uploaded successfully')
            return redirect('upload')
            
    data = QuestionAnswer.objects.all()
    return render(request, 'chat/upload.html', {'data': data})
