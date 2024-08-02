# celery_prac/celery.py
from __future__ import absolute_import, unicode_literals
import os
from . import settings
from celery import Celery

# 設定 Django 的設定模組
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_prac.settings')

# 創建 Celery 應用
app = Celery('celery_prac', ignore_result=False)

# 從 Django 的設定檔案中載入設定，所有 Celery 的設定都應該以 'CELERY_' 開頭
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自動發現並載入所有已註冊 Django app 的 tasks 模組
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
