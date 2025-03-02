# views/user/delete_user.py
import json

from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from .BaseApiView import BaseAPIView
from ..log.log import Logger

logger = Logger()


class DeleteUser(BaseAPIView):
    def post(self, request, *args, **kwargs):
        permission_error = self.check_admin_permission(request)
        if permission_error:
            return permission_error
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    data=json.loads(request.body.decode('utf-8'))
                    user_id = data.get('user_id',None)
                    if user_id is None:
                        return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)
                    delete_sql = '''
                    DELETE FROM auth_user WHERE id=%s
                    '''
                    cursor.execute(delete_sql, [user_id])
                    if cursor.rowcount != 1:
                        raise DatabaseError('异常删除数量，操作已回滚')

                    # 使用日志记录用户删除操作
                    logger.info(f'{request.user} 删除了用户 {user_id}')
                    return JsonResponse({'status': 200, 'msg': '删除成功'}, status=200)

        except DatabaseError as db_err:
            return self.handle_database_error(request, db_err)

        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器内部错误'}, status=500)
