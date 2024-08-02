from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from celery.result import AsyncResult
from .tasks import add


class AddView(APIView):
    def get(self, request):
        task_id = request.query_params.get('task_id')
        result = AsyncResult(task_id)
        if result.ready():
            print(result.status)
        return Response({'result': result.status}, status=200)

    def post(self, request):
        x = request.data.get('x')
        y = request.data.get('y')
        print(x, y)
        task = add.delay(x, y)  # 使用 .delay() 調用 Celery 任務

        return Response({'task_id': task.id, 'status': 'Task started'}, status=200)


class MyDataView(APIView):
    def get(self, request, *args, **kwargs):
        # 嘗試從緩存中獲取數據
        data = cache.get('my_data_key')
        if not data:
            # 如果緩存中沒有數據，從數據庫或其他來源獲取數據
            data = {
                'key': 'value',  # 假設這是我們從數據庫獲取的數據
            }
            # 將數據存入緩存，設置過期時間（例如60秒）
            cache.set('my_data_key', data, timeout=60)
        
        return Response(data)
