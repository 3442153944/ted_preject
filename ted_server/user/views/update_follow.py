from rest_framework.views import APIView
from django.db import connection, transaction, DatabaseError
import json
from .log.log import Logger
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

logger = Logger()


class UpdateFollow(APIView):
    def __init__(self):
        super().__init__()
        self.sql_dict = {
            'search_follow': '''
                SELECT follow_status FROM follow_table WHERE operation_user_id=%s AND target_user_id=%s
            ''',
            'update_follow': '''
                UPDATE follow_table SET operation_time=%s, follow_status=%s 
                WHERE target_user_id=%s AND operation_user_id=%s
            ''',
            'insert_follow': '''
                INSERT INTO follow_table (target_user_id, operation_user_id, operation_time, follow_status) 
                VALUES (%s, %s, %s, %s)
            '''
        }

    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request):
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 检查用户是否已登录
            if not request.user.is_authenticated:
                return JsonResponse({'status': 400, 'msg': '未登录'}, status=400)

            user_id = request.user.id
            data = json.loads(request.body.decode('utf-8'))
            target_user_id = data.get('target_user_id')
            operate_type = data.get('operate_type')

            # 校验参数
            if not target_user_id or target_user_id == user_id:
                return JsonResponse({'status': 400, 'msg': '参数错误或不能关注自己'}, status=400)
            if operate_type not in ['add', 'cancel']:
                return JsonResponse({'status': 400, 'msg': '操作类型错误'}, status=400)

            follow_status = 1 if operate_type == 'add' else 0

            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 查询是否已有关注记录
                    cursor.execute(self.sql_dict['search_follow'], [user_id, target_user_id])
                    result = cursor.fetchone()

                    if result:
                        # 更新关注状态
                        cursor.execute(self.sql_dict['update_follow'], [now, follow_status, target_user_id, user_id])
                        action_result = '已关注' if follow_status == 1 else '已取消关注'
                    else:
                        # 插入新的关注记录
                        cursor.execute(self.sql_dict['insert_follow'], [target_user_id, user_id, now, follow_status])
                        action_result = '关注成功' if follow_status == 1 else '取消关注成功'

                    if cursor.rowcount == 1:
                        return JsonResponse({'status': 200, 'msg': action_result}, status=200)
                    else:
                        raise DatabaseError('操作条数异常，已回退修改')

        except Exception as e:
            logger.error(f'请求信息：{self.request_path(request)}，错误信息：{e}')
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
