# myproject/__init__.py
from __future__ import absolute_import, unicode_literals

# 確保 Django 在載入時也加載 Celery
from .celery import app as celery_app

__all__ = ('celery_app',)
