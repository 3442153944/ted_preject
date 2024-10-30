from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection
from datetime import datetime
from .log.log import Logger
import json

logger = Logger()


def format_result(cursor):
    result = cursor.fetchall()
    col = cursor.description
    return [dict(zip([column[0] for column in col], row)) for row in result]


class GetDynamicList(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def request_path(self, request):
        request_ip = request.META.get('REMOTE_ADDR', '未知IP')
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f'{request_ip} 在 {now} 访问了 {request.path}'

    def get(self, request):
        logger.warning(self.request_path(request) + str(request.user))
        return render(request, '404.html', status=404)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get('user_id')
            if user_id is None:
                user_id = request.user.id
            request_type = data.get('request_type')
            self_limit = data.get('self_limit',10)
            self_offset = data.get('self_offset',0)
            other_limit = data.get('other_limit',10)
            other_offset = data.get('other_offset',0)

            if not user_id:
                return JsonResponse({'status': 400, 'msg': '缺少参数'}, status=400)

            if request_type not in ['self', 'other']:
                return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)

            with connection.cursor() as cursor:
                follow_list = self.get_follow_list(cursor, user_id) if request_type == 'self' else []
                follow_user_dynamic_list = self.get_dynamic_list_for_followers(cursor,
                                        follow_list,other_limit,other_offset) if request_type == 'self' else []
                self_dynamic_list = self.get_dynamic_list(cursor, user_id,self_limit,self_offset)

                return JsonResponse({
                    'status': 200,
                    'msg': '获取成功',
                    'data': {
                        'follow_user_dynamic_list': follow_user_dynamic_list,
                        'self_dynamic_list': self_dynamic_list
                    } if request_type == 'self' else self_dynamic_list
                })

        except Exception as e:
            logger.error(f'{self.request_path(request)}，错误信息为：{e}')
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)

    def get_follow_list(self, cursor, user_id):
        sql = 'SELECT * FROM follow_table WHERE operation_user_id=%s AND follow_status=1'
        cursor.execute(sql, [user_id])
        return format_result(cursor)

    def get_dynamic_list_for_followers(self, cursor, follow_list, limit=10, offset=0):
        follow_user_dynamic_list = []
        sql = ('SELECT dynamic_table.title, dynamic_table.content, dynamic_table.send_user_id, dynamic_table.send_time,'
               ' dynamic_table.dynamic_status, dynamic_table.img_list,auth_user.id as user_id,'
               'auth_user.username,auth_user.avatar_path '
               'FROM dynamic_table left join auth_user on auth_user.id=dynamic_table.send_user_id'
               ' WHERE send_user_id=%s AND dynamic_status=1')

        for follow_user in follow_list:
            cursor.execute(sql, [follow_user['target_user_id']])
            follow_user_dynamic_list.extend(format_result(cursor))

        # 合并后排序
        follow_user_dynamic_list.sort(key=lambda x: x['send_time'], reverse=True)

        # 应用分页
        paginated_list = follow_user_dynamic_list[offset:offset + limit]

        return paginated_list

    def get_dynamic_list(self, cursor, user_id,limit=10,offset=0):
        sql = 'SELECT * FROM dynamic_table WHERE send_user_id=%s AND dynamic_status=1 limit %s offset %s'
        cursor.execute(sql, [user_id,limit,offset])
        result = format_result(cursor)
        result.sort(key=lambda x: x['send_time'])
        return result
