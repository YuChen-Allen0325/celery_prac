from celery import shared_task
from time import sleep


@shared_task
def add(x, y):
    sleep(5)  # 模擬一個耗時的任務
    print("HELLO!!!!!!!")
    return x + y
