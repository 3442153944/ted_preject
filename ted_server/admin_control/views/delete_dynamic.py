from .BaseApiView import BaseAPIView
from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
import json
from ..log.log import Logger

logger = Logger()


class DeleteDynamic(BaseAPIView):
    def post(self, request, *args, **kwargs):
        try:
            admin_auth = self.check_admin_permission(request)
            if admin_auth:
                return admin_auth
            data = json.loads(request.body.decode('utf-8'))
            dynamic_id = data.get('dynamic_id', None)
            if dynamic_id is None:
                return JsonResponse({'status': 400, 'msg': '参数错误'}, status=400)
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("delete from dynamic_table where id=%s", (dynamic_id,))
                    if cursor.rowcount != 1:
                        DatabaseError('删除条数异常，已回退修改')
                    return JsonResponse({'status': 200, 'msg': '删除成功'}, status=200)
        except Exception as e:
            self.log_error(request, e)
            return JsonResponse({'status': 500, 'msg': '服务器错误'}, status=500)
        except DatabaseError as e:
            self.handle_database_error(request, e)
