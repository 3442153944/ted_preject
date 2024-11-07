from .BaseApiView import BaseAPIView
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
import json


class DeleteComment(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            admin_auth = self.check_admin_permission(request)
            if admin_auth:
                return admin_auth
            data = json.loads(request.body)
            comment_id = data.get('comment_id', None)
            if comment_id is None:
                return JsonResponse({'status': 400, 'msg': '缺少参数'}, status=400)
            with transaction.atomic():
                with connection.cursor() as cursor:
                    delete_comment_sql = '''
                    delete from comment_table where id=%s
                    '''
                    cursor.execute(delete_comment_sql, [comment_id])
                    if cursor.rowcount != 1:
                        raise DatabaseError('异常的评论删除数量，已回退操作')
                    return JsonResponse({'status': 200, 'msg': '删除评论成功'}, status=200)
        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
        except DatabaseError as e:
            self.handle_database_error(request, e)
