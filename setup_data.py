import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot_project.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import QuestionAnswer

# Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created with password 'admin'")
else:
    print("Superuser 'admin' already exists")

# Load CSV
try:
    csv_path = r"..\Question&ans.csv" # relative to project root where this script runs? No, this script is in project root.
    # The csv is in the parent folder or same folder?
    # LS showed:
    # - c:\Users\lakha\OneDrive\Desktop\ChatBot/
    #   - Question&ans.csv
    #   - chatbot_project/
    # The current cwd for commands is chatbot_project root if I cd there.
    # Wait, the `cwd` in previous commands was `C:\Users\lakha\OneDrive\Desktop\ChatBot`.
    # And `manage.py` is in `C:\Users\lakha\OneDrive\Desktop\ChatBot`.
    # Wait, no.
    # `django-admin startproject chatbot_project .`
    # So `manage.py` is in `C:\Users\lakha\OneDrive\Desktop\ChatBot\manage.py`.
    # And `Question&ans.csv` is in `C:\Users\lakha\OneDrive\Desktop\ChatBot\Question&ans.csv`.
    
    csv_path = "Question&ans.csv"
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} rows in CSV.")
        
        # Clear existing? Maybe not.
        if QuestionAnswer.objects.count() == 0:
            for index, row in df.iterrows():
                QuestionAnswer.objects.create(
                    question=row['question'],
                    answer=row['answer']
                )
            print("Data loaded successfully.")
        else:
            print("Data already exists in DB.")
    else:
        print(f"CSV not found at {csv_path}")

except Exception as e:
    print(f"Error loading data: {e}")
