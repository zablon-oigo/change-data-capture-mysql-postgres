from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from typing import List
from src.config import Config 


c_app = Celery(
    "tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

c_app.config_from_object("src.config")





