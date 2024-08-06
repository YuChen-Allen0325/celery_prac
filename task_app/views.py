import boto3
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.cache import cache
from celery.result import AsyncResult
from .tasks import add
from .models import Image
from .serializers import ImageSerializer


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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            image = queryset.get(pk=pk)
        except Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(image)
        return Response(serializer.data)


class CloudWatchViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        cloudwatch = boto3.client('cloudwatch', region_name='ap-northeast-3')
        autoscaling = boto3.client('autoscaling', region_name='ap-northeast-3')

        try:
            alarms = cloudwatch.describe_alarms(AlarmNames=[
                                                'awsec2-i-078795b97e4f10b86-GreaterThanOrEqualToThreshold-CPUUtilization'])
            if alarms['MetricAlarms']:
                alarm = alarms['MetricAlarms'][0]
                state = alarm['StateValue']
                state_reason = alarm['StateReason']

                if state == 'ALARM':
                    # 替换 'CloudWatchPractice_autoscaling' 为你的 Auto Scaling 组名称
                    response = autoscaling.describe_auto_scaling_groups(
                        AutoScalingGroupNames=['CloudWatchPractice_autoscaling'])
                    group = response['AutoScalingGroups'][0]
                    current_desired_capacity = group['DesiredCapacity']
                    new_desired_capacity = current_desired_capacity + 1

                    autoscaling.set_desired_capacity(
                        AutoScalingGroupName='CloudWatchPractice_autoscaling',
                        DesiredCapacity=new_desired_capacity,
                        HonorCooldown=False
                    )
                    return Response({'message': 'Auto Scaling group capacity increased', 'new_desired_capacity': new_desired_capacity}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': f'Alarm state is {state}, Alarm state reason is {state_reason}. No action taken.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Alarm not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
