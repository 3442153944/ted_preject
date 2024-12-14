from django.db import connection, transaction, DatabaseError
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import render
import json
from datetime import datetime
from .log.log import Logger

logger = Logger()


def format_result(cursor):
    result = cursor.fetchall()
    columns = cursor.description
    rows = [dict(zip([column[0] for column in columns], row)) for row in result]
    return rows


class RecordSubscriber(APIView):
    def get(self, request):
        logger.warning("非法请求,RecodeSubscriber")
        return render(request, '404.html', status=404)

    def post(self,request,*args,**kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            email=data.get('email',False)
            if email:
                get_email_sql='''
                select email from subscriber where email=%s
                '''

                insert_sql='''
                insert into subscriber (email, datetime) values (%s,%s)
                '''
                now=datetime.now()
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(get_email_sql,(email,))
                        if cursor.rowcount>=1:
                            return JsonResponse({'status':200,'msg':'订阅成功'},status=200)
                        cursor.execute(insert_sql,(email,now))
                        if cursor.rowcount==1:
                            return JsonResponse({'status':200,'msg':'订阅成功'},status=200)
                        else:
                            raise DatabaseError('异常新增条数已回退')
        except Exception as e :
            logger.error(e)
            return JsonResponse({'status':500,'msg':'服务器错误'},status=500)