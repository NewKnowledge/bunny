from celery import Celery
from bunny.config import BROKER_URL

app = Celery('bunny', broker=BROKER_URL)