from apscheduler.schedulers.background import BackgroundScheduler
from .send_chat import send_chat


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_chat, 'interval', hours=2)
    scheduler.start()
