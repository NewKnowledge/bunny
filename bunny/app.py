from celery import Celery

from bunny.config import BROKER_URL

app = Celery('bunny.consumer', broker=BROKER_URL)
