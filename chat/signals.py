from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import QuestionAnswer
from .bot_logic import chatbot

@receiver(post_save, sender=QuestionAnswer)
@receiver(post_delete, sender=QuestionAnswer)
def update_bot_data(sender, **kwargs):
    print("QuestionAnswer data changed. Reloading bot...")
    chatbot.load_data()
